import numpy as np

from parameters import LEN_FFT, dt


def fft_one_satellite_one_interval(part_data, start_point=0):
    """

    :param part_data: data from one satellite ONLY, cf. __main__ of this file
    :return: the FFT images
    """
    # Ax_avg, Ay_avg, Az_avg = part_data.T[:][start_point:start_point + LEN_FFT].mean(axis=0)
    Ax_avg = part_data.T[0][start_point:start_point + LEN_FFT].mean()
    Ay_avg = part_data.T[1][start_point:start_point + LEN_FFT].mean()
    Az_avg = part_data.T[2][start_point:start_point + LEN_FFT].mean()

    Ax_series = part_data.T[0][start_point:start_point + LEN_FFT] - Ax_avg
    Ay_series = part_data.T[1][start_point:start_point + LEN_FFT] - Ay_avg
    Az_series = part_data.T[2][start_point:start_point + LEN_FFT] - Az_avg

    Ax_fft = np.fft.rfft(Ax_series)
    Ay_fft = np.fft.rfft(Ay_series)
    Az_fft = np.fft.rfft(Az_series)
    # formerly used scipy.fft(), but negative omega makes no sense in our case.

    return Ax_fft, Ay_fft, Az_fft


def reformat_fft_result(Ax_fft, Ay_fft, Az_fft):
    """
    :return: reformatted data organized as
            [omega1: (Ax_image, Ay_image, Az_image), omega2: (Ax_image, Ay_image, Az_image), ...]
    """
    return list(zip(Ax_fft, Ay_fft, Az_fft))


def fft_all_satellite(all_sate_data, start_point=0):
    """
    build a list consist of A vectors of different omegas.
    :param all_sate_data: data from all satellites, cf. __main__ of this file
    :param start_point: reformatted fft result as
            [omega1: (Ax_image_1, Ay_image_1, Az_image_1, Ax_image_2, ..., Az_image_4),
             omega2: (Ax_image_1, Ay_image_1, Az_image_1, Ax_image_2, ..., Az_image_4),
             ...]
    :return:
    """
    result = list()
    num_of_omega = LEN_FFT // 2 + 1  # =1024/2+1
    for one_sate_data in all_sate_data:
        Ax_fft, Ay_fft, Az_fft = fft_one_satellite_one_interval(one_sate_data, start_point=start_point)
        result.append(reformat_fft_result(Ax_fft, Ay_fft, Az_fft))
    # shape of result: 4(sates) * 513(omegas) * 3(components) now.

    for res_one_sate in result[1:]:
        for index in range(num_of_omega):
            result[0][index] += res_one_sate[index]
            # add components from other 3 satellites to the first satellite,
            # so as to build shape: 513(omegas) * 12(components).
            # 20190714note: the '+=' here implies the addition of tuples, which connect 2 tuples rather than
            #               add the components like that in the numpy array.
    return result[0]


if __name__ == '__main__':
    from eingabe import input_data_B_field

    t_s, s_data = input_data_B_field()

    import time

    start = time.time()

    fft_res = fft_one_satellite_one_interval(s_data[0], start_point=1024)
    fft_power = [abs(fft) ** 2 for fft in fft_res]
    freqs = np.fft.rfftfreq(LEN_FFT, dt)
    # check the power law of the spectrum

    a = fft_all_satellite(s_data)
    print(np.shape(a))

    end = time.time()
    print('it takes us', end - start, 'second(s) to do the whole fft, but we just do this once,\n'
                                      'so it may not be a time-consuming problem.')

    from matplotlib import pyplot as plt

    plt.plot(freqs, fft_power[0], 'r.')
    plt.plot(freqs, fft_power[1], 'g.')
    plt.plot(freqs, fft_power[2], 'b.')
    plt.semilogy()
    plt.semilogx()
    plt.show()
