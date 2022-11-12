import pickle


def get_pattern_dict_fname(chunk_no=None):
    if chunk_no is None:
        suffix = ""
    else:
        suffix = f"_{chunk_no}"
    return f"pattern_dict{suffix}.p"


def load_pattern_dict(chunk_no=None):
    """Load the cache."""
    fname = get_pattern_dict_fname(chunk_no)
    with open(fname, "rb") as file:
        pattern_dict = pickle.load(file)
    return pattern_dict


def save_pattern_dict(pattern_dict, chunk_no=None):
    fname = get_pattern_dict_fname(chunk_no)
    with open(fname, "wb+") as file:
        pickle.dump(pattern_dict, file)


def load_word_dictionary(fname):
    with open(fname, encoding="utf8") as ifp:
        dictionary = list(map(lambda x: x.strip(), ifp.readlines()))
    if not is_valid_dictionary(dictionary):
        print("Dictionary contains words of different length.")
        raise AssertionError()

    return dictionary


def is_valid_dictionary(dictionary):
    num_lengths = len({len(x) for x in dictionary})
    return bool(num_lengths == 1)
