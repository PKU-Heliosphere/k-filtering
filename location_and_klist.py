LOC_SATELLITES = [(0, 0, 0),
                  (-3.375, -0.8046875, -7.274414),
                  (-5.90625, -3.8789062, -1.9326172),
                  (-5.09375, 1.1328125, -1.6254883)]


def get_k_list():
    n_k = 25
    kx_list = [x * 0.01 + 0.055 + 1e-8 for x in range(n_k)]
    ky_list = [y * 0.01 + 0.055 + 1e-8 for y in range(n_k)]
    kz_list = [z * 0.01 + 0.055 + 1e-8 for z in range(n_k)]

    k_list = list()

    for kz in kz_list:
        for ky in ky_list:
            for kx in kx_list:
                k_list.append((kx, ky, kz))

    # (kx1, ky1, kz1), (kx2, ky1, kz1), ...
    return k_list


if __name__ == '__main__':
    print(get_k_list())
