from math import atan, pi, tan


student_coeff = 100
exp_res = 89.98980417737947


def calculate_error(test_res: float, exp_res: float) -> float:
    return abs(tan((test_res - exp_res) / exp_res * student_coeff))


def solve(exp_res: float, perc: float, n: int):
    if exp_res == 0:
        return ()
    arc_tan = atan(perc)
    if exp_res < 0:
        exp_res = - exp_res
    exp_res = exp_res
    lower = exp_res * (-arc_tan/student_coeff + 1)
    upper = exp_res * (arc_tan/student_coeff + 1)
    return ((lower, upper), (lower + 2 * pi * n, upper + 2 * pi * n))