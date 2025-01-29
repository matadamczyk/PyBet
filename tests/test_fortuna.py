import unittest
from unittest.mock import patch, MagicMock
from backend.datacollection.bookmakers.fortuna import get_all_matches


def mock_response(content, status_code=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.text = content
    return mock_resp


class TestFortuna(unittest.TestCase):

    @patch("backend.datacollection.bookmakers.fortuna.requests.get")
    def test_get_all_matches(self, mock_get):
        mock_main_page_html = """
        <html>
        <body>
            <a class="event-link js-event-link" href="link1"></a>
            <a class="event-link js-event-link" href="link2"></a>
        </body>
        </html>
        """
        mock_event_page_html = """
        <html>
        <body>
            <span class="market-name">Team A - Team B</span>
            <td class="col-odds"><span class="odds-value">1</span></td>
            <td class="col-odds"><span class="odds-value">2</span></td>
            <td class="col-odds"><span class="odds-value">3</span></td>
        </body>
        </html>
        """
        mock_get.side_effect = [
            mock_response(mock_main_page_html),
            mock_response(mock_event_page_html),
            mock_response(mock_event_page_html),
        ]

        matches = get_all_matches("link1")
        self.assertEqual(len(matches), 2)

        match1 = matches[0]
        self.assertEqual(match1["identifier"], "Team A:Team B")
        self.assertEqual(match1["team1"], "Team A")
        self.assertEqual(match1["team2"], "Team B")
        self.assertEqual(match1["course1"], "1.00")
        self.assertEqual(match1["courseX"], "2.00")
        self.assertEqual(match1["course2"], "3.00")

    @patch("backend.datacollection.bookmakers.fortuna.requests.get")
    def test_get_all_matches_invalid_response(self, mock_get):
        mock_get.return_value = mock_response("", status_code=500)

        matches = get_all_matches("link3")
        self.assertEqual(len(matches), 0)
