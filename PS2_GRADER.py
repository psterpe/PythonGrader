MAX_POINTS = 8


def test_generatePattern1(module, idx):
    try:
        # test the function three times, ideally all three should be different if random
        result1 = module.generatePattern()
        result2 = module.generatePattern()
        result3 = module.generatePattern()
        if result1 != result2 or result1 != result3 or result2 != result3:
            return GRADING_DATA[idx]['possiblePoints'], ''
        else:
            return 0, 'Function did not return a randomly generated list.'
    except Exception as ex:
        return 0, 'Your code produced an error when we called the generatePattern function. The error was: {}'.format(ex)


def test_generatePattern2(module, idx):
    AVAILABLE_COLORS = ('r', 'o', 'y', 'g', 'b', 'v')
    try:
        # test the function to make sure that the list contains legal characters
        result = module.generatePattern()
        for color in result:
            if color not in AVAILABLE_COLORS:
                return 0, 'Function returned colors not in AVAILABLE_COLORS'
            return GRADING_DATA[idx]['possiblePoints'], ''
    except Exception as ex:
        return 0, 'Your code produced an error when we called the generatePattern function. The error was: {}'.format(ex)


def test_generatePattern3(module, idx):
    PATTERN_SIZE = 4

    try:
        result = module.generatePattern()
        if len(result) != PATTERN_SIZE:
            return 0, 'Function did not generate a pattern of length {}'.format(PATTERN_SIZE)
        return GRADING_DATA[idx]['possiblePoints'], ''
    except Exception as ex:
        return 0, 'Your code produced an error when we called the generatePattern function. The error was: {}'.format(ex)


def test_cleanGuess1(module, idx):
    try:
        # test function to see if it returns a list
        test = ''' r Y o G ,  '''
        result = module.cleanGuess(test)
        if not isinstance(result, list):
            return 0, 'Function did not return a list.'
        return GRADING_DATA[idx]['possiblePoints'], ''
    except Exception as ex:
        return 0, 'Your code produced an error when we called the cleanGuess function. The error was {}'.format(ex)


def test_cleanGuess2(module, idx):
    try:
        # test function to see if it returns only characters and lowercase
        test = ''' r Y o G ,  '''
        result = module.cleanGuess(test)
        for character in result:
            if not character.islower() or not character.isalpha() :
                return(0, 'Function did not return a list of lowercase letters.')
        return GRADING_DATA[idx]['possiblePoints'], ''
    except Exception as ex:
        return 0, 'Your code produced an error when we called the cleanGuess function. The error was {}'.format(ex)


def test_illegal(module, idx):
    try:
        test = ''' rgxzbo  '''
        expect = ['r','g','b','o']
        result = module.cleanGuess(test)
    except Exception as ex:
        return 0, 'Your code produced an error when we called the cleanGuess function. The error was {}'.format(ex)

    if result != expect:
        # cleanGuess didn't weed out illegal colors, so guessIsValid must do so by declaring the guess invalid
        try:
            result = module.guessIsValid(['r', 'g', 'b', 'x'])
            if result != False:
                return 0, 'You did not reject illegal colors either in cleanGuess or guessIsValid.'
            else:
                return GRADING_DATA[idx]['possiblePoints'], ''
        except Exception as ex:
            return 0, 'Your code produced an error when we called the guessIsValid function. The error was {}'.format(ex)

    return GRADING_DATA[idx]['possiblePoints'], ''


def test_guessIsValid1(module, idx):
    try:
        # Test only for length since instructions ask student to weed out illegal colors in cleanGuess
        test = ['r','b','y','o','g']
        expect = False
        result = module.guessIsValid(test)
        if result != expect:
            return 0, 'Function did not account for correct number of colors.'
        return GRADING_DATA[idx]['possiblePoints'], ''
    except Exception as ex:
        return 0, 'Your code produced an error when we called the guessIsValid function. The error was {}'.format(ex)


def test_guessIsValid2(module, idx):
    try:
        test = ['b','b','b','b']
        expect = True
        result = module.guessIsValid(test)
        if result == expect:
            return GRADING_DATA[idx]['possiblePoints'], ''
    except Exception as ex:
        return 0, 'Your code produced an error when we called the guessIsValid function. The error was {}'.format(ex)


GRADING_DATA = [
    {
        'key': 'genpat1',
        'area': 'generatePattern function - testing random generator',
        'testfunc': test_generatePattern1,
        'possiblePoints': 1,
    },
    {
        'key': 'genpat2',
        'area': 'generatePattern function - testing legal colors',
        'testfunc': test_generatePattern2,
        'possiblePoints': 1,
    },
    {
        'key': 'genpat3',
        'area': 'generatePattern function - testing length',
        'testfunc': test_generatePattern3,
        'possiblePoints': 1,
    },
    {
        'key': 'clean1',
        'area': 'cleanGuess function - testing return list',
        'testfunc': test_cleanGuess1,
        'possiblePoints': 1,
    },
    {
        'key': 'clean2',
        'area': 'cleanGuess function - testing return only lowercase characters',
        'testfunc': test_cleanGuess2,
        'possiblePoints': 1,
    },
    {
        'key': 'illegal_colors',
        'area': 'test that illegal colors are rejected either by cleanGuess or guessIsValid',
        'testfunc': test_illegal,
        'possiblePoints': 1,
    },
    {
        'key': 'valid1',
        'area': 'guessIsValid function - testing for length and legal characters',
        'testfunc': test_guessIsValid1,
        'possiblePoints': 1,
    },
    {
        'key': 'valid2',
        'area': 'guessIsValid function - test for expected cleaned guess',
        'testfunc': test_guessIsValid2,
        'possiblePoints': 1,
    }
]
