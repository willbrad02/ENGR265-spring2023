import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    pi_estimate = 0
    current_error = abs(pi_estimate - math.pi)

    while current_error > target_error:

        a = 1
        b = 1 / math.sqrt(2)
        t = 1 / 4
        p = 1

        for i in range(1, 10):
            a_temp = (a + b) / 2
            b_temp = math.sqrt(a * b)
            t_temp = t - (p * (math.pow((a - a_temp), 2)))
            p_temp = 2 * p

            a = a_temp
            b = b_temp
            t = t_temp
            p = p_temp

            print("Loop Iteration: ", i)

            #Updating pi estimate

            pi_estimate = (math.pow((a + b), 2)) / (4 * t)

    # change this so an actual value is returned
    return pi_estimate




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
