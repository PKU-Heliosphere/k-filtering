import fft_data
import numpy as np

LEN_FFT = fft_data.LEN_FFT
LEN_DATA = 4096
LEN_OVERLAP = 256


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
    # print(np.shape(result))  # turns out to be (513, 12)
    start_point = 0
    while start_point + LEN_FFT < LEN_DATA:
        fft_this_interval = fft_data.fft_all_satellite(all_sate_data=all_sate_data,
                                                       start_point=start_point)
        # print('   ',fft_this_interval[0])
        for i in range(len(fft_this_interval)):
            result[i] += np.array(fft_this_interval[i])
        # print(result[0])

        # run the next line at the end of one cycle
        start_point += LEN_OVERLAP

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
    while start_point + LEN_FFT < LEN_DATA:
        fft_this_interval = fft_data.fft_all_satellite(all_sate_data=all_sate_data,
                                                       start_point=start_point)
        for i in range(len(fft_this_interval)):
            result[i] += A_vec_to_M(np.array(fft_this_interval[i]))
            # calculate A*A.T.conj this line

        # run the next line at the end of one cycle
        start_point += LEN_OVERLAP

    return result


if __name__ == '__main__':
    from eingabe import input_data

    t_s, s_data = input_data()

    # check the first function: accumulate_A_vectors()
    res = accumulate_A_vectors(s_data)
    print(np.shape(res))
    print('Want to check more details about this file, please uncomment those "print"s in the function above')

    import time

    start = time.time()
    res = build_M_matrices_list(s_data)
    print(np.shape(res))
    print(res[:1])
    end = time.time()
    print('It takes', end - start, 'second(s) to run the function: build_M_matrices_list() ')