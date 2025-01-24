import unittest
from unittest.mock import patch, MagicMock
from backend.datacollection.bookmakers.sts import get_data

def mock_response(content, status_code=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.text = content
    return mock_resp

class TestSts(unittest.TestCase):

    @patch("backend.datacollection.bookmakers.sts.requests.get")
    def test_get_data(self, mock_get):
        mock_html = """
        <html>
        <body>
            <div class="match-tile-event-details-teams__team match-tile-event-details-teams__team--1">Team A</div>
            <div class="match-tile-event-details-teams__team match-tile-event-details-teams__team--2">Team B</div>
            <div class="odds-button__odd-value ng-star-inserted">1</div>
            <div class="odds-button__odd-value ng-star-inserted">2</div>
            <div class="odds-button__odd-value ng-star-inserted">3</div>
        </body>
        </html>
        """
        mock_get.return_value = mock_response(mock_html)

        data = get_data("link1")
        self.assertEqual(len(data), 1)

        match = data[0]
        self.assertEqual(match["identifier"], "Team A:Team B")
        self.assertEqual(match["team1"], "Team A")
        self.assertEqual(match["team2"], "Team B")
        self.assertEqual(match["course1"], "1")
        self.assertEqual(match["courseX"], "2")
        self.assertEqual(match["course2"], "3")

    @patch("backend.datacollection.bookmakers.sts.requests.get")
    def test_invalid_response(self, mock_get):
        mock_get.return_value = mock_response("", status_code=500)

        data = get_data("link2")
        self.assertEqual(len(data), 0)