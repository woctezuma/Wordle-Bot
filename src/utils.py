from src.chunk_utils import get_pattern
from src.pattern_utils import calculate_pattern


def update_possible_words(
    all_words,
    all_dictionary,
    guess_word,
    word_to_guess,
    verbose=True,
):
    info = calculate_pattern(guess_word, word_to_guess)

    if verbose:
        # Print round information
        print("Guessing:     ", guess_word)
        print("Info:         ", info)

    # Filter our list of remaining possible words
    words = get_pattern(all_dictionary, guess_word)[info]
    all_words = all_words.intersection(words)

    return all_words
