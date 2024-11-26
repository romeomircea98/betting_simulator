# Betting Simulation with PyQt6

This repository contains a betting simulation application built using Python and PyQt6. The application simulates a betting system with odds generation, value betting, and bankroll management, and provides an interactive interface for users to track their betting activities.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
  - [generate_odds](#generate_odds)
  - [value_bet_generator](#value_bet_generator)
  - [kelly_criterion](#kelly_criterion)
  - [determine_winner](#determine_winner)
  - [update_bankroll](#update_bankroll)
- [Testing](#testing)
- [License](#license)

---

## Overview

This project simulates betting scenarios with an interface where users can place bets, track their bankroll, and make decisions based on value betting. The core logic includes generating betting odds, applying the Kelly Criterion to calculate optimal bet sizes, and managing bankrolls based on betting outcomes.

The project is developed with a PyQt6 graphical user interface (GUI) to enhance user interaction, making the simulation more engaging and user-friendly.

---

## Features

- **Simulated Betting**: Generate betting odds and simulate bets based on probabilities and odds.
- **Value Betting**: Identify value bets by adjusting probabilities to favor specific outcomes.
- **Kelly Criterion**: Apply the Kelly Criterion to determine the optimal bet size based on the odds and the probability of an outcome.
- **Bankroll Management**: Track and update the user's bankroll after each bet based on the result.
- **Graphical Interface**: A simple but interactive interface built with PyQt6, allowing users to interact with the simulation.

---

## Technologies Used

- **Python 3.12**: The main programming language used.
- **PyQt6**: A toolkit for creating graphical user interfaces in Python.
- **UnitTest**: A Python module used for testing the application and its functions.
- **GitHub**: Version control and code hosting platform.

---

## Installation & Setup

### Option 1: Run the Application (Windows) using the EXE file
1. Download the application [from this link](https://drive.google.com/drive/folders/1dos0r9k5bp9mjHdyey5a1tu440w_cY4o?usp=drive_link).
2. Select all files and click download
3. Inside the downloaded files, there is "dist" file, there is the main file
4. Double-click the `.exe` file to launch the application.


## Usage

https://github.com/user-attachments/assets/737dd6e5-a221-466a-b423-309e8744da4f

1. Choose a bankroll value
2. How many play variants do you want?
  "How many betting variants would you like to create? Enter an integer representing the number of betting options you want to include (for example, 3 for 3 betting variants like 'Team A wins', 'Draw', or 'Team B wins' in a football match, for horse racing would be, 5 for 5 different horses)."**
3. What percentage of Kelly do you want to use? (10% - 100%)
  "Enter a percentage value (from 0 to 100) to indicate how much of the recommended Kelly bet size you wish to use. For example, if the Kelly Criterion suggests betting 10% of your bankroll, entering 100 means you’ll bet the full 10%. If you enter a lower percentage, like 50, you would bet only half of the recommended amount, which is a more conservative approach."**
4. How many bets do you want to simulate?
5. How much do you want the inflated probability to be? (1%-100%)
  "Enter a percentage value between 1% and 100% to specify how much you want to increase the probability of one of the betting options. This inflated probability will simulate a 'value bet' by making one of the options seem more favorable than it actually is. For example, if you enter 10%, the probability of one randomly chosen option will be increased by 10%, making it a better betting opportunity."

"The software automatically uses the Kelly Criterion to determine the optimal bet size for each option.

The Kelly Criterion is a mathematical formula designed to maximize your bankroll's growth by determining the ideal amount to bet on each wager. It helps you avoid betting too much on unfavorable odds or too little on value bets. By using this criterion, the software helps you manage your bankroll more efficiently, ensuring you bet proportionally based on the perceived edge or value of each betting option. This approach reduces the risk of losing your bankroll while allowing for optimal growth over time."
---

## Functions

### `generate_odds(num_odds)`
Generates a set of odds based on the number of odds requested. It simulates bookmaker odds with a margin to represent expected profit.

**Parameters:**
- `num_odds` (int): The number of odds to generate.

**Returns:**
- A dictionary with betting options and corresponding odds.

---

### `value_bet_generator(generated_odds, inflated_probability)`
Generates adjusted probabilities for value betting, simulating one bet with inflated probability (value bet).

**Parameters:**
- `generated_odds` (dict): A dictionary where keys are options (e.g., teams or horses) and values are the odds.
- `inflated_probability` (float): The probability by which one bet's probability is inflated to simulate a value bet.

**Returns:**
- A dictionary with options and adjusted probabilities.

---

### `kelly_criterion(odds_dict, probabilities_dict)`
Calculates the optimal bet size for each option using the Kelly Criterion. It helps maximize bankroll growth by betting more on favorable odds.

**Parameters:**
- `odds_dict` (dict): A dictionary of odds with options as keys.
- `probabilities_dict` (dict): A dictionary of calculated probabilities for each option.

**Returns:**
- A tuple containing the Kelly percentage, the option's name, and the odds for the first positive Kelly percentage.

---

### `determine_winner(variants_list, weights)`
Randomly selects a winner based on provided weights (probabilities). The function simulates the outcome of a bet.

**Parameters:**
- `variants_list` (list): A list of possible betting outcomes (e.g., teams, horses).
- `weights` (list): A list of probabilities corresponding to each outcome.

**Returns:**
- A string representing the selected winner.

---

### `update_bankroll(bankroll, bet_size, bet, win)`
Updates the user's bankroll based on the outcome of the bet. If the user wins, their bankroll increases based on the bet size and odds; if they lose, it decreases.

**Parameters:**
- `bankroll` (float): The current bankroll before the bet.
- `bet_size` (float): The amount of money being bet.
- `bet` (float): The odds on the bet.
- `win` (bool): Whether the bet was successful (True if won, False if lost).

**Returns:**
- A float representing the updated bankroll.

---

## Testing

This project includes unit tests for all major functions, ensuring that the core functionality of the application works as expected. The tests are located in the `test_simulation.py` file.

To run the tests:

1. Ensure you have installed the required dependencies.
2. Run the tests using the following command:

   ```bash
   python -m unittest test_simulation.py
   ```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Feel free to fork this repository and submit pull requests for improvements, fixes, or additional features. All contributions are welcome!

---

### Contact Information

If you have any questions or need help with the project, please feel free to open an issue or contact the project owner directly.

---
