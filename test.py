import asyncio

from parsers.electricity_issues_parser.html import ElectricityIssuesParserHTML
from repositories.electricity_issues_html_repository.http import (
    ElectricityIssuesHTMLRepositoryHTTP,
)

base_uri = "https://dp.rosseti-yug.ru/res/?state=549&district=%E3.%D2%E0%E3%E0%ED%F0%EE%E3&places=%E3.%D2%E0%E3%E0%ED%F0%EE%E3&street=&filter_set=%CF%EE%EA%E0%E7%E0%F2%FC"
repo = ElectricityIssuesHTMLRepositoryHTTP(base_uri)
parser = ElectricityIssuesParserHTML(repo=repo)
asyncio.run(parser.parse())
