#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
import json
import base64
import uuid
import datetime
import os
import boto3
from src.utils.utils import create_json_response, require_env
from src.utils.logger import get_logger

log = get_logger("execute_request")
JOBS_TABLE_NAME = require_env("JOBS_TABLE_NAME")
log.info(f"using table {JOBS_TABLE_NAME}")
JOBS_SQS_NAME = require_env("JOBS_SQS_NAME")
aws_region = os.environ.get("REGION", "us-east-1")
ttl_sec = os.environ.get("TTL_SEC", (60 * 60 * 24) * 20)  # 20 days

sqs = boto3.client("sqs", region_name=aws_region)
queue_url = sqs.get_queue_url(QueueName=JOBS_SQS_NAME)["QueueUrl"]
log.info(f"using queue {queue_url}")

dynamodb = boto3.resource("dynamodb", region_name=aws_region)
job_table = dynamodb.Table(JOBS_TABLE_NAME)


def handler(event, context):
    print(json.dumps(event))
    if "body" not in event:
        return create_json_response(
            400, {"error": "bad request: body not in event"}, event
        )

    if event["isBase64Encoded"]:
        body = base64.b64decode(event["body"])
    else:
        body = event["body"]
    execute_request = json.loads(body)

    if "lesson" not in execute_request:
        return create_json_response(
            400,
            {"error": "Bad request: Need lesson in json body"},
            event,
        )
    code = execute_request["code"] if "code" in execute_request else ""
    lesson = execute_request["lesson"]
    ping = execute_request["ping"] if "ping" in execute_request else False

    job_id = str(uuid.uuid4())
    execute_job = {
        "id": job_id,
        "code": code,
        "lesson": lesson,
        "ping": ping,
        "status": "QUEUED",
        "created": datetime.datetime.now().isoformat(),
        # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/time-to-live-ttl-before-you-start.html#time-to-live-ttl-before-you-start-formatting
        "ttl": int(datetime.datetime.now().timestamp()) + ttl_sec,
    }

    log.debug(execute_job)
    sqs_msg = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(execute_job))
    log.info(sqs_msg)

    job_table.put_item(Item=execute_job)

    data = {
        "id": job_id,
        "status": "QUEUED",
        "statusUrl": f"/execute/status/{job_id}",
    }
    return create_json_response(200, data, event)
