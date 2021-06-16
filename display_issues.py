import asyncio
import subprocess
import sys
import textwrap

from core.env import URI_WATER_ISSUES_SOURCE_HTML
from parsers.issues_parser.html import IssuesParserHTML
from repositories.issues_html_repository.http import IssuesHTMLRepositoryHTTP

if __name__ == "__main__":
    issues_html_repo = IssuesHTMLRepositoryHTTP(uri=URI_WATER_ISSUES_SOURCE_HTML)
    issues_html_parser = IssuesParserHTML(repo=issues_html_repo)

    issues = asyncio.run(issues_html_parser.parse())

    try:
        pager = subprocess.Popen(
            ["less", "-F", "-R", "-S", "-X", "-K"],
            stdin=subprocess.PIPE,
            stdout=sys.stdout,
        )
        if pager.stdin is None:
            exit(1)

        for issue in issues:

            for line in textwrap.wrap(issue.formatted):
                if line is not None:
                    pager.stdin.write((line + "\n").encode())

            pager.stdin.write("\n------\n".encode())

        pager.stdin.close()
        pager.wait()
    except KeyboardInterrupt:
        pass
