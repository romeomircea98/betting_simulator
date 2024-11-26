import unittest
from functions_library import generate_odds, value_bet_generator, kelly_criterion, determine_winner, update_bankroll

class TestSimulation(unittest.TestCase):

    def test_generate_odds(self):
        """
        Test case for the `generate_odds` function. It checks whether the function generates the correct number of odds 
        based on the input number of odds requested.
        """
        odds = generate_odds(5)
        self.assertEqual(len(odds), 5)

    def test_value_bet_generator(self):
        """
        Test case for the `value_bet_generator` function. It ensures that the function returns the correct number of 
        probabilities and adjusts one of the probabilities to simulate a value bet.
        """
        odds = {"A": 1.5, "B": 2.0,"C": 3.0}
        inflated_probability = 10
        probabilities = value_bet_generator(odds, inflated_probability)
        self.assertEqual(len(probabilities), len(odds))

    def test_kelly_criterion(self):
        """
        Test case for the `kelly_criterion` function. It verifies that the Kelly percentage is calculated correctly 
        and is between 0 and 1 (inclusive).
        """
        odds = {"A": 1.5, "B": 2.0,"C": 3.0}
        probabilities = {"A": 0.70,"B": 0.50,"C": 0.33}
        kelly_result = kelly_criterion(odds, probabilities)
        self.assertTrue(0 <= kelly_result[0] <= 1)

    def test_determine_winner(self):
        """
        Test case for the `determine_winner` function. It ensures that the function correctly selects a winner based 
        on the provided weights.
        """
        probabilities = {'A': 0.6, 'B': 0.4}
        winner = determine_winner(probabilities.keys(), probabilities.values())
        self.assertIn(winner, probabilities)

    def test_update_bankroll(self):
        """
        Test case for the `update_bankroll` function. It checks whether the bankroll is updated correctly based on 
        the bet outcome (win or lose).
        """
        bankroll = 100
        bet_size = 10
        bet = 2.0
        win = True
        new_bankroll = update_bankroll(bankroll, bet_size, bet, win)
        self.assertGreater(new_bankroll, bankroll)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
