import os

from django.conf import settings
from loguru import logger

from candle_lab import variables


class Logger:
    def __init__(self, directory: str, file: str):
        self.logger = logger
        self.dir_checker(directory=directory)
        self.log_file_path = os.path.join(settings.BASE_DIR, "logs/%s/%s_{time:YYYY-MM-DD}.log" % (directory, file))
        self.logger.add(
            self.log_file_path,
            format="<green>{time}</green> {level} <level>{message}</level>",
            serialize=True,
            rotation="10 MB",
            compression="zip",
            level="DEBUG",
            filter=lambda record: record["extra"]["module"] == file
        )
        self.bind(params={"environment": variables.ENVIRONMENT, "release": variables.RELEASE, "module": file})

    @staticmethod
    def dir_checker(directory: str):
        if directory not in os.listdir(os.path.join(settings.BASE_DIR, "logs")):
            os.mkdir(os.path.join(settings.BASE_DIR, "logs", directory))  # pragma: no cover

    def bind(self, params: dict):
        self.logger = self.logger.bind(**params)
