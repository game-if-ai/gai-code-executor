#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
import json
import datetime
import os
import boto3
from src.utils.utils import require_env
from src.utils.logger import get_logger
from src.utils.executor import execute_code

log = get_logger("execute")
shared_root = os.environ.get("SHARED_ROOT") or "shared"
log.info(f"shared: {shared_root}")
JOBS_TABLE_NAME = require_env("JOBS_TABLE_NAME")
log.info(f"using table {JOBS_TABLE_NAME}")
MODELS_BUCKET = require_env("MODELS_BUCKET")
log.info(f"bucket: {MODELS_BUCKET}")
s3 = boto3.client("s3")
aws_region = os.environ.get("REGION", "us-east-1")
dynamodb = boto3.resource("dynamodb", region_name=aws_region)
job_table = dynamodb.Table(JOBS_TABLE_NAME)


def handler(event, context):
    for record in event["Records"]:
        request = json.loads(str(record["body"]))
        code = request["code"]
        # ping = request["ping"] if "ping" in request else False
        update_status(request["id"], "IN_PROGRESS")

        try:
            result = execute_code(code)
            update_status(request["id"], "SUCCESS", result)
        except Exception as e:
            log.exception(e)
            update_status(request["id"], "FAILURE", e.args.__str__())


def update_status(id, status, result=""):
    job_table.update_item(
        Key={"id": id},
        # status is reserved, workaround according to:
        # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeNames.html
        UpdateExpression="set #status = :s, updated = :u, result = :res",
        ExpressionAttributeNames={
            "#status": "status",
        },
        ExpressionAttributeValues={
            ":s": status,
            ":u": datetime.datetime.now().isoformat(),
            ":res": result,
        },
    )
