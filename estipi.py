# Adam Rilatt
# 01 / 13 / 21
# Estimating Pi using a Monte Carlo method

from decimal import *
import math
import random

# math.pi holds 48 decimal places of precision
#print("%.48f" % math.pi)

'''
We define a circle with radius 1. The area of the circle, then, is pi. Inscribe
one-quarter of that circle within a square with side lengths 1 x 1. The area
of the square is 1, and the are of the quarter-circle is then pi / 4.

Now, start randomly placing points within the square using coordinates (0, 0)
through (1, 1). As more points are placed, the ratio of the points within the
quarter-circle to the total number of points in the square will approach pi / 4.
'''

# initializers
random.seed(82)
getcontext().prec = 48     # set decimal precision for Decimal()s
num_points = 10000           # how many points will be placed onto the grid
point_count = 0            # number of points already placed

# estimation
for i in range(num_points):

    # generate coordinates between (0, 0) and (1, 1)
    x = random.random()
    y = random.random()

    if (x ** 2) + (y ** 2) < 1:
        # point is within the quarter-circle
        point_count += 1


estimate = Decimal(4) * (Decimal(point_count) / Decimal(num_points))
error = abs(Decimal(100) * ((Decimal(math.pi) - estimate) / Decimal(math.pi)))
print("Estimate of pi: %.48f" % estimate)
print("True value:     %.48f" % Decimal(math.pi))
print("Error: %f%%" % error)
