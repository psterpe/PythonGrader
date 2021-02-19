MAX_POINTS = 2


def test_loan_payment(module, idx):
    expect = 566.14
    try:
        result = round(module.pmt(30000, 5, 60), 2)
        if result == expect:
            return GRADING_DATA[idx]['possiblePoints'], ''
        else:
            return 0, f'Function did not return the expected value, which was {expect}'
    except Exception as ex:
        return 0, f'Your code produced an error when we called the pmt function. The error was: {ex}'


GRADING_DATA = [
    {
        'key': 'pmt',
        'area': 'Loan payment calculation',
        'testfunc': test_loan_payment,
        'possiblePoints': 2,
    }
]
