from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import sys
from functions_library import generate_odds, value_bet_generator, kelly_criterion, determine_winner, update_bankroll
import logging
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(current_dir, "icon.png")

logging.basicConfig(
    filename="betting_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"  
)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Betting Simulator")
        self.setContentsMargins(20, 20, 20, 20)

        self.bankroll = 0

        layout = QGridLayout()
        self.setLayout(layout)

        # Input labels
        bankroll_layout = QLabel("Choose a bankroll value: ")
        layout.addWidget(bankroll_layout, 0, 0)

        variants_layout = QLabel("How many play variants do you want?")
        layout.addWidget(variants_layout, 1, 0)

        fraction_layout = QLabel("What percentage of Kelly do you want to use? (10% - 100%): ")
        layout.addWidget(fraction_layout, 2, 0)

        bets_layout = QLabel("How many bets do you want to simulate?")
        layout.addWidget(bets_layout, 3, 0)

        probability_layout = QLabel("How much you want the inflated probability to be? (1% - 100%)")
        layout.addWidget(probability_layout, 4, 0)

        # Input fields (make them attributes of the class)
        self.input_bankroll = QLineEdit()
        layout.addWidget(self.input_bankroll, 0, 1)

        self.input_variants = QLineEdit()
        layout.addWidget(self.input_variants, 1, 1)

        self.input_fraction = QLineEdit()
        layout.addWidget(self.input_fraction, 2, 1)

        self.input_bets = QLineEdit()
        layout.addWidget(self.input_bets, 3, 1)

        self.probability_input = QLineEdit()
        layout.addWidget(self.probability_input, 4, 1)

        # Start button
        button1 = QPushButton("Start")
        layout.addWidget(button1, 5, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        # Connect button to function
        button1.clicked.connect(self.get_betting_data)

    def show_error_popup(self, message):
        """
        Displays a popup with an error message.

        :param message: The text of the message to display.
        """
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Eroare")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()

    def open_new_window(self):
        """
        Open a new window when the Start button is clicked.
        """
        self.new_window = NewWindow(self.bankroll_history, self.results_history)
        self.new_window.show()

    def select_kelly_fraction(self):
        """
        Prompt the user to select a fraction of the Kelly Criterion to use.
        """
        try:
            text = self.input_fraction.text().strip().replace('%', '')
            fraction = int(text)
            if 10 <= fraction <= 100:
                return fraction / 100
            else:
                self.show_error_popup("Please enter a number between 10 and 100.")
                return None
        except ValueError:
            self.show_error_popup("Invalid input. Please enter a number between 10 and 100.")
            return None

    def get_betting_data(self):
        """
        Simulates a series of bets using the Kelly Criterion, adjusting bet sizes based on optimal strategy.
        Logs transaction details for each bet (chosen variant, odds, bet size, winner, and bankroll before the bet).
        At the end of the simulation, it prints the initial and final bankroll, total wins and losses.
        Additionally, it generates plots showing bankroll evolution and win/loss statistics.

        Parameters:
            number_of_bets (int): The total number of bets to simulate during the session.

        Returns:
            None: This function prints results to the console, logs transaction details, and shows plots.
        """

        logging.info("Simulation started.")

        try:
            self.bankroll = int(self.input_bankroll.text().strip().replace('%', ''))
            if self.bankroll <= 0:
                self.show_error_popup("Bankroll must be a positive value.")
                return
        except (ValueError, AttributeError):
            self.show_error_popup("Invalid bankroll input. Please enter a numeric value.")
        self.initial_bankroll = self.bankroll
        try:
            number_of_variants = int(self.input_variants.text())
        except ValueError:
            self.show_error_popup("Invalid number of variants. Please enter a numeric value")
        try:
            kelly_fraction = self.select_kelly_fraction()
        except ValueError:
            self.show_error_popup("Invalid kelly fraction. Please enter a numeric value between 1 - 100")
        try:
            number_of_bets = int(self.input_bets.text())
        except ValueError:
            self.show_error_popup("Invalid number of bets. Please enter a numeric value")
        try:
            inflated_strip = self.probability_input.text().strip().replace('%', '')
            inflated_probability = int(inflated_strip)
            if not (1 <= inflated_probability <= 100):
                self.show_error_popup("Please enter a probability value between 1 and 100.")
                return
        except ValueError:
            self.show_error_popup("Invalid inflated probability. Please enter a numeric value")
            return
        wins = 0
        loses = 0
        self.bankroll_history = [self.bankroll]  # To track bankroll evolution
        self.results_history = []  # To track wins(1) and losses (0)

        for i in range(number_of_bets):
            try:
                odds = generate_odds(number_of_variants)
                probabilities = value_bet_generator(odds, inflated_probability)
            except:
                self.show_error_popup(f"An error occurred during odds generation: {str(e)}")
                return
            kelly = kelly_criterion(odds, probabilities)
            choice = kelly[1]
            bet_size = round(self.bankroll * (kelly[0] * kelly_fraction), 2)
            bet = odds[choice]
            winner = determine_winner(list(probabilities.keys()), list(probabilities.values()))
            if self.bankroll <= 1:
                bet_size = self.bankroll
            self.bankroll = update_bankroll(self.bankroll, bet_size, bet, choice == winner)
            
            # Update win/loss history
            if self.bankroll <= 0:
                self.show_error_popup("You run out of money")
                break
            if winner == choice:
                wins += 1
                self.results_history.append(1)
            else:
                loses += 1
                self.results_history.append(0)
            self.bankroll_history.append(self.bankroll)

            try:
                logging.info(
                f"Bet #{i + 1}: Chose {choice} with odds {bet}. "
                f"Bet size: ${bet_size}. Probability: {probabilities[choice]}. "
                f"Kelly: {kelly[0]}. Kelly Fraction: {kelly_fraction * 100}%. Winner: {winner}. "
                f"Bankroll before: ${round(self.bankroll, 2)}"
                )
            except IOError as e:
                self.show_error_popup(f"An error occurred during odds generation: {str(e)}")
                logging.error(f"Error during odds generation: {str(e)}")
                return
            
        logging.info(f"Simulation ended. Final bankroll: ${round(self.bankroll, 2)}")

        self.open_new_window()


class NewWindow(QWidget):
    def __init__(self, bankroll_history, results_history):
        super().__init__()
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Simulation Results")

        self.bankroll_history = bankroll_history
        self.results_history = results_history

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header label
        label = QLabel("Simulation Results")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignTop)

        # Matplotlib plot
        self.canvas = FigureCanvas(self.graph())
        layout.addWidget(self.canvas)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: yellow;
                color: black;
            }
            QPushButton:hover {
                background-color: rgb(255, 200, 0); /* Fundal la hover */
        """)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

    

    def graph(self):
        """
        Generate the matplotlib plot based on the passed data, with additional stats like
        bankroll increase and win/loss percentages.
        """
        fig, ax = plt.subplots(2, 1, figsize=(8, 5))

        ax[0].plot(range(len(self.bankroll_history)), self.bankroll_history, label="Bankroll", color="blue")
        ax[0].set_title("Bankroll Evolution Over Time")
        ax[0].set_xlabel("Number of Bets")
        ax[0].set_ylabel("Bankroll ($)")
        ax[0].grid(True)
        ax[0].legend()

        
        initial_bankroll = self.bankroll_history[0]
        final_bankroll = self.bankroll_history[-1]
        increase_percentage = ((final_bankroll - initial_bankroll) / initial_bankroll) * 100
        ax[0].text(0.14, 1.05, f"Bankroll Results: {increase_percentage:.2f}%", ha="center", va="center", transform=ax[0].transAxes)
        
        ax[0].text(0.86, 1.05, f"Final Bankroll: ${final_bankroll:.2f}", ha="center", va="center", transform=ax[0].transAxes)

        
        wins = sum(self.results_history)  
        losses = len(self.results_history) - wins  

        
        ax[1].bar(["Wins", "Losses"], [wins, losses], color=["green", "red"])
        ax[1].set_title("Wins and Losses")
        ax[1].set_xlabel("Result")
        ax[1].set_ylabel("Count")
        ax[1].grid(True)

        
        total_bets = len(self.results_history)
        win_percentage = (wins / total_bets) * 100
        loss_percentage = (losses / total_bets) * 100
        ax[1].text(0.14, 1.05, f"Win: {win_percentage:.2f}% / Loss: {loss_percentage:.2f}%", ha="center", va="center", transform=ax[1].transAxes)



        plt.tight_layout()

        return fig


app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: black;
        color: white;
    }
    QPushButton {
        background-color: yellow;
        color: black;
    }
    QPushButton:hover {
        background-color: rgb(255, 200, 0); /* Fundal la hover */
    }   
    QLineEdit { 
        border: 2px solid yellow; 
        border-radius: 5px; 
        padding: 5px;
        color: white;
        background-color: rgb(50, 50, 50);
    }
""")


window = Window()
window.show()
sys.exit(app.exec())
