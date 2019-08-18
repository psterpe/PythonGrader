AVAILABLE_COLORS = ('r', 'o', 'y', 'g', 'b', 'v')
PATTERN_SIZE = 4
MAX_GUESSES = 10

def playGame():
    pattern = generatePattern()
    numGuesses = 0

    while numGuesses < MAX_GUESSES:

        # Prompt user for guess and read it in. Check format of guess and, if format not valid, re-prompt.
        # Guess format is valid if, after all punctuation and whitespace are removed, only 4 letters remain AND
        # those letters are from the AVAILABLE_COLORS list. The guess should NOT be case-sensitive -- any mix of
        # upper and lower case is allowed.

        while True:
            guess = cleanGuess(input('Enter a guess: '))
            if not guessIsValid(guess):
                print('Guess not in valid format; please try again.')
            else:
                numGuesses += 1
                break

        result = evaluateGuess(pattern, guess)
        if result == [PATTERN_SIZE, 0]:
            print('Congratulations! You won in {} guesses! My pattern was {}'.format(numGuesses, pattern))
            return numGuesses
        else:
            print('Guess {:>2}:\nRight color and position: {}\nRight color, wrong position: {}\n'.format(numGuesses, result[0], result[1]))

    print('Aw...you\'re out of guesses. Game over! My pattern was {}'.format(pattern))
    return numGuesses

def generatePattern():
    # This is a stub for now. Just return a list of 1-character strings
    # that are valid color letters.
    return ['r', 'b', 'o', 'y']


def cleanGuess(g):
    # As a stub, we just return a list of color strings; it doesn't matter what list.
    return ['r', 'g', 'r', 'v']

def guessIsValid(glist):
    # Stub for now; just return a boolean.
    return True

def evaluateGuess(pattern, guess):
    return [1, 1]

if __name__ == '__main__':
    number_of_guesses = playGame()
    print('Game over after {} guesses'.format(number_of_guesses))

