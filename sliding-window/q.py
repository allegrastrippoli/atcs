import math
from random import randint


def get_exact_diameter(slist):

    maxValue = max(slist)
    minValue = min(slist)

    return maxValue - minValue


def insert(windowX, newpoint):
    if not windowX:
        windowX.append(newpoint)
    else:
        i = 0
        while i < len(windowX) and windowX[i] <= newpoint:
            windowX.pop(i)
        windowX.insert(0, newpoint)

    return windowX


def refine(epsilon, windowX, q1, x, q_index, y):

    if (1 + epsilon) * abs(q1 - x) >= abs(q1 - y):
        del windowX[q_index]

    return windowX


def compute_diameter(epsilon, windowX):
    if len(windowX) > 2:
        q1 = windowX[0]
        i = 1

        while i < len(windowX) - 1:
            windowX = refine(epsilon, windowX, q1, windowX[i - 1], i, windowX[i + 1])
            i += 1

    return windowX[-1] - windowX[0]


def get_approx_diameter(epsilon, source, window, window_size):

    if window_size < 1:
        return 1
    exact_window = []

    for point in source:
        window = insert(window, point)
        exact_window.append(point)

        if len(window) > window_size:
            window.pop()

        if len(exact_window) > window_size:
            exact_window.pop(0)

        if len(window) == window_size:
            print(
                f"{get_diameter(epsilon, window) = } | {get_exact_diameter(exact_window) = }"
            )


def main():
    epsilon = 0.1
    source = [randint(1, 9999) for i in range(100)]
    window = []
    window_size = 5

    get_approx_diameter(epsilon, source, window, window_size)


if __name__ == "__main__":
    main()
