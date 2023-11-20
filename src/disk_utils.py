import pickle


def get_pattern_dict_fname(chunk_no=None):
    suffix = f"_{chunk_no}" if chunk_no else ""
    return f"pattern_dict{suffix}.p"


def load_pattern_dict(chunk_no=None):
    """Load the cache."""
    fname = get_pattern_dict_fname(chunk_no)
    with open(fname, "rb") as file:
        return pickle.load(file)


def save_pattern_dict(pattern_dict, chunk_no=None):
    fname = get_pattern_dict_fname(chunk_no)
    with open(fname, "wb+") as file:
        pickle.dump(pattern_dict, file)


def load_word_dictionary(fname, verbose=True):
    with open(fname, encoding="utf8") as ifp:
        dictionary = [x.strip() for x in ifp.readlines()]
    if not is_valid_dictionary(dictionary):
        print("Dictionary contains words of different length.")
        raise AssertionError

    if verbose:
        print(f"Loaded dictionary {fname} with {len(dictionary)} words...")

    return dictionary


def is_valid_dictionary(dictionary):
    num_lengths = len({len(x) for x in dictionary})
    return bool(num_lengths == 1)
