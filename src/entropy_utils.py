from scipy.stats import entropy

from src.chunk_utils import chunks
from src.disk_utils import load_pattern_dict

ENTROPY_CHUNK_SIZE = 25000


def calculate_entropies(words, possible_words, pattern_dict):
    """Calculate the entropy for every word in `words`, taking into account
    the remaining `possible_words`"""
    entropies = {}
    for word in words:
        counts = []
        for matches in pattern_dict[word].values():
            num_matches = len(matches.intersection(possible_words))
            counts.append(num_matches)
        entropies[word] = entropy(counts)
    return entropies


def calculate_entropies_in_chunks(
    words,
    possible_words,
    num_chunks,
):
    entropies = {}
    for chunk_no in range(1, num_chunks + 1):
        pattern_dict = load_pattern_dict(chunk_no)

        candidates = set(pattern_dict).intersection(words)
        chunk_entropies = calculate_entropies(
            candidates,
            possible_words,
            pattern_dict,
        )
        del pattern_dict
        entropies.update(chunk_entropies)

    return entropies


def make_a_guess(
    words,
    possible_words,
    num_chunks,
    verbose=True,
):
    entropies = calculate_entropies_in_chunks(
        words,
        possible_words,
        num_chunks,
    )

    # Guess the candidate with the highest entropy
    guess_word, max_entropy = max(entropies.items(), key=lambda x: x[1])

    if verbose:
        print(f"Maximal entropy ({max_entropy:.2f}) reached with {guess_word}.")

    return guess_word, max_entropy


def divide_and_conquer(
    words,
    possible_words,
    num_chunks,
    verbose=True,
):
    guess_word = None
    max_entropy = None

    for word_subset in chunks(list(words), length=ENTROPY_CHUNK_SIZE):

        subset_guess_word, subset_max_entropy = make_a_guess(
            word_subset,
            possible_words,
            num_chunks,
            verbose=False,
        )

        if max_entropy is None or max_entropy < subset_max_entropy:
            guess_word = subset_guess_word
            max_entropy = subset_max_entropy

    if verbose:
        print(f"Maximal entropy ({max_entropy:.2f}) reached with {guess_word}.")

    return guess_word, max_entropy
