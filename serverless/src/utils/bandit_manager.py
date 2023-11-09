#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
from uuid import uuid4
from os import mkdir, path, system
from typing import Any, List, Dict, Tuple
from dataclass_wizard import JSONWizard
from dataclasses import dataclass, field

CODE_FILE_NAME = "code.py"
OUTPUT_FILE_NAME = "output.json"


@dataclass
class BanditResult(JSONWizard):
    errors: List[Any]
    generated_at: str
    results: Any
    metrics: Dict[str, Dict[str, int]] = field(default_factory=dict)


def write_python_file(code_as_string: str) -> str:
    directory = path.join(path.curdir, uuid4().__str__())
    mkdir(directory)
    file_path = path.join(directory, CODE_FILE_NAME)
    with open(file_path, "w") as file:
        file.write(code_as_string)
        file.flush()
    return directory


def run_bandit(directory: str):
    system(
        f"bandit {path.join(directory, CODE_FILE_NAME)} -f json -o {path.join(directory, OUTPUT_FILE_NAME)}"
    )


def read_output(directory: str) -> BanditResult:
    file_path = path.join(directory, OUTPUT_FILE_NAME)
    if path.exists(file_path):
        with open(file_path, "r") as file:
            result = BanditResult.from_json(file)
            return result
    else:
        raise RuntimeError("could not read result of Bandit analysis")


def evaluate_bandit_results(results: BanditResult) -> bool:
    return results.metrics["_total"]["SEVERITY.HIGH"] == 0


def scan_user_code(code_as_string: str) -> Tuple[bool, BanditResult]:
    directory = write_python_file(code_as_string)
    run_bandit(directory)
    results = read_output(directory)
    if evaluate_bandit_results(results):
        return (True, results)
    else:
        print(f"code has security vulnerabilities in it: {results.to_json()}")
        return (False, results)
