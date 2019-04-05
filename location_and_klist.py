import numpy as np

LOC_SATELLITES = [(0, 0, 0),
                  (-3.375, -0.8046875, -7.274414),
                  (-5.90625, -3.8789062, -1.9326172),
                  (-5.09375, 1.1328125, -1.6254883)]
n_k = 40

def get_k_list():

    kx_list = np.linspace(-0.3,0.3,n_k)
    ky_list = np.linspace(-0.3,0.3,n_k)
    kz_list = np.linspace(-0.3,0.3,n_k)

    k_list = list()

    for kx in kx_list:
        for ky in ky_list:
            for kz in kz_list:
                k_list.append((kx, ky, kz))

    # (kx1, ky1, kz1), (kx1, ky1, kz2), ...
    return k_list,kx_list,ky_list,kz_list


if __name__ == '__main__':
    print(get_k_list())
