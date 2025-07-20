class ScrappingError(Exception):
    """Basic exception for scrapping."""

class MenuNotFoundError(ScrappingError):
    """Exception: today menu not found."""

class MenuBodyNotFoundError(ScrappingError):
    """Exception: missing menu files."""

class ImageNotFoundError(ScrappingError):
    """Exception: missing image file."""