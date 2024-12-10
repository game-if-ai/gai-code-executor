#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
from typing import Tuple
from contextlib import redirect_stdout
from io import StringIO
from src.utils.bandit_manager import scan_user_code
from src.utils.logger import get_logger
from contextlib import contextmanager
import shutil
import os

SUCCESS_STATE = "SUCCESS"
FAILURE_STATE = "FAILURE"

log = get_logger("executor")


@contextmanager
def tempdir_cleanup_context():
    namespace = {}
    try:
        yield namespace
    finally:
        log.info("cleaning up tempdir")
        # Check for `tempdir` and clean up if it exists
        tempdir = namespace.get("tempdir")
        if tempdir and isinstance(tempdir, str) and os.path.isdir(tempdir):
            shutil.rmtree(tempdir)
            log.info(f"Cleaned up tempdir: {tempdir}")


def execute_code(code: str, uuid: str = "") -> Tuple[str, str, str]:
    log.info("entering execute code function")
    console_output = ""
    try:
        log.info("scanning code")
        (code_is_valid, bandit_result_as_string) = scan_user_code(code, uuid)
        if code_is_valid:
            with tempdir_cleanup_context() as local_vars:
                string_io = StringIO()
                log.info("executing code")
                with redirect_stdout(string_io):
                    exec(code, local_vars, local_vars)
                console_output = string_io.getvalue()
                log.info(console_output)
                log.info("code executed")
                if "result" in local_vars.keys():
                    log.info(local_vars["result"])
                    return (local_vars["result"], console_output, SUCCESS_STATE)
                else:
                    local_vars.pop(
                        "__builtins__"
                    )  # don't display the builtin variables.  It's a lot of information we don't need
                    return (
                        f"no result variable instantiated.  Could not return result.  local vars:\n {str(local_vars)}",
                        console_output,
                        FAILURE_STATE,
                    )
        else:
            return (bandit_result_as_string, "", FAILURE_STATE)
    except Exception as e:
        log.info("exception thrown")
        console_output = string_io.getvalue()
        return (f"{e.__class__.__name__}:{e.__str__()}", console_output, FAILURE_STATE)
