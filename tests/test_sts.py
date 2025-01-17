import unittest
from unittest.mock import patch, MagicMock
from backend.datacollection.bookmakers.sts import get_data

class TestSts(unittest.TestCase):

    @patch("backend.datacollection.bookmakers.sts.requests.get")
    def test_get_data(self, mock_get):
        mock_html = """
        <html>
        <body>
            <div class="match-tile-event-details-teams__team match-tile-event-details-teams__team--1">Team A</div>
            <div class="match-tile-event-details-teams__team match-tile-event-details-teams__team--2">Team B</div>
            <span class="odds-button__odd-value ng-star-inserted">1</span>
            <span class="odds-button__odd-value ng-star-inserted">2</span>
            <span class="odds-button__odd-value ng-star-inserted">3</span>
            <bb-prematch-match-tile class="ng-star-inserted">
                <a href="/some-match-link"></a>
            </bb-prematch-match-tile>
        </body>
        </html>
        """
        mock_get.return_value = MagicMock(status_code=200, text=mock_html)

        result = get_data("link1")
        expected_result = [
            {
                "identifier": "Team A:Team B",
                "team1": "Team A",
                "team2": "Team B",
                "course1": "1",
                "courseX": "2",
                "course2": "3",
                "bts": 0,
                "nbts": 0,
            }
        ]
        self.assertEqual(result, expected_result)