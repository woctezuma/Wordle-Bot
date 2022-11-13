from tqdm import tqdm

from src.cache_utils import pre_compute_patterns
from src.disk_utils import load_word_dictionary
from src.entropy_utils import calculate_entropies_in_chunks
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

    # Load 2315 words for solutions
    dictionary = load_word_dictionary(DICT_FILE)

    num_chunks = pre_compute_patterns(all_dictionary)

    # Simulate games
    precomputed_first_guess = FIRST_GUESS

    for word_to_guess in tqdm(dictionary):

        all_words = set(all_dictionary)

        if precomputed_first_guess is not None:
            all_words = update_possible_words(
                all_words,
                all_dictionary,
                precomputed_first_guess,
                word_to_guess,
            )
            init_round = 1
        else:
            init_round = 0

        for n_round in range(init_round, N_GUESSES):
            entropies = calculate_entropies_in_chunks(
                all_words,
                num_chunks,
            )

            # Guess the candiate with highest entropy
            guess_word = max(entropies.items(), key=lambda x: x[1])[0]

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
