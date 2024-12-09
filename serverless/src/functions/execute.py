#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
import json
import datetime
import os
import shutil
import boto3
from src.utils.utils import require_env
from src.utils.logger import get_logger
from src.utils.executor import execute_code, FAILURE_STATE
from src.utils.s3_file_downloader import (
    LessonDownloader,
    CafeDownloader,
    FruitPickerDownloader,
    NeuralMachineTranslationDownloader,
    PlanesDownloader,
    WineDownloader,
)
from typing import Dict

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


def log_temp_folder():
    # List contents of the /tmp folder and calculate the total size
    temp_path = "/tmp"
    num_files_listed = 0
    total_size = 0  # To accumulate the size of all files

    if os.path.exists(temp_path):
        log.info("Contents of /tmp folder:")
        for root, dirs, files in os.walk(temp_path):
            for name in files:
                file_path = os.path.join(root, name)
                file_size = os.path.getsize(file_path)
                total_size += file_size
            for name in dirs:
                num_files_listed += 1
    else:
        log.info("/tmp folder does not exist.")

    # Log the total size of files in /tmp
    log.info(f"Total size of files in /tmp: {total_size / (1024 ** 2):.2f} MB")

    # Check available space in the container
    total, used, free = shutil.disk_usage("/")
    log.info(f"Total space: {total / (1024 ** 3):.2f} GB")
    log.info(f"Used space: {used / (1024 ** 3):.2f} GB")
    log.info(f"Free space: {free / (1024 ** 3):.2f} GB")


# Call the function to log the details

LESSON_DOWNLOADERS: Dict[str, LessonDownloader] = {
    "planes": PlanesDownloader(),
    "cafe": CafeDownloader(),
    "neural_machine_translation": NeuralMachineTranslationDownloader(),
    "fruitpicker": FruitPickerDownloader(),
    "wine": WineDownloader(),
}


def handler(event, context):
    log_temp_folder()
    for record in event["Records"]:
        request = json.loads(str(record["body"]))
        code = request["code"]
        lesson = request["lesson"]
        # ping = request["ping"] if "ping" in request else False
        update_status(request["id"], "IN_PROGRESS")

        try:
            LESSON_DOWNLOADERS[lesson].download_files_for_lesson(MODELS_BUCKET, s3)
            (result, console, state) = execute_code(code)
            update_status(request["id"], state, result, console)
        except Exception as e:
            log.exception(e)
            update_status(
                request["id"], FAILURE_STATE, f"{e.__class__.__name__}:{e.__str__()}"
            )


def update_status(id, status, result="", console=""):
    job_table.update_item(
        Key={"id": id},
        # status is reserved, workaround according to:
        # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeNames.html
        UpdateExpression="set #status = :s, updated = :u, rezult = :res, console = :cons",
        ExpressionAttributeNames={
            "#status": "status",
        },
        ExpressionAttributeValues={
            ":s": status,
            ":u": datetime.datetime.now().isoformat(),
            ":res": result,
            ":cons": console,
        },
    )
