import argparse

from tqdm import tqdm

from src.cache_utils import pre_compute_patterns
from src.disk_utils import load_word_dictionary
from src.entropy_utils import divide_and_conquer
from src.utils import update_possible_words

N_GUESSES = 6
DATA_FOLDER = "data/"
GAME_NAMES = ["wordle", "dungleon"]
DICT_FILE_ALL = "guesses.txt"
DICT_FILE = "solutions.txt"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game-name",
        type=str,
        choices=GAME_NAMES,
        default="wordle",
        help="Game name",
    )
    parser.add_argument(
        "--first-guess",
        type=str,
        default=None,
        help="Pre-computed first guess",
    )
    args = parser.parse_args()

    game_folder = f"{args.game_name}/"
    fname_all_words = f"{DATA_FOLDER}{game_folder}{DICT_FILE_ALL}"
    fname_solutions = f"{DATA_FOLDER}{game_folder}{DICT_FILE}"

    # load all 5-letter-words for making patterns
    all_dictionary = load_word_dictionary(fname_all_words)

    num_chunks = pre_compute_patterns(all_dictionary)
    all_candidate_words = set(all_dictionary)

    # Load 2315 words for solutions
    dictionary = load_word_dictionary(fname_solutions)

    all_solutions = set(dictionary)

    # Simulate games
    precomputed_first_guess = args.first_guess

    for word_to_guess in tqdm(dictionary):
        remaining_candidate_words = all_candidate_words

        for n_round in range(N_GUESSES):
            if n_round == 0 and precomputed_first_guess is not None:
                guess_word = precomputed_first_guess
            else:
                remaining_solutions = remaining_candidate_words.intersection(
                    all_solutions,
                )

                guess_word, _ = divide_and_conquer(
                    remaining_candidate_words,
                    remaining_solutions,
                    num_chunks,
                )
                if n_round == 0:
                    precomputed_first_guess = guess_word

            if guess_word == word_to_guess:
                print(f"WIN IN {n_round + 1} GUESSES!")
                break

            # Filter our list of remaining possible words
            remaining_candidate_words = update_possible_words(
                remaining_candidate_words,
                all_dictionary,
                guess_word,
                word_to_guess,
            )


if __name__ == "__main__":
    main()
