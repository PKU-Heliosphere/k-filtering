import numpy as np

LOC = ((0, 0, 0),
       (-2.0136719, 13.878255, 0.5975749),
       (10.086589, 6.667318, 0.92631024),
       (3.0097656, 7.073568, -12.702515))
# Chris chen 2017 event.
n_k = 40


def get_k_list():
    k_max = 0.21

    kx_list = np.linspace(-k_max, k_max, n_k)
    ky_list = np.linspace(-k_max, k_max, n_k + 1)
    kz_list = np.linspace(-k_max, k_max, n_k - 1)

    k_list = list()

    for kx in kx_list:
        for ky in ky_list:
            for kz in kz_list:
                k_list.append((kx, ky, kz))

    # (kx1, ky1, kz1), (kx1, ky1, kz2), ...
    return k_list, kx_list, ky_list, kz_list


if __name__ == '__main__':
    print(get_k_list())
