class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""

    pass


class PageNotDownloadError(Exception):
    """Вызывается, когда основная страница не загружена."""

    pass


class ParserFindListWithTagException(Exception):
    """Вызывается, когда парсер не может найти список с тегами."""

    pass
