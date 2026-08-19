import numpy as np

def check_simple_exposure_region(initialc10,ratio,lines_between):

    black_x, black_y = lines_between[0][0:50000], lines_between[1][0:50000]
    blue_x, blue_y = lines_between[0][50000:100000], lines_between[1][50000:100000]

    black_order = np.argsort(black_x)
    blue_order = np.argsort(blue_x)
    black_x_sorted, black_y_sorted = np.array(black_x)[black_order], np.array(black_y)[black_order]
    blue_x_sorted, blue_y_sorted = np.array(blue_x)[blue_order], np.array(blue_y)[blue_order]

    inside_x, inside_y = [], []
    outside_x, outside_y = [], []

    lower_bound = np.interp(initialc10, black_x_sorted, black_y_sorted)
    upper_bound = np.interp(initialc10, blue_x_sorted, blue_y_sorted)

    lo, hi = min(lower_bound, upper_bound), max(lower_bound, upper_bound)

    if lo <= ratio <= hi:
        inside_x.append(initialc10)
        inside_y.append(ratio)
        check = True

    elif ratio <= lo:
        inside_x.append(initialc10)
        inside_y.append(ratio)
        check = True
    else:
        outside_x.append(initialc10)
        outside_y.append(ratio)

        check = False

    return check
