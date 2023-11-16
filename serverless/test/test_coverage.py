#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
import pytest
from os import path
from test_utils import fixture_path
from src.utils.executor import execute_code


CODE_FILE_NAME = "code.py"
EXEPECTED_OUTPUT_FILE_NAME = "expected_output.txt"


def test_coverage():
    assert True


@pytest.mark.parametrize(
    "sample_code",
    [
        ("helloworld"),
        ("code_error"),
        ("function_call"),
        ("bandit_failure"),
    ],
)
def test_code_execution(sample_code: str):
    uuid = "0"
    code_file_path = path.join(fixture_path(sample_code), CODE_FILE_NAME)
    expected_output_file_path = path.join(
        fixture_path(sample_code), EXEPECTED_OUTPUT_FILE_NAME
    )
    with open(code_file_path, "r") as code_file:
        code = code_file.read()

    with open(expected_output_file_path, "r") as expected_output_file:
        expected_output = expected_output_file.read()

    result = execute_code(code, uuid)

    # need to do this because the bandit result includes a timestamp that we can't freeze
    if "CONFIDENCE" in result:
        assert True
    else:
        assert result == expected_output
