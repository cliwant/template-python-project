import src.utils.logging as logging


class App:

    def __init__(self) -> None:
        self.logger = logging.get_logger()

    def run(self) -> None:
        self.logger.warning("okok")


def create_app() -> App:
    return App()
