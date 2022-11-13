from tqdm import tqdm

from src.cache_utils import pre_compute_patterns
from src.disk_utils import load_word_dictionary
from src.entropy_utils import make_a_guess
from src.utils import update_possible_words

N_GUESSES = 6
FIRST_GUESS = "tares"
DATA_FOLDER = "data/"
GAME_FOLDER = "wordle/"
DICT_FILE_ALL = f"{DATA_FOLDER}{GAME_FOLDER}guesses.txt"
DICT_FILE = f"{DATA_FOLDER}{GAME_FOLDER}solutions.txt"


def main():
    # load all 5-letter-words for making patterns
    all_dictionary = load_word_dictionary(DICT_FILE_ALL)

    num_chunks = pre_compute_patterns(all_dictionary)

    # Load 2315 words for solutions
    dictionary = load_word_dictionary(DICT_FILE)

    # Simulate games
    precomputed_first_guess = FIRST_GUESS

    for word_to_guess in tqdm(dictionary):

        all_words = set(all_dictionary)

        for n_round in range(N_GUESSES):
            if n_round == 0 and precomputed_first_guess is not None:
                guess_word = precomputed_first_guess
            else:
                guess_word = make_a_guess(
                    all_words,
                    num_chunks,
                )
                if n_round == 0:
                    precomputed_first_guess = guess_word

            if guess_word == word_to_guess:
                print(f"WIN IN {n_round + 1} GUESSES!\n\n\n")
                break

            # Filter our list of remaining possible words
            all_words = update_possible_words(
                all_words,
                all_dictionary,
                guess_word,
                word_to_guess,
            )


if __name__ == "__main__":
    main()
