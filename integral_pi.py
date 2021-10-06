# Adam Rilatt
# 15 March 2021
# Integral Approximation of Pi

'''
Darn it, I missed Pi Day! I can at least approximate pi using an integral
of a quarter-circle.
'''

import math
import multiprocessing as mp

def integral_pi(args):

    start = args[0]
    n = args[1]
    num_samples = args[2]

    # simpson's rule, we select even N
    if not n % 2:
        n += 1

    # first term of approximation is sqrt(1-Xj^2) @ Xj = 1,
    # last term evaluates to sqrt(0) and is ignored
    sum = 0
    if start == 0:
        sum += math.sqrt(1 - (1 / num_samples) ** 2)

    # subintervals awssigned to this worker
    for j in range(start, start + n + 1):

        if j % 2:
            coeff = 4
        else:
            coeff = 2

        # the final subinterval often comes out to -0.00, and to us that should
        # just mean 0. in this case we just ignore it: it's 0!
        try:
            sum += coeff * math.sqrt(1 - (j / num_samples) ** 2)
        except ValueError as e:
            pass

    return sum


def dispatch(num_samples, num_cores):

    samples_per_core = num_samples // num_cores
    start_dist = [(k * samples_per_core, samples_per_core, num_samples) for k in range(num_cores)]

    with mp.Pool(num_cores) as pool:
        ret = list(pool.map(integral_pi, start_dist))

    return (4 * sum(ret)) / (3 * num_samples)


if __name__ == "__main__":

    import time

    # error of 0.000016% with 100,000,000 subintervals, taking 35.37s on 1 core
    n = 500_000_000
    NUM_CORES = 12

    # ensure number of subintervals is divisible into the core count
    n += NUM_CORES - (n % NUM_CORES)

    t0 = time.time()
    approx = dispatch(n, NUM_CORES)
    duration = time.time() - t0
    actual = math.pi

    print("Approximation: %.16f" % approx)
    print("        Error: %.16f%%" % abs(((approx - actual) / actual) * 100))
    print("     Run Time: %.6fs" % duration)
