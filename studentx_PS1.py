# Hypothetical solution to loan payment calculation problem

def pmt(pv, r, nper):
    # nper will be a number of months
    # r will be expressed as 5 to mean 5% annual interest; we need to divide by 100
    # and then by 12 so it is monthly
    r = r / 100 / 12

    numerator = r * pv
    denominator = 1 - (1 + r)**-nper
    return numerator / denominator
