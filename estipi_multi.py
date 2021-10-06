# Adam Rilatt
# 01 / 13 / 21
# Estimating Pi using a Monte Carlo method -- Multiprocessed

from decimal import *
import multiprocessing as mp
import math
import random
from time import perf_counter

# === Initializers ===

# total number of samples to run. higher is better, but takes longer.
NUM_POINTS = 1_000_000_000

# number of cores allotted to system. can utilize up to the maximum reported by
# your system. hyperthreaded or virtual cores will result in skewed time
# estimate, but will cause an overall speedup.
ALLOWED_CORES = 12

# re-seeds the RNG every number of samples, increasing entropy and hopefully
# resulting in a better approximation, but slightly increasing execution time.
# if None, one common seed is shared between all processes.
ENTROPY_MOD = 10_000
#ENTROPY_MOD = NUM_POINTS // ALLOWED_CORES    # re-seed once per core

def spray_points(n):
    '''
    Scatters n points on a grid and returns the number that fall within the
    inscribed quarter-circle.
    '''

    point_count = 0

    for i in range(n):

        if ENTROPY_MOD not in [0, None] and i % ENTROPY_MOD == 0:
            # re-seeding the RNG on a per-core basis introduces more entropy
            # into the approximation process, yielding a better result
            random.seed(None)

        # generate coordinates between (0, 0) and (1, 1)
        x = random.random()
        y = random.random()

        if (x ** 2) + (y ** 2) < 1:
            # point is within the quarter-circle
            point_count += 1

    return point_count

def sample_time(num_samples = 20):
    '''
    Runs a small number of point placements in order to estimate program
    execution time.

    NOTE: hyperthreading performance will be vastly overestimated.
    '''
    sample_t0 = perf_counter()
    _ = spray_points(num_samples)
    sample_t1 = perf_counter()
    time_per_iter = (sample_t1 - sample_t0) / num_samples
    return time_per_iter


if __name__ == "__main__":

    # set arbitrary-precision Decimal length
    getcontext().prec = 48

    # if ENTROPY_MOD not set, share a common seed between all processes
    if ENTROPY_MOD in [0, None]:
        random.seed(None)

    # estimate program execution time by timing a few samples
    time_per_iter = sample_time(num_samples = 100)
    #print("Time per sample: %.8fs" % time_per_iter)

    # take the max number of cores available and/or permissible so that the
    # total number of points can be divided evenly among the cores, plus
    # some leftovers that can be easily handled afterward
    num_cores     = min(ALLOWED_CORES, mp.cpu_count())
    iter_per_core = NUM_POINTS // num_cores
    leftovers     = NUM_POINTS % num_cores
    exec_time     = (iter_per_core + leftovers) * time_per_iter

    print(
    "Running %d points over %d cores (%d per core). Estimated %.3fs duration." %
    (NUM_POINTS, num_cores, iter_per_core, exec_time))

    # distribute points across cores and return num points within the
    # quarter-circle
    t0 = perf_counter()

    with mp.Pool(num_cores) as pool:
        ret = list(pool.map(spray_points, num_cores * [iter_per_core]))

    points_in_arc = sum(ret)

    if leftovers > 0:
        points_in_arc += spray_points(leftovers)

    t1 = perf_counter()

    # full estimate of pi
    estimate = Decimal(4) * (Decimal(points_in_arc) / Decimal(NUM_POINTS))
    actual   = Decimal(math.pi)
    error    = Decimal(100) * abs((estimate - actual) / actual)

    print("Run time:       %.3fs" % (t1 - t0))
    print("Estimate of pi: %.15f" % estimate)
    print("True value:     %.15f" % actual)
    print("Error:          %f%%"  % error)
