#!/usr/bin/python
import os
from collections import defaultdict

from tqdm import tqdm

from src.chunk_utils import chunks, get_num_chunks, get_pattern
from src.disk_utils import (
    get_pattern_dict_fname,
    load_word_dictionary,
    save_pattern_dict,
)
from src.entropy_utils import calculate_entropies_in_chunks
from src.pattern_utils import calculate_pattern, generate_pattern_dict

N_GUESSES = 10
DATA_FOLDER = "data/"
GAME_FOLDER = "dungleon/"
DICT_FILE_ALL = f"{DATA_FOLDER}{GAME_FOLDER}guesses.txt"
DICT_FILE = f"{DATA_FOLDER}{GAME_FOLDER}solutions.txt"


def main():
    # load all 5-letter-words for making patterns
    all_dictionary = load_word_dictionary(DICT_FILE_ALL)

    # Load 2315 words for solutions
    dictionary = load_word_dictionary(DICT_FILE)

    print(f"Loaded dictionary with {len(all_dictionary)} words...")

    num_chunks = get_num_chunks(all_dictionary)
    for chunk_no, dictionary_chunk in enumerate(chunks(all_dictionary), start=1):
        fname = get_pattern_dict_fname(chunk_no)
        print(f"[{chunk_no}/{num_chunks}] Processing {fname}")
        if not os.path.exists(fname):
            # Calculate the pattern_dict and cache it
            pattern_dict = generate_pattern_dict(dictionary_chunk)
            save_pattern_dict(pattern_dict, chunk_no)

    # Simulate games
    defaultdict(list)
    precomputed_first_guess = "tares"

    for word_to_guess in tqdm(dictionary):

        all_words = set(all_dictionary)

        if precomputed_first_guess is not None:
            info = calculate_pattern(precomputed_first_guess, word_to_guess)
            words = get_pattern(all_dictionary, precomputed_first_guess)[info]
            all_words = all_words.intersection(words)
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
            info = calculate_pattern(guess_word, word_to_guess)

            # Print round information
            print("Guessing:     ", guess_word)
            print("Info:         ", info)
            if guess_word == word_to_guess:
                print(f"WIN IN {n_round + 1} GUESSES!\n\n\n")
                break

            # Filter our list of remaining possible words
            words = get_pattern(all_dictionary, guess_word)[info]
            all_words = all_words.intersection(words)


if __name__ == "__main__":
    main()
