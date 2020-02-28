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
        print('FFT start point:',start_point)
        do_change_coordinate = False  # 改这里就好了改这里就好了改这里就好了改这里就好了改这里就好了
        if do_change_coordinate:
            # 下面几行是需要变换参考系，使得z朝向B_average的。
            transformed_data_this_interval = \
                coor_transform_Bavg_equals_Bz(all_sate_data[:, start_point:start_point + LEN_FFT])
            all_sate_data_partially_altered = all_sate_data.copy()
            all_sate_data_partially_altered[:, start_point:start_point + LEN_FFT] = transformed_data_this_interval
            # 上面这三行：只对需要的那个部分做参考系变化。
            fft_this_interval = fft_data.fft_all_satellite(all_sate_data=all_sate_data_partially_altered,
                                                           start_point=start_point)

            # 这下面一行呢，是不变换参考系的。
        else:
            fft_this_interval = fft_data.fft_all_satellite(all_sate_data=all_sate_data,
                                                           start_point=start_point)

            # 下面一行呢，是之前写的备注，体现出我的恐惧。
            # 这里改了一下，传进去的数据是：all_sate_data，其他地方不变，但是在start_point开始的一个LEN_FFT变换了参考系
            # 有点担心这个copy...

        for i in range(len(fft_this_interval)):
            result[i] += A_vec_to_M(np.array(fft_this_interval[i]))
            # calculate A*A.T.conj this line

        # run the next line at the end of one cycle
        start_point += LEN_MOVE_ONCE
        count += 1
    for i in range(len(fft_this_interval)):
        result[i] = result[i] / count
        # 除一下count做平均吧～
        # 20190713晚上添加。

    return result


if __name__ == '__main__':
    from eingabe import input_data_B_field

    t_s, s_data = input_data_B_field()

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
