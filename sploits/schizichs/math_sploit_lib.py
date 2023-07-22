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


# 102468.2291967225
if __name__ == '__main__':
    x = 0
    n = 0
    while x < exp_res + 100000 or abs(tan((x - exp_res) / exp_res * student_coeff)) >= 0.1:
        res = solve(exp_res, 0.1, n)
        n += 1
        x = res[1][1] + (res[0][1] - res[0][0]) / 2
        print(x)

    print(abs(tan((x - exp_res) / exp_res * student_coeff)) < 0.1)
