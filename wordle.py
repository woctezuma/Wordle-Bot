#!/usr/bin/python
import itertools
import os
from collections import defaultdict

from tqdm import tqdm

from src.chunk_utils import chunks, get_num_chunks, get_pattern
from src.disk_utils import get_pattern_dict_fname, save_pattern_dict
from src.entropy_utils import calculate_entropies_in_chunks
from src.pattern_utils import calculate_pattern, generate_pattern_dict

N_GUESSES = 10
DATA_FOLDER = "data/"
GAME_FOLDER = "dungleon/"
DICT_FILE_ALL = f"{DATA_FOLDER}{GAME_FOLDER}guesses.txt"
DICT_FILE = f"{DATA_FOLDER}{GAME_FOLDER}solutions.txt"
SAVE_TIME = False


def main():
    # load all 5-letter-words for making patterns
    with open(DICT_FILE_ALL, encoding="utf8") as ifp:
        all_dictionary = list(map(lambda x: x.strip(), ifp.readlines()))

    # Load 2315 words for solutions
    with open(DICT_FILE, encoding="utf8") as ifp:
        dictionary = list(map(lambda x: x.strip(), ifp.readlines()))

    error_msg = "Dictionary contains different length words."
    assert len({len(x) for x in all_dictionary}) == 1, error_msg
    print(f"Loaded dictionary with {len(all_dictionary)} words...")
    word_len = len(all_dictionary[0])  # 5-letters

    # Generate the possible patterns of information we can get
    all_patterns = list(itertools.product([0, 1, 2], repeat=word_len))

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

    for word_to_guess in tqdm(dictionary):

        if SAVE_TIME:
            guess_word = "tares"
            all_words = set(all_dictionary)
            info = calculate_pattern(guess_word, word_to_guess)
            words = get_pattern(all_dictionary, guess_word)[info]
            all_words = all_words.intersection(words)
            init_round = 1
        else:
            all_words = set(all_dictionary)
            init_round = 0

        for n_round in range(init_round, N_GUESSES):
            entropies = calculate_entropies_in_chunks(
                all_words,
                all_patterns,
                num_chunks,
                filter_candidates=True,
            )

            if max(entropies.values()) < 0.1:
                entropies = calculate_entropies_in_chunks(
                    all_words,
                    all_patterns,
                    num_chunks,
                    filter_candidates=False,
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
