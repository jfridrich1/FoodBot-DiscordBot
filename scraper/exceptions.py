class ScrappingError(Exception):
    """Basic exception for scrapping."""

class MenuNotFoundError(ScrappingError):
    """Exception: today menu not found."""

class MenuBodyNotFoundError(ScrappingError):
    """Exception: missing menu files."""

class InvalidGuildError(ScrappingError):
    """Exception: guild not in config"""

class InvalidChannelError(ScrappingError):
    """Exception: channel not in config"""