from src.exceptions import RepositoryException


class IssuesHTMLRepositoryException(RepositoryException):
    pass


class LoadingHTMLIssuesException(IssuesHTMLRepositoryException):
    pass
