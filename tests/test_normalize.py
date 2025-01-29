import unittest
from unittest.mock import patch, MagicMock, mock_open
from backend.datacollection.bookmakers.normalize import (
    normalize_team_name,
    normalize_identifier,
)


class TestNormalize(unittest.TestCase):

    def test_normalize_team_name(self):
        self.assertEqual(normalize_team_name("Nottingham Forest"), "Nott'm Forest")
        self.assertEqual(normalize_team_name("Manchester Utd"), "Man United")
        self.assertEqual(normalize_team_name("Manchester City"), "Man City")
        self.assertEqual(normalize_team_name("Wolverhampton"), "Wolves")
        self.assertEqual(normalize_team_name("Chelsea"), "Chelsea")

    def test_normalize_identifier(self):
        self.assertEqual(
            normalize_identifier("Nottingham Forest:Chelsea"), "Nott'm Forest:Chelsea"
        )
        self.assertEqual(
            normalize_identifier("Manchester Utd:Liverpool"), "Man United:Liverpool"
        )
        self.assertEqual(
            normalize_identifier("Manchester City:Wolves"), "Man City:Wolves"
        )
        self.assertEqual(
            normalize_identifier("Wolverhampton:Arsenal"), "Wolves:Arsenal"
        )
        self.assertEqual(normalize_identifier("Chelsea:Tottenham"), "Chelsea:Tottenham")
