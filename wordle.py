from random import Random
from dataclasses import dataclass
import os

class Colours:
    """ANSI escape codes for coloured console output."""                                                                                                                          
    WHITE = '\33[37m'                                                                                                               
    PURPLE = '\033[95m'                                                                                                             
    RED = '\33[31m'                                                                                                                 
    GREEN = '\33[92m'                                                                                                               
    YELLOW = '\33[33m'

FILE_NAME_ALL_WORDS = "src/all_words.txt"
FILE_NAME_TARGET_WORDS = "src/target_words.txt"
 
CORRECT_COLOUR = Colours.GREEN
INCORRECT_COLOUR = Colours.RED
INCORRECT_PLACEMENT_COLOUR = Colours.YELLOW

ATTEMPTS_PER_WORD = 6

RANDOM_GEN = Random()


class InvalidGuessException(Exception):
    """Raised when a guess is not found in the list of valid words."""


@dataclass
class GuessResult:
    """Result of a guessed word.
    
    Attributes:
        placement: A list of colours letters indicating correctness.
        correct: True if the guess matches the target word, otherwise False
    """
    placement: list[str]
    correct: bool


class WordHolder:
    """Manage the target word and validate guesses.
    
    Args:
        all_words: List of all valid guessable words.
        target_words: List of words eligible to be chosen as the target.
    """

    def __init__(self, all_words, target_words):
        self._all_words = all_words
        self._target_words = target_words

        self._word = RANDOM_GEN.choice(self._target_words)
        # self._word = "spike"
        self._letters = get_letter_count(self._word)

    @property
    def target_word(self) -> str:
        """Return the chosen target word."""
        return self._word
    
    @property
    def all_words(self):
        """Return the list of all valid guessable words."""
        return self._all_words
    
    @property
    def target_words(self):
        """Return the list of all possible target words."""
        return self._target_words

    
    def guess_word(self, guess: str) -> GuessResult:
        """Check a guess against the target word.
        
        Args: 
            guess: The guessed word.

        Returns:
            GuessResult containing coloured placements and correctness flag.

        Raises:
            InvalidGuessException: If the guess is not allowed in the word list or incorrect length.
        """
        guess = guess.lower()

        if len(guess) != 5:
            raise InvalidGuessException("You need to guess a 5 letter word!")
        
        if guess not in self._all_words:
            raise InvalidGuessException("Your guess needs to be an actual word!")

        placements = []
        guessed_letters = {}
        wrong_letters = 0

        # Filling up guessed letters so correct letters take priority over incorrect placement letters
        for idx, letter in enumerate(guess):
            if letter != self._word[idx]:
                continue

            guessed_letters[letter] = guessed_letters.get(letter, 0) + 1

        for idx, letter in enumerate(guess):
            if letter == self._word[idx]:
                placements.append(colour_word(CORRECT_COLOUR, letter))
                continue

            wrong_letters += 1

            if guessed_letters.get(letter, 0) >= self._letters.get(letter, 0) or letter not in self._word :
                placements.append(colour_word(INCORRECT_COLOUR, letter))
                continue

            placements.append(colour_word(INCORRECT_PLACEMENT_COLOUR, letter))
            guessed_letters[letter] = guessed_letters.get(letter, 0) + 1

        return GuessResult(placements, wrong_letters == 0)


def colour_word(colour: str, word: str) -> str:
    """Wrap a word in the specific colour and reset the colour afterwards.
    
    Args:
        colour: The ANSI escape sequence for the colour.
        word: The word or letter to wrap.

    Returns: 
        A string with the colour codes applied.
    """
    return f"{colour}{word}{Colours.WHITE}"
    

def get_letter_count(word: str) -> dict[str, int]:
        """Returns a mapping of letters to their frequency in the word.
        
        Args:
            word: The word to count letters in.
        
        Returns:
            A dictionary mapping each letter to the number of times it appears.
        """
        letters = {}

        for letter in word:
            letters[letter] = letters.get(letter, 0) + 1
        
        return letters


def get_file_contents(name: str) -> list[str]:
    """Read all lines from a file and return them as a list of strings.

    Leading and trailing whitespace is stripped from each line.

    Args: 
        name: Path to the file.

    Returns: 
        A list of stripped lines from the file.
    """
    with open(name, encoding="utf-8") as f:
        return [i.strip() for i in f]


def play_wordle():
    """Run the wordle game loop until the user exits manually."""
    def write_screen(attempts: list[str]):
        """Render the game state to the console."""
        os.system('cls')
        print("Guess the 5 letter word!\n")
        print("Green  : in word and correct placement")
        print("Yellow : in word but incorrect placement")
        print("Red    : not in word\n")

        if len(attempts) == 0:
            return

        for idx, attempt in enumerate(attempts):
            print(f"{idx + 1}.", end=" ")
            for letter in attempt:
                print(letter, end=" ")
            print("")

        print("")

    while True:
        all_words = get_file_contents(FILE_NAME_ALL_WORDS)
        target_words = get_file_contents(FILE_NAME_TARGET_WORDS)

        current_word = WordHolder(all_words, target_words)
        guessed_words = []

        attempt_number = 0

        while True:
            if attempt_number >= ATTEMPTS_PER_WORD:
                input(f"\nYou have ran out of guesses. The word was '{current_word.target_word}'. Better luck next time!: ")
                break

            write_screen(guessed_words)

            guess = input(f"Guess {attempt_number + 1} / {ATTEMPTS_PER_WORD}: ")

            try:
                result = current_word.guess_word(guess)
            except InvalidGuessException as e:
                input(colour_word(Colours.RED, f"\n{e}: "))
                continue
            except Exception as e:
                raise e
            
            if result.correct:
                input("\nYou guessed the word correctly. Good work!: ")
                break

            guessed_words.append(result.placement)
            attempt_number += 1


if __name__ == '__main__':
    play_wordle()
