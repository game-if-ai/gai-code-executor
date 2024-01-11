#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
from abc import ABC, abstractmethod
from typing import Any
import shutil
import os


class LessonDownloader(ABC):
    @abstractmethod
    def download_files_for_lesson(self, models_bucket: str, s3: Any):
        raise NotImplementedError()


class CafeDownloader(LessonDownloader):
    def download_files_for_lesson(self, models_bucket: str, s3: Any):
        s3.download_file(models_bucket, "cafe/reviews.json", "/tmp/reviews.json")


class FruitPickerDownloader(LessonDownloader):
    def download_files_for_lesson(self, models_bucket: str, s3: Any):
        s3.download_file(models_bucket, "fruitpicker/fruits.json", "/tmp/fruits.json")


class NeuralMachineTranslationDownloader(LessonDownloader):
    def download_files_for_lesson(self, models_bucket: str, s3: Any):
        s3.download_file(
            models_bucket,
            "neural_machine_translation/small_vocab_en",
            "/tmp/small_vocab_en",
        )
        s3.download_file(
            models_bucket,
            "neural_machine_translation/small_vocab_fr",
            "/tmp/small_vocab_fr",
        )
        s3.download_file(
            models_bucket,
            "neural_machine_translation/translation_tf.zip",
            "/tmp/translation_tf.zip",
        )
        os.mkdir("/tmp/translation.tf")
        shutil.unpack_archive("/tmp/translation_tf.zip", "/tmp/translation.tf", "zip")


class PlanesDownloader(LessonDownloader):
    def download_files_for_lesson(self, models_bucket: str, s3: Any):
        s3.download_file(
            models_bucket,
            "planes/Epoch30_tiny_accuracy.json",
            "/tmp/Epoch30_tiny_accuracy.json",
        )
        s3.download_file(
            models_bucket,
            "planes/Epoch60_tiny_accuracy.json",
            "/tmp/Epoch60_tiny_accuracy.json",
        )
        s3.download_file(
            models_bucket,
            "planes/Epoch30_small_accuracy.json",
            "/tmp/Epoch30_small_accuracy.json",
        )
        s3.download_file(
            models_bucket,
            "planes/Epoch60_small_accuracy.json",
            "/tmp/Epoch60_small_accuracy.json",
        )
        s3.download_file(
            models_bucket,
            "planes/Epoch30_medium_accuracy.json",
            "/tmp/Epoch30_medium_accuracy.json",
        )
        s3.download_file(
            models_bucket,
            "planes/Epoch60_medium_accuracy.json",
            "/tmp/Epoch60_medium_accuracy.json",
        )
        s3.download_file(
            models_bucket,
            "planes/Epoch30_large_accuracy.json",
            "/tmp/Epoch30_large_accuracy.json",
        )
        s3.download_file(
            models_bucket,
            "planes/Epoch60_large_accuracy.json",
            "/tmp/Epoch60_large_accuracy.json",
        )
