from pathlib import Path

from src.chunk_utils import chunks, get_num_chunks
from src.disk_utils import get_pattern_dict_fname, save_pattern_dict
from src.pattern_utils import generate_pattern_dict


def pre_compute_patterns(all_dictionary):
    all_words = set(all_dictionary)
    num_chunks = get_num_chunks(all_dictionary)
    for chunk_no, dictionary_chunk in enumerate(chunks(all_dictionary), start=1):
        fname = get_pattern_dict_fname(chunk_no)
        print(f"[{chunk_no}/{num_chunks}] Processing {fname}")
        if not Path(fname).exists:
            # Calculate the pattern_dict and cache it
            pattern_dict = generate_pattern_dict(dictionary_chunk, all_words)
            save_pattern_dict(pattern_dict, chunk_no)

    return num_chunks
