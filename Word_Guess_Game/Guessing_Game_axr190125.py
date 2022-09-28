import sys
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import random

def main():
    # Send the filename to the main program in a system argument.
    # If no system arg is present, print an error message and exit the program.
    if len(sys.argv) != 2:
        print("Error: Please enter the anat19.txt file as a sysarg.")
        exit()

    # Read the input file as raw text.
    with open('anat19.txt') as file:
        raw_text = file.read()

    # Calculate the lexical diversity of the tokenized text and output it, formatted to 2 decimal places.
    tokens = word_tokenize(raw_text)
    setT = set(tokens)
    ld = (len(setT) / len(tokens))
    print("\nThe Lexical Diversity is: %.2f" % (ld))

    # process the text; function returns (tokens, only_nouns)
    tokens, nouns = process_text(tokens)

    # make a dict of {noun:count of noun in tokens} items from the nouns and tokens lists
    dict = {}
    for nouns in tokens:
        dict[nouns] = tokens.count(nouns)

    # sort the dict by count and print the 50 most common words and their counts
    sorted_dict = sorted(dict.items(), key = lambda x : x[1], reverse = True)
    print("Most common words: ", sorted_dict[:50])

    # save the words to a list to use in guessing game
    most_common = sorted_dict[:50]                      # returns a list of tuples
    game_words = []                                     # create an empty list to store values in
    com_noun = map(lambda x: x[0], most_common)         # picking out the first value of the tuples
    for i in com_noun:
        game_words.append(i)                            # appending those values to the list

    # Start guessing game
    guessing_game(game_words)


def process_text(tokenized_text):
    # tokenize the lower-case raw text, reduce the tokens to only those that are alpha,
    # not in the NLTK stopword list, and have length > 5
    tokens = [t.lower() for t in tokenized_text if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]

    # lemmatize the tokens and use set() to make a list of unique lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    unique_lemmas = list(set(lemmas))

    # Do pos tagging on the unique lemmas and print the first 20 tagged items
    tags = nltk.pos_tag(unique_lemmas)
    print("First 20 tagged items: ", tags[:20])

    # create a list of lemmas (t[0]), for all the lemmas in the tags that are nouns
    only_nouns = list([lem[0] for lem in tags if lem[1].startswith("N")])

    # printing the total number of tokens and number of nouns
    print("Tokens: %d\n Nouns: %d" % (len(tokens), len(only_nouns)))

    # returning all the tokens (not unique tokens) and the nouns
    return tokens, only_nouns


def guessing_game(words):
    # Give the user 5 points to start with
    score = 5

    # game ends when total score is negative
    while True:
        word_to_guess = list(random.choice(words))
        # Randomly choose one of the 50 words in the top 50 list
        underscore = []
        # Printing intro and empty string
        intro = "\nLet's play a word guessing game!"
        outro = "Current score: "
        print(intro)
        print(' '.join(underscore))
        # Creating empty "string"
        for letters in word_to_guess:
            underscore.append('_')
        while score > -1:
            # Ask the user for a letter
            prompt = "Guess a letter: "
            users_guess = input(prompt)

            # User decides to quit game
            if users_guess == '!':
                print("Ending game\n", outro, score)
                quit()

            # If the letter is in the word, add 1 from their score, print ‘Right!’, followed by the updated string and get new input
            elif users_guess in word_to_guess:
                score += 1
                correct = "Right! Score is: "
                print(correct, score)
                counter = 0
                while counter < len(word_to_guess):
                    # check if user had tried this character before
                    if word_to_guess[counter] == users_guess:
                        underscore[counter] = users_guess
                        word_to_guess[counter] = '#'
                    counter += 1

            # If the letter is not in the word, subtract 1 from their score, print ‘Sorry, guess again’, followed by the updated string and get new input
            elif users_guess not in word_to_guess:
                score -= 1
                incorrect = "Sorry, guess again. Score is: "
                print(incorrect, score)

            # User guesses the word
            if not underscore.__contains__("_"):
                print("You solved it!\n", outro, score)
                break
        continue
    print("Game over\n", outro, score)
    quit()

if __name__ == "__main__":
    main()