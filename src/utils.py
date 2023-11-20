import itertools

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
        print(f"Guessing word {guess_word} with feedback pattern {info}")

    # Filter our list of remaining possible words
    words = get_pattern(all_dictionary, guess_word)[info]
    return all_words.intersection(words)


def draw_sample(iterable):
    # Reference: https://stackoverflow.com/a/59841/376454
    return next(iter(iterable))


def get_all_patterns(word_len):
    # Generate the possible patterns of information we can get
    return list(itertools.product([0, 1, 2], repeat=word_len))
