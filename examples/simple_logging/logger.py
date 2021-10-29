import logging
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum


class Color(Enum):
    BLACK = "0"
    RED = "1"
    GREEN = "2"
    YELLOW = "3"
    BLUE = "4"
    MAGENTA = "5"
    CYAN = "6"
    WHITE = "7"


@dataclass
class TermColor:
    foreground: Color
    background: Optional[Color] = None


ESC_SEQ = "\x1b["
RESET = f"{ESC_SEQ}0m"


DEFAULT_COLORS = {
    logging.DEBUG: TermColor(Color.BLUE),
    logging.INFO: TermColor(Color.WHITE),
    logging.WARNING: TermColor(Color.YELLOW),
    logging.ERROR: TermColor(Color.RED),
    logging.CRITICAL: TermColor(Color.WHITE, Color.RED)
}


class ColorFormatter(logging.Formatter):

    def __init__(
        self, *args,
        colors: Optional[Dict[int, TermColor]] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        colors = DEFAULT_COLORS if colors is None else colors
        self._termcolors = self.make_termcolors(colors)

    @staticmethod
    def make_termcolors(
        level_colors: Dict[int, TermColor]
    ) -> Dict[int, str]:

        result = {}
        for level, color in level_colors.items():
            color_string = f"{ESC_SEQ}3{color.foreground.value}"
            if color.background is not None:
                color_string += f";4{color.background.value}"
            color_string += "m"
            result[level] = color_string

        return result

    def make_color_log(self, levelno) -> str:

        return f"{self._termcolors.get(levelno)}{self._fmt}{RESET}"

    def format(self, record):

        formatter = logging.Formatter(self.make_color_log(record.levelno))

        return formatter.format(record)


def get_stream_handler(level, formatter: logging.Formatter):

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    return stream_handler


def get_stream_logger(
    name: str, level: int, formatter: logging.Formatter
) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = get_stream_handler(level, formatter)
    logger.addHandler(stream_handler)

    return logger


if __name__ == "__main__":

    log_format = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    formatter = ColorFormatter(log_format)
    # formatter = logging.Formatter(log_format, datefmt="%Y%m%d %H:%M:%S")
    logger = get_stream_logger("deflog", logging.DEBUG, formatter)

    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
