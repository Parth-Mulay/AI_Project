"""A manually rewritten version of the word counting logic.

This file shows a slightly different style after understanding the first version.
"""


def count_words_in_note(note_text):
    """Return the number of words in a meeting note.

    Args:
        note_text (str): The meeting note content.

    Returns:
        int: The total number of words.
    """
    return len(note_text.split())


if __name__ == "__main__":
    note = "Summary of decisions and follow-up tasks"
    print(f"Word count: {count_words_in_note(note)}")
