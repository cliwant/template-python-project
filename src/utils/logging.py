import logging
import os

import colorlog


def get_logger(name: str = __name__, level: str | int = logging.INFO) -> logging.Logger:
    # Define log format
    log_format = "%(asctime)s.%(msecs)03d %(log_color)s%(levelname)-8s%(reset)s %(process)5d --- [%(cyan)s%(threadName)-12s%(reset)s] %(bold_purple)s%(full_path)30s:%(lineno)-4d%(reset)s >> %(bold_blue)s%(funcName)20s%(reset)s : %(message)s"

    # Define log color by log level
    log_colors = {
        "DEBUG": "light_black",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "bold_red",
        "CRITICAL": "bg_bold_red",
    }

    # Create console handler and set level and format
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        _CustomFormatter(log_format, log_colors=log_colors, datefmt="%Y-%m-%d %H:%M:%S")
    )

    # Set level and handler
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)

    return logger


class _CustomFormatter(colorlog.ColoredFormatter):
    def format(self, record: logging.LogRecord) -> str:
        # 절대 경로에서 패키지 경로만 추출
        project_root = os.getcwd()  # 현재 실행 위치를 기준으로 경로 정리
        if record.pathname.startswith(project_root):
            record.full_path = record.pathname[len(project_root) + 1 :].replace(
                os.sep, "."
            )
        else:
            record.full_path = record.pathname.replace(os.sep, ".")

        return super().format(record)
