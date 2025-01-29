import unittest
from unittest.mock import patch, MagicMock
from backend.datacollection.bookmakers.betclic import (
    fetch_matches_overview,
    fetch_match_details,
    fetch_match_details_retry,
)


def mock_response(content, status_code=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.text = content
    return mock_resp


class TestBetclic(unittest.TestCase):

    @patch("backend.datacollection.bookmakers.betclic.requests.get")
    def test_fetch_matches_overview(self, mock_get):
        mock_html = """
        <html>
        <body>
            <a class="cardEvent ng-star-inserted" href="/match/123">
                <scoreboards-scoreboard-global class="scoreboard_wrapper">
                    <div data-qa="contestant-1-label">Team A</div>
                    <div data-qa="contestant-2-label">Team B</div>
                </scoreboards-scoreboard-global>
            </a>
        </body>
        </html>
        """
        mock_get.return_value = mock_response(mock_html)

        with patch(
            "backend.datacollection.bookmakers.betclic.fetch_match_details_retry"
        ):
            matches = fetch_matches_overview("link1")

        match = matches[0]
        self.assertEqual(match["identifier"], "Team A:Team B")
        self.assertEqual(match["team1"], "Team A")
        self.assertEqual(match["team2"], "Team B")

    @patch("backend.datacollection.bookmakers.betclic.requests.get")
    def test_fetch_match_details(self, mock_get):
        mock_html = """
        <html>
        <body>
            <div class="marketBox_lineSelection">
                <span class="btn_label ng-star-inserted">1</span>
            </div>
            <div class="marketBox_lineSelection">
                <span class="btn_label ng-star-inserted">2</span>
            </div>
            <div class="marketBox_lineSelection">
                <span class="btn_label ng-star-inserted">3</span>
            </div>
        </body>
        </html>
        """
        mock_get.return_value = mock_response(mock_html)

        details = fetch_match_details("link2")
        self.assertEqual(details["course1"], 1)
        self.assertEqual(details["courseX"], 2)
        self.assertEqual(details["course2"], 3)

    @patch("backend.datacollection.bookmakers.betclic.requests.get")
    def test_a_fetch_match_details_retry(self, mock_get):
        mock_html = """
        <html>
        <body>
            <div class="marketBox_lineSelection">
                <span class="btn_label ng-star-inserted">1</span>
            </div>
            <div class="marketBox_lineSelection">
                <span class="btn_label ng-star-inserted">2</span>
            </div>
            <div class="marketBox_lineSelection">
                <span class="btn_label ng-star-inserted">3</span>
            </div>
        </body>
        </html>
        """
        mock_get.return_value = mock_response(mock_html)

        details = fetch_match_details_retry("link3")
        self.assertEqual(details["course1"], 1)
        self.assertEqual(details["courseX"], 2)
        self.assertEqual(details["course2"], 3)

    @patch("backend.datacollection.bookmakers.betclic.requests.get")
    def test_b_fetch_match_details_retry(self, mock_get):
        mock_get.side_effect = Exception()

        details = fetch_match_details_retry("link4", delay=1)
        self.assertIsNone(details)
