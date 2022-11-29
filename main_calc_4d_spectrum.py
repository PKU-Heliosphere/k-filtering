"""
This is LinRonald's k-filtering project.
We used structured data of magnetic or electric field sampled by several satellites to calculate the
4D spectrum of the wave in the space (omega, kx, ky, kz)

the structured data should be like:
[
[satellite one: (Ex1, Ey1, Ez1), (Ex2, Ey2, Ez2), ...],
[satellite two: (Ex1, Ey1, Ez1), (Ex2, Ey2, Ez2), ...],
...
]

This work started on March the 30th, 2019.

"""

import numpy as np
from location_and_klist import get_k_list, N_k
from M_matrices import build_M_matrices_list
from filter_centrl_algrthm import H_matrix, P_value, P_value_MUSIC
import time


def calc_spectrum_4d():
    """
    Calculate P for each (omega, kx, ky, kz), and organize them into a numpy array.
    The shape of the array: num of omega * num of kx * num of ky * num of kz.
    :return: None.
    """
    from parameters import dt, LEN_FFT, LEN_MOVE_ONCE, NUM_OF_OMEGAS

    load_name = 'simulated_signal_by_wave_generator.npy'  # change this line to change the input file.
    s_data = np.load(load_name)
    print('Data shape:', s_data.shape)
    save_name = 'spectrum_4d_simulated'  # change this line to change the name of the saved file (need no .npy suffix)

    M_mat_list = build_M_matrices_list(s_data)[:NUM_OF_OMEGAS]

    k_list, kx_list, ky_list, kz_list = get_k_list()

    spectrum_4d = list()

    omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:NUM_OF_OMEGAS]
    print('#PARAMETERS#')
    print('load_name =', load_name, '| save_name =', save_name)
    print('dt =', dt, '| LEN_FFT =', LEN_FFT, '| LEN_MOVE_ONCE =', LEN_MOVE_ONCE, '| numberOfOmegas =',
          NUM_OF_OMEGAS)

    count = 1
    for omega, M_this_omega in zip(omega_list, M_mat_list):
        result = np.zeros((N_k, N_k + 1, N_k - 1), dtype=np.double)
        n = 0
        start = time.time()

        for i in range(N_k):
            for j in range(N_k + 1):
                for l in range(N_k - 1):
                    result[i, j, l] = np.abs(
                        P_value_MUSIC(H_matrix(k_list[n]), M_this_omega, automode=1))  # calculate P
                    n = n + 1

        end = time.time()
        print('n k total = ' + str(n) + ', it takes', end - start, 'second(s) to calculate with omega =',
              omega, '(' + str(count) + '/' + str(NUM_OF_OMEGAS) + ')')
        spectrum_4d.append(result)
        count += 1

    spectrum_4d_array = np.array(spectrum_4d)
    np.save(save_name, spectrum_4d_array)


if __name__ == '__main__':
    calc_spectrum_4d()
