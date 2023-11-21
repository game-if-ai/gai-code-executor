#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
from typing import Dict, Any, Tuple
from contextlib import redirect_stdout
from io import StringIO
from src.utils.bandit_manager import scan_user_code


def execute_code(code: str, uuid: str = "") -> Tuple[str, str]:
    try:
        (code_is_valid, bandit_result_as_string) = scan_user_code(code, uuid)
        if code_is_valid:
            local_vars: Dict[str, Any] = {}
            string_io = StringIO()
            console_output = ""
            with redirect_stdout(string_io):
                exec(code, local_vars, local_vars)
                console_output = string_io.getvalue()

            if "result" in local_vars.keys():
                return (local_vars["result"], console_output)
            else:
                local_vars.pop(
                    "__builtins__"
                )  # don't display the builtin variables.  It's a lot of information we don't need
                return (
                    f"no result variable instantiated.  Could not return result.  local vars:\n {str(local_vars)}",
                    console_output,
                )
        else:
            return (bandit_result_as_string, "")
    except Exception as e:
        print(local_vars)
        return (e.__str__(), console_output)
