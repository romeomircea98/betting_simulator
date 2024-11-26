import random
import logging
import matplotlib.pyplot as plt

logging.basicConfig(
    filename="betting_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"  
)

def kelly_criterion(odds_dict: dict, probabilities_dict: dict):
    """     
    Calculate the optimal bet size for each option using the Kelly Criterion.

    The Kelly Criterion is a formula used to determine the optimal bet size in scenarios with 
    known odds and probabilities. It is designed to maximize the growth of the bankroll by betting 
    more on favorable odds (i.e., value bets) and less on others. This implementation iterates 
    over each option in the odds and probability dictionaries, calculates the Kelly percentage 
    for each, and identifies which options represent value bets (i.e., where the Kelly percentage 
    is positive).

    :param odds_dict: A dictionary where keys are option names (e.g., teams, horses, etc.) and 
                      values are the odds assigned to each option by the bookmaker.
    :param probabilities_dict: A dictionary with matching keys to `odds_dict` where values represent 
                               the calculated probability of each option (e.g., from historical data 
                               or other analysis).
    :return: The Kelly percentage (rounded to 2 decimals) for the first option found to have a 
             positive expected value, along with the option's name and odds.

    Note: Only the first positive Kelly percentage is returned. If no value bet exists, 
    the function will return None.
    """
    for key in odds_dict:
        odd = odds_dict[key]
        probability = probabilities_dict[key]
        
        adjusted_odd = odd - 1
        losing_probability = 1 - probability
        kelly = round((adjusted_odd * probability - losing_probability) / adjusted_odd,2)
        
        if kelly > 0:
            return round(kelly,2), key, odd
             
    
def value_bet_generator(generated_odds, inflated_probability):
    """
    Generate adjusted probabilities for value betting based on given odds.
    
    This function calculates initial probabilities from provided odds and then randomly increases 
    the probability of one of the bets to simulate a value betting scenario. This "value bet" 
    option will have an inflated probability (by 0.05), indicating it has better-than-expected odds. 
    The function returns a dictionary of these adjusted probabilities.

    :param generated_odds: A dictionary where keys are option names (e.g., teams or horses) 
                            and values are their corresponding odds.
    :return: A dictionary where each key is an option name and each value is an adjusted probability 
             based on the odds, with one randomly selected option modified to simulate a value bet.
    
    Notes:
    - This function modifies one probability in the list, making the selected option a better choice 
      for value betting.
    """

    fraction = inflated_probability / 100
    probabilities = {key: round(1 / value, 3) for key, value in generated_odds.items()}
    

    random_key = random.choice(list(probabilities.keys()))
    random_probability = probabilities[random_key]

    random_odd_probability = round(random_probability + fraction, 3)
    probabilities[random_key] = random_odd_probability

    probabilities = {key: round(value, 3) for key, value in probabilities.items()}
    
    return probabilities

import random

def generate_odds(num_odds):
    """
    Generate a dictionary of betting odds simulating the reality of bookmakers by adding a 5% margin to each odds,
    which represents the expected value for bookmakers, i.e., their profit.

    :param num_odds: The total number of odds to generate.

    :return: A dictionary where keys are variant names and values are their corresponding odds.
    """
    num_large_odds = num_odds // 3
    num_medium_odds = num_odds // 3
    num_small_odds = num_odds - num_large_odds - num_medium_odds

    # Generate probabilities for each category
    large_probabilities = [random.uniform(0.5, 0.6) for _ in range(num_large_odds)]
    medium_probabilities = [random.uniform(0.3, 0.5) for _ in range(num_medium_odds)]
    small_probabilities = [random.uniform(0.1, 0.3) for _ in range(num_small_odds)]

    # Combine all probabilities
    probabilities = large_probabilities + medium_probabilities + small_probabilities

    # Normalize probabilities to sum up to slightly more than 1 (to simulate the bookmaker margin)
    total_probabilities = sum(probabilities)
    adjusted_probabilities = [(p / total_probabilities) * 1.05 for p in probabilities]

    # Generate odds dictionary
    odds_dict = {f"Variant {chr(65 + i)}": round(1 / p, 2) for i, p in enumerate(adjusted_probabilities)}

    return odds_dict


def get_number_of_variants():
    """
    Prompts the user to specify the number of betting options (variants) for the game.
    Keeps prompting until a valid integer is entered.

    Returns:
        int: The number of play variants chosen by the user.
    """
    while True:
        try:
            return int(input("How many play variants do you want? "))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def update_bankroll(bankroll, bet_size, bet, win):
    """
    Updates the user's bankroll based on the outcome of the bet.

    Parameters:
        bankroll (float): Current bankroll amount before placing the bet.
        bet_size (float): Amount of money bet.
        bet (float): Odds on the bet.
        win (bool): True if the bet was successful, False otherwise.

    Returns:
        float: The updated bankroll after the bet outcome.
    """
    if win:
        bankroll += (bet_size * (bet - 1))
        logging.info(f"Win! Gained: ${round(bet_size * (bet - 1), 2)}. New bankroll: ${round(bankroll, 2)}")
    else:
        bankroll -= bet_size
        logging.info(f"Lose. Lost: ${round(bet_size, 2)}. New bankroll: ${round(bankroll, 2)}")
    return bankroll

def determine_winner(variants_list, weights):
    """
    Randomly selects a winner from a list of variants based on the given weights.
    Weights represent the probability of each variant winning.

    Parameters:
        variants_list (list): List of possible betting outcomes.
        weights (list): List of probabilities corresponding to each outcome in variants_list.

    Returns:
        str: The chosen winner as a single element from variants_list.
    """
    return random.choices(list(variants_list), weights=weights, k=1)[0]