from bs4 import BeautifulSoup
from mini_search.utils.scrape_utils import parse_tables


def test_parse_tables():
    table = """
    <header>
    </header>
    <body>
    <table>
        <tr>
            <th>Company</th>
            <th>Contact</th>
            <th>Country</th>
        </tr>
        <tr>
            <td>CompaInc</td>
            <td>CompaContact</td>
            <td>CompaCountry</td>
        </tr>
    </table>
    </body>
    """

    soup = BeautifulSoup(table, "html.parser")
    tokenizedTables = parse_tables(soup)
    assert tokenizedTables[0]["headersTag"] == [["company"], ["contact"], ["country"]]
    assert tokenizedTables[0]["tableDataTag"] == [
        [["compainc"], ["compacontact"], ["compacountry"]]
    ]
