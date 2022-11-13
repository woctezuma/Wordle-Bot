from scipy.stats import entropy

from src.disk_utils import load_pattern_dict


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
    all_words,
    num_chunks,
):
    entropies = {}
    for chunk_no in range(1, num_chunks + 1):
        pattern_dict = load_pattern_dict(chunk_no)

        candidates = set(pattern_dict)
        chunk_entropies = calculate_entropies(
            candidates,
            all_words,
            pattern_dict,
        )
        entropies.update(chunk_entropies)

    return entropies


def make_a_guess(
    all_words,
    num_chunks,
    verbose=True,
):
    entropies = calculate_entropies_in_chunks(
        all_words,
        num_chunks,
    )

    # Guess the candidate with the highest entropy
    guess_word, max_entropy = max(entropies.items(), key=lambda x: x[1])

    if verbose:
        print(f"Maximal entropy ({max_entropy}) reached with {guess_word}.")

    return guess_word, max_entropy
