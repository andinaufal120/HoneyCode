import random


def randomize_whitespaces(string: str,
                          start_index: int = 0,
                          /,
                          *,
                          track: bool = False) -> tuple[str, list[int] | None]:
    """
    Add extra whitespace at random indexes for a given string.

    :param string: The string to be processed
    :param start_index: will not modify below this index
    :param track: the function will also track and return a list of modified indexes if set to True
    :return: processed string and a list of indexes if track set to True
    """
    preprocessed: list[str] = list(string)

    # Find whitespace indexes
    idx: list[int] = [i for i, char in enumerate(preprocessed) if char == " " and i >= start_index]
    # Pick indexes to modify at random
    to_modify: list[int] = random.choices(idx, k=random.randint(0, len(idx)))

    if to_modify:
        for i in to_modify:
            preprocessed[i] = "  "  # Insert a new space
    else:
        return (string, to_modify) if track else (string, None)  # return early when nothing is modified

    string = "".join(preprocessed)
    return (string, to_modify) if track else (string, None)
