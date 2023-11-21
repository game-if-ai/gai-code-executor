#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
from uuid import uuid4
from os import mkdir, path, system
from typing import Dict, Tuple
from dataclass_wizard import JSONWizard
from dataclasses import dataclass, field
from shutil import rmtree

CODE_FILE_NAME = "code.py"
OUTPUT_FILE_NAME = "output.json"


@dataclass
class BanditResult(JSONWizard):
    generated_at: str
    metrics: Dict[str, Dict[str, int]] = field(default_factory=dict)


def write_python_file(code_as_string: str, uuid: str = "") -> str:
    if uuid != "":
        directory = path.join(path.curdir, uuid)
    else:
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


def read_output(directory: str) -> Tuple[BanditResult, str]:
    file_path = path.join(directory, OUTPUT_FILE_NAME)
    if path.exists(file_path):
        with open(file_path, "r") as file:
            result_as_string = file.read()
            result = BanditResult.from_json(result_as_string)
            return (result, result_as_string)
    else:
        raise RuntimeError("could not read result of Bandit analysis")


def evaluate_bandit_results(results: BanditResult) -> bool:
    return (
        results.metrics["_totals"]["SEVERITY.HIGH"] == 0
        and results.metrics["_totals"]["SEVERITY.MEDIUM"] == 0
    )


def scan_user_code(code_as_string: str, uuid: str = "") -> Tuple[bool, str]:
    directory = write_python_file(code_as_string, uuid)
    run_bandit(directory)
    (results, results_as_string) = read_output(directory)
    rmtree(directory)
    if evaluate_bandit_results(results):
        return (True, results_as_string)
    else:
        print(f"code has security vulnerabilities in it: {results_as_string}")
        return (False, results_as_string)
