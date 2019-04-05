"""
This is LinRonald's k-filtering project.
We used structured data of magnetic or electric field sampled by several satellites to calculate the
4 dimension spectrum of the wave in the space (omega, kx, ky, kz)

the structured data should be like:
[
[satellite one: (Ex1, Ey1, Ez1), (Ex2, Ey2, Ez2), ...],
[satellite two: (Ex1, Ey1, Ez1), (Ex2, Ey2, Ez2), ...],
...
]

My work started on March the 30th.

"""

import numpy as np
from location_and_klist import get_k_list, n_k
from M_matrices import build_M_matrices_list
from eingabe import input_data
from filter_centrl_algrthm import H_matrix, P_value
import time


def calc_spectrum_4d():
    """
    Calculate P for each (omega, kx, ky, kz), and organize them into a numpy array.
    The shape of the array: num of omega * num of kx * num of ky * num of kz.
    :return: None.
    """
    t_s, s_data = input_data()
    M_mat_list = build_M_matrices_list(s_data)[1:256]

    k_list, kx_list, ky_list, kz_list = get_k_list()

    spectrum_4d = list()

    for omega, M_this_omega in zip(omega_list, M_mat_list):
        result = np.zeros((n_k, n_k, n_k), dtype=np.double)
        n = 0
        start = time.time()

        for i in range(n_k):
            for j in range(n_k):
                for l in range(n_k):
                    result[i, j, l] = np.real(P_value(H_matrix(k_list[n]), M_this_omega))  # calculate P
                    n = n + 1

        end = time.time()
        print('n k total = ', n, 'it takes ', end - start, 'second(s) to calculate using this omega:', omega)
        spectrum_4d.append(result)

    spectrum_4d_array = np.array(spectrum_4d)
    np.save('spectrum 4d', spectrum_4d_array)


if __name__ == '__main__':
    calc_spectrum_4d()
