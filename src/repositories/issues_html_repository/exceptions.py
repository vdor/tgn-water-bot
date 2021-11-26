from src.core.exceptions import RepositoryException


class IssuesHTMLRepositoryException(RepositoryException):
    pass


class LoadingHTMLIssuesException(IssuesHTMLRepositoryException):
    pass
