import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from backend.algorithms.optimized_algorithm import predict_match_outcome


class TestPredictMatchOutcome(unittest.TestCase):

    @patch("joblib.load")
    def test_predict_match_outcome(self, mock_joblib_load):
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = np.array([[0.2, 0.3, 0.5]])

        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = [[0.1, 0.2, 0.3, 0.4, 0, 0, 0, 0]]

        mock_table = MagicMock()
        mock_table[["Team", "A", "B", "C", "D"]] = [
            {"Team": "Team A", "A": 10, "B": 5, "C": 7, "D": 3},
            {"Team": "Team B", "A": 6, "B": 4, "C": 8, "D": 6},
        ]

        mock_joblib_load.side_effect = [mock_model, mock_scaler, mock_table]


        result = predict_match_outcome("Team A", "Team B")

        self.assertEqual(result[0], "Team A:Team B")
        self.assertAlmostEqual(result[1], 0.5, places=2)
        self.assertAlmostEqual(result[2], 0.3, places=2)
        self.assertAlmostEqual(result[3], 0.2, places=2)

if __name__ == "__main__":
    unittest.main()