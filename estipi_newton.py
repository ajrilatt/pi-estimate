# Adam Rilatt
# 02 / 03 / 21
# Approximation of Pi via Newton's Method

import decimal
import math

NUM_DIGITS = 3

# the function used to approximate pi. x = pi must be a root of the function.
FUNC = math.sin

# derivative of function above.
FUNC_D = math.cos

# an entry-point approximation of pi.
x = 3 * (10 ** NUM_DIGITS)

def num_decimals_accurate(approx, actual):
    '''
    Returns the number of decimal points to which the current Newton's method
    approximation agrees with the true value of pi.
    '''

    # remove '3.'
    approx = str(approx)[2:]
    actual = str(actual)[2:]

    t = 0
    for i, digit in enumerate(actual):
        if digit == approx[i]:
            t += 1
        else:
            break

    return t


if __name__ == "__main__":

    # get pi as a big integer
    pi = int(str(math.pi).replace('.', ''))

    for i in range(NUM_ITERATIONS):

        x -= FUNC(x) // FUNC_D(x)
        t = num_decimals_accurate(x, pi)

        print(f"Iteration {i}: pi = {round(x, 20)}, acc. to {t} places")
