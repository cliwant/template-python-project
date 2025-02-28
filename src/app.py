from src.settings import AppSettings
from src.utils import logging


class App:
    def __init__(self) -> None:
        self.settings = AppSettings()
        self.logger = logging.get_logger(level=self.settings.log_level)

    def run(self) -> None:
        self.logger.debug("로그가 디버그 레벨로 설정 되었습니다.")
        self.logger.info(
            "[%s]가 [%s] 프로파일로 실행중입니다.",
            self.settings.title,
            self.settings.profile,
        )


def create_app() -> App:
    return App()
