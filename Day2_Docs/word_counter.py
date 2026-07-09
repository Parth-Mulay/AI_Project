"""Count words in a meeting note.

This utility demonstrates a simple function for the AI Meeting Notes Manager.
"""


def count_words_in_note(note_text):
    """Count the number of words in a meeting note string.

    Args:
        note_text (str): The meeting note content.

    Returns:
        int: The number of words in the note.
    """
    words = note_text.split()
    return len(words)


if __name__ == "__main__":
    sample_note = "Discussed roadmap launch timeline and action items"
    word_count = count_words_in_note(sample_note)
    print(f"Word count: {word_count}")
