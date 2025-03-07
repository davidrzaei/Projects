def main():
    # Ask for user input
    user_text = get_text()

    # Count words
    count_w = count_words(user_text)

    # Count letters
    count_l = count_letters(user_text)

    # Per 100 words
    L = calculate_L(count_l, count_w)

    # Count sentences
    count_s = count_sentences(user_text)

    # Per 100 words
    S = calculate_S(count_s, count_w)

    # Calculate using Index
    index = calculate_index(L, S)

    # Round to nearest int
    rounded_index = round_to_nearest_int(index)

    # Output grade level
    print_grade_level(rounded_index)


# Function to get user input text with at least one alphabetic character
def get_text():
    while True:
        text = input("Enter sample text here: ").strip()
        if text and any(c.isalpha() for c in text):
            return text


# Function to count the number of alphabetic characters in the text
def count_letters(text):
    return sum(1 for char in text if char.isalpha())


# Function to count the number of words in the text
def count_words(text):
    return len(text.split())


# Function to count the number of sentences in the text
def count_sentences(text):
    sentence_endings = ['.', '!', '?']
    return sum(1 for char in text if char in sentence_endings)


# Function to calculate letters per 100 words (L)
def calculate_L(letters, words):
    return (letters / words) * 100 if words != 0 else 0


# Function to calculate sentences per 100 words (S)
def calculate_S(sentences, words):
    return (sentences / words) * 100 if words != 0 else 0


# Function to calculate the Coleman-Liau index
def calculate_index(L, S):
    return 0.0588 * L - 0.296 * S - 15.8


# Function to round a float to the nearest integer
def round_to_nearest_int(value):
    return round(value)


# Function to print the corresponding grade level based on the index
def print_grade_level(index):
    if index < 1:
        print("Before Grade 1")
    elif 1 <= index <= 15:
        print(f"Grade {round(index)}")
    else:
        print("Grade 16+")


if __name__ == "__main__":
    main()
