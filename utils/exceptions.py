class ScrappingError(Exception):
    """Basic exception for scrapping."""

class WeekendError(Exception):
    """Exception: due to Druzba and FiitFood structure, menu is not available during weekend."""

# class MenuNotFoundError(ScrappingError):
#     """Exception: today menu not found."""

class MenuNotFoundError(Exception):
    def __init__(self, date_expected, date_found):
        self.date_expected = date_expected
        self.date_found = date_found
        super().__init__(f"Menu sa nenašlo: očakávané {date_expected}, nájdené {date_found}")

class MenuBodyNotFoundError(ScrappingError):
    """Exception: missing menu files."""

class InvalidGuildError(ScrappingError):
    """Exception: guild not in config"""

class InvalidChannelError(ScrappingError):
    """Exception: channel not in config"""