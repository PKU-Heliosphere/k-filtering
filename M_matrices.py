import fft_data
import numpy as np
from parameters import LEN_FFT, LEN_DATA, LEN_MOVE_ONCE
from coor_transform import coor_transform_Bavg_equals_Bz


def accumulate_A_vectors(all_sate_data):
    """
    get a series of time depending A vectors by slipping our fft window, then accumulate (sum) them to ONE
    list consist of A vectors of different omegas .

    THIS FUNCTION IS FOR TEST, BUT WILL NOT BE USED IN THE MAIN PROGRAM.
    The function build_M_matrices_list() is based on this, check the difference between them.

    :param all_sate_data: data from all satellites.
    :return: summed fft result of different time sampled as
            [omega1: (Ax_image_1, Ay_image_1, Az_image_1, Ax_image_2, ..., Az_image_4),
             omega2: (Ax_image_1, Ay_image_1, Az_image_1, Ax_image_2, ..., Az_image_4),
             ...]
    """
    result = list()
    for i in range(LEN_FFT // 2 + 1):
        result.append(np.zeros(12, dtype='complex128'))
    # print(np.shape(result))  # (513, 12)
    start_point = 0
    while start_point + LEN_FFT < LEN_DATA:
        fft_this_interval = fft_data.fft_all_satellite(all_sate_data=all_sate_data,
                                                       start_point=start_point)
        for i in range(len(fft_this_interval)):
            result[i] += np.array(fft_this_interval[i])
        start_point += LEN_MOVE_ONCE

    return result


def A_vec_to_M(A_vec):
    # calculate M = A * A.T.conj
    A_copy = np.array([A_vec], dtype=A_vec.dtype).T
    A_dag = A_copy.T.conj()
    return A_copy * A_dag


def build_M_matrices_list(all_sate_data):
    """
    Get the M matrices which is the most important input in our k-filtering algorithm.
    :param all_sate_data: data from all satellites.
    :return: M matrices list of each omega.
    """
    result = list()
    for i in range(LEN_FFT // 2 + 1):
        result.append(np.zeros((12, 12), dtype='complex128'))
    start_point = 0
    count = 0
    while start_point + LEN_FFT < LEN_DATA:
        print('FFT start at point:', start_point)
        fft_this_interval = fft_data.fft_all_satellite(all_sate_data=all_sate_data,
                                                       start_point=start_point)

        for i in range(len(fft_this_interval)):
            result[i] += A_vec_to_M(np.array(fft_this_interval[i]))
            # calculate A*A.T.conj this line

        # run the next line at the end of one cycle
        start_point += LEN_MOVE_ONCE
        count += 1
    for i in range(len(fft_this_interval)):
        result[i] = result[i] / count
        # do average

    return result


if __name__ == '__main__':
    from parameters import LEN_FFT, dt

    load_name = 'simulated_signal.npy'  # change this line to change the input file.
    s_data = np.load(load_name)

    # check the first function: accumulate_A_vectors()
    res = accumulate_A_vectors(s_data)
    print(np.shape(res))
    print('Want to check more details about this file, please uncomment those "print"s in the function above')

    import time

    start = time.time()
    res = build_M_matrices_list(s_data)
    print(np.shape(res))
    end = time.time()
    print('It takes', end - start, 'second(s) to run the function: build_M_matrices_list() ')
    np.set_printoptions(precision=1, linewidth=256)
    omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)

    # mat_inv = np.linalg.inv
    import scipy.linalg

    mat_inv = scipy.linalg.inv

    see_num = 52
    MA = res[see_num]
    print(MA.dtype, res[0].dtype)
    MAinv = mat_inv(MA)
    print('M_A:\n', MA)
    print(np.linalg.det(MA), np.linalg.cond(MA), np.linalg.det(MAinv), np.linalg.cond(MAinv), np.finfo(MA.dtype).eps)
    print('==========\n{M_A}^-1\n', MAinv)
    print(omega_list[see_num])
    print('MA*MA^-1:\n', np.dot(MA, MAinv))
    print(np.linalg.inv(MAinv) - MA)
