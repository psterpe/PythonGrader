
MAX_POINTS = 8


def test_evaluateGuess1(module, idx):
    try:
        #Test 1 - in Canvas
        cleanGuess = ['y','r','b','b']
        pattern = ['g','b','v','b']
        result1 = module.evaluateGuess(cleanGuess,pattern)
        result2 = module.evaluateGuess(pattern,cleanGuess)
        if (result1[0] == 1 and result1[1] == 1) or (result2[0] == 1 and result2[1] == 1):
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Function did not return correct output. Test Pattern: {}. Test Guess {}. Expected [1,1]'.format(pattern,cleanGuess) )

    except Exception as ex:
        return (0, 'Your code produced an error when we called the evaluateGuess function. The error was: {}'.format(ex))


def test_evaluateGuess2(module, idx):
    try:
        #Test 2 - in Canvas
        cleanGuess = ['y','g','g','r']
        pattern = ['g','b','v','b']
        result1 = module.evaluateGuess(cleanGuess,pattern)
        result2 = module.evaluateGuess(pattern, cleanGuess)
        if (result1[0] == 0 and result1[1] == 1) or (result2[0] == 0 and result2[1] == 1):
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Function did not return correct output. Test Pattern: {}. Test Guess {}. Expected [0,1]'.format(pattern,cleanGuess) )

    except Exception as ex:
        return (0, 'Your code produced an error when we called the evaluateGuess function. The error was: {}'.format(ex))


def test_evaluateGuess3(module, idx):
    try:
        #Test 3 in Canvas
        cleanGuess = ['y','b','b','g']
        pattern = ['g','b','v','b']
        result1 = module.evaluateGuess(cleanGuess,pattern)
        result2 = module.evaluateGuess(pattern,cleanGuess)
        if (result1[0] == 1 and result1[1] == 2) or (result2[0] == 1 and result2[1] == 2):
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Function did not return correct output. Test Pattern: {}. Test Guess {}. Expected [1,2]'.format(pattern,cleanGuess) )

    except Exception as ex:
        return (0, 'Your code produced an error when we called the evaluateGuess function. The error was: {}'.format(ex))


def test_evaluateGuess4(module, idx):
    try:
        #Test Case - New
        cleanGuess = ['b','b','b','v']
        pattern = ['g','b','v','b']
        result1 = module.evaluateGuess(cleanGuess,pattern)
        result2 = module.evaluateGuess(cleanGuess,pattern)
        if (result1[0] == 1 and result1[1] == 2) or (result2[0] == 1 and result2[1] == 2):
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Function did not return correct output. Test Pattern: {}. Test Guess {}. Expected [2,0]'.format(pattern,cleanGuess) )

    except Exception as ex:
        return (0, 'Your code produced an error when we called the evaluateGuess function. The error was: {}'.format(ex))


def test_evaluateGuess5(module, idx):
    try:
        #Test win scenario
        cleanGuess = ['g','b','v','b']
        pattern = ['g','b','v','b']
        result1 = module.evaluateGuess(cleanGuess,pattern)
        result2 = module.evaluateGuess(cleanGuess,pattern)
        if (result1[0] == 4 and result1[1] == 0) or (result2[0] == 4 and result2[1] == 0):
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Function did not return correct output. Test Pattern: {}. Test Guess {}. Expected [4,0]'.format(pattern,cleanGuess) )

    except Exception as ex:
        return (0, 'Your code produced an error when we called the evaluateGuess function. The error was: {}'.format(ex))


def test_evaluateGuess6(module, idx):
    try:
        #Test if function returns list or tuple
        cleanGuess = ['g','b','v','b']
        pattern = ['g','b','v','b']
        result = module.evaluateGuess(cleanGuess,pattern)
        if type(result) == list or type(result) == tuple:
            return (GRADING_DATA[idx]['possiblePoints'], '')
        else:
            return (0, 'Function did not return a list or tuple.')

    except Exception as ex:
        return (0, 'Your code produced an error when we called the evaluateGuess function. The error was: {}'.format(ex))


GRADING_DATA = [
    {
        'key': 'evalguess1',
        'area': 'evaluateGuess function - testing scenario',
        'testfunc': test_evaluateGuess1,
        'possiblePoints': 1,
    },
    {
        'key': 'evalguess2',
        'area': 'evaluateGuess function - testing scenario',
        'testfunc': test_evaluateGuess2,
        'possiblePoints': 1,
    },
    {
        'key': 'evalguess3',
        'area': 'evaluateGuess function - testing scenario',
        'testfunc': test_evaluateGuess3,
        'possiblePoints': 1,
    },
    {
        'key': 'evalguess4',
        'area': 'evaluateGuess function - testing scenario',
        'testfunc': test_evaluateGuess4,
        'possiblePoints': 2,
    },
    {
        'key': 'evalguess5',
        'area': 'evaluateGuess function - testing scenario',
        'testfunc': test_evaluateGuess5,
        'possiblePoints': 1,
    },
    {
        'key': 'evalguess6',
        'area': 'evaluateGuess function - testing return value',
        'testfunc': test_evaluateGuess6,
        'possiblePoints': 2,
    }
]

