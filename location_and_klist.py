import numpy as np
#
LOC_SATELLITES = [(0, 0, 0),
                  (-3.375, -0.8046875, -7.274414),
                  (-5.90625, -3.8789062, -1.9326172),
                  (-5.09375, 1.1328125, -1.6254883)]

# LOC_SATELLITES = [(0, 0, 0),
#                   (3.0625, -19.016928, 4.4580894),
#                   (10.0859375, 6.6783853, 0.9247233),
#                   (3.0065105, 7.0794272, -12.702393)]
# psr's event

n_k = 40


def get_k_list():
    # kx_list = np.linspace(-0.15, 0.15, n_k)
    # ky_list = np.linspace(-0.15, 0.15, n_k + 1)
    # kz_list = np.linspace(-0.15, 0.15, n_k - 1)
    # psr's event

    kx_list = np.linspace(-0.3, 0.3, n_k)
    ky_list = np.linspace(-0.3, 0.3, n_k + 1)
    kz_list = np.linspace(-0.3, 0.3, n_k - 1)

    k_list = list()

    for kx in kx_list:
        for ky in ky_list:
            for kz in kz_list:
                k_list.append((kx, ky, kz))

    # (kx1, ky1, kz1), (kx1, ky1, kz2), ...
    return k_list, kx_list, ky_list, kz_list


if __name__ == '__main__':
    print(get_k_list())
