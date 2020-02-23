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
from filter_centrl_algrthm import H_matrix, P_value
import time


def calc_spectrum_4d():
    """
    Calculate P for each (omega, kx, ky, kz), and organize them into a numpy array.
    The shape of the array: num of omega * num of kx * num of ky * num of kz.
    :return: None.
    """
    from parameters import dt, LEN_FFT, NUM_OF_OMEGAS, BIG_NUM_OMEGAS

    # BIG_NUM_OMEGAS = NUM_OF_OMEGAS
    # BIG_NUM_OMEGAS is used to calculate P with many omegas so that one can then calculate P with omega_pl as the
    # independent variable.
    # if one want to use fewer omegas, just dis-comment 'BIG_NUM_OMEGAS = NUM_OF_OMEGAS'.

    s_data = np.load('Eprime2_brst_data.npy')  # change this line to change the input file.
    save_name = 'spectrum_4d'  # change this line to change the name of the saved file.

    M_mat_list = build_M_matrices_list(s_data)[:BIG_NUM_OMEGAS]

    k_list, kx_list, ky_list, kz_list = get_k_list()

    spectrum_4d = list()

    omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:BIG_NUM_OMEGAS]

    count = 1
    for omega, M_this_omega in zip(omega_list, M_mat_list):
        result = np.zeros((n_k, n_k + 1, n_k - 1), dtype=np.double)
        n = 0
        start = time.time()

        for i in range(n_k):
            for j in range(n_k + 1):
                for l in range(n_k - 1):
                    result[i, j, l] = np.real(P_value(H_matrix(k_list[n]), M_this_omega))  # calculate P
                    n = n + 1

        end = time.time()
        print('n k total = '+str(n)+ ', it takes', end - start, 'second(s) to calculate using this omega:',
              omega, '(' + str(count) + '/' + str(BIG_NUM_OMEGAS) + ')')
        spectrum_4d.append(result)
        count += 1

    spectrum_4d_array = np.array(spectrum_4d)
    np.save(save_name, spectrum_4d_array)


if __name__ == '__main__':
    calc_spectrum_4d()
