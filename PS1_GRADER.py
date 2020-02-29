
MAX_POINTS = 8


def test_generatePattern(module, idx):
    expect = ['r', 'b', 'o', 'y']
    try:
        result = module.generatePattern()
        if result == expect:
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Function did not return the expected list, which was {}'.format(expect))
    except Exception as ex:
        return (0, 'Your code produced an error when we called the generatePattern function. The error was: {}'
                .format(ex))


def test_cleanGuess(module, idx):
    expect = ['r', 'g', 'r', 'v']
    try:
        result = module.cleanGuess(None)
        if result == expect:
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Function did not return the expected list, which was {}'.format(expect))
    except Exception as ex:
        return (0, 'Your code produced an error when we called the cleanGuess function. The error was: {}'
                .format(ex))


def test_guessIsValid(module, idx):
    expect = True
    try:
        result = module.guessIsValid(None)
        if result == expect:
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Expected the function to return True, but it returned {}'.format(result))
    except Exception as ex:
        return (0, 'Your code produced an error when we called the guessIsValid function. The error was: {}'
                .format(ex))


def test_evaluateGuess(module, idx):
    expect = [1, 1]
    try:
        result = module.evaluateGuess(None, None)
        if result == expect:
            return(GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Expected the function to return [1, 1], but it returned {}'.format(result))
    except Exception as ex:
        return (0, 'Your code produced an error when we called the evaluateGuess function. The error was: {}'
                .format(ex))


def test_playGame(module, idx):
    # The playGame() function reads from standard input (stdin), so to feed it our "guesses," we need to fake
    # some input. We can do this with StringIO.

    import sys
    from io import StringIO

    stdin = sys.stdin

    fake_input = StringIO('''1 a b c
    2 a b c
    3 a b c
    4 a b c
    5 a b c
    6 a b c
    7 a b c
    8 a b c
    9 a b c
    10 a b c
    ''')

    # Save stdin so we can put things back to normal
    sys.stdin = fake_input

    expect = 10
    try:
        result = module.playGame()

        # Restore stdin
        sys.stdin = stdin
    except Exception as ex:
        sys.stdin = stdin
        return (0, 'Your code produced an error when we called the playGame function. The error was: {}'
                .format(ex))

    if result == expect:
        return(GRADING_DATA[idx]['possiblePoints'], '')
    else:
        return(0, 'Expected to lose the game (return value of 10) after 10 guesses')


GRADING_DATA = [
    {
        'key': 'genpat',
        'area': 'generatePattern function',
        'testfunc': test_generatePattern,
        'possiblePoints': 1,
    },
    {
        'key': 'clean',
        'area': 'cleanGuess function',
        'testfunc': test_cleanGuess,
        'possiblePoints': 1,
    },
    {
        'key': 'valid',
        'area': 'guessIsValid function',
        'testfunc': test_guessIsValid,
        'possiblePoints': 1,
    },
    {
        'key': 'eval',
        'area': 'evaluateGuess function',
        'testfunc': test_evaluateGuess,
        'possiblePoints': 1,
    },
    {
        'key': 'play',
        'area': 'playGame function',
        'testfunc': test_playGame,
        'possiblePoints': 4,
    }
]
