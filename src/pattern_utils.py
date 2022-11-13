from collections import Counter, defaultdict

from tqdm import tqdm


def calculate_pattern(guess, true):
    """Generate a pattern list that Wordle would return if you guessed
    `guess` and the true word is `true`
    Thanks to MarkCBell, Jeroen van der Hooft and gbotev1
    >>> calculate_pattern('weary', 'crane')
    (0, 1, 2, 1, 0)
    >>> calculate_pattern('meets', 'weary')
    (0, 2, 0, 0, 0)
    >>> calculate_pattern('rower', 'goner')
    (0, 2, 0, 2, 2)
    """
    wrong = [i for i, v in enumerate(guess) if v != true[i]]
    counts = Counter(true[i] for i in wrong)
    pattern = [2] * 5
    for i in wrong:
        letter = guess[i]
        if counts[letter] > 0:
            pattern[i] = 1
            counts[letter] -= 1
        else:
            pattern[i] = 0
    return tuple(pattern)


def generate_pattern_dict(dictionary, all_words=None):
    """For each word and possible information returned, store a list
    of candidate words
    >>> pattern_dict = generate_pattern_dict(['weary', 'bears', 'crane'])
    >>> pattern_dict['crane'][(2, 2, 2, 2, 2)]
    {'crane'}
    >>> sorted(pattern_dict['crane'][(0, 1, 2, 0, 1)])
    ['bears', 'weary']
    """
    if all_words is None:
        all_words = set(dictionary)
    pattern_dict = defaultdict(lambda: defaultdict(set))
    for word in tqdm(dictionary):
        for word2 in all_words:
            pattern = calculate_pattern(word, word2)
            pattern_dict[word][pattern].add(word2)
    return dict(pattern_dict)
