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
            [omega1: (Ax_image1, Ay_image1, Az_image1), omega2: (Ax_image2, Ay_image2, Az_image2), ...]
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
    num_of_omega = LEN_FFT // 2 + 1
    for one_sate_data in all_sate_data:
        Ax_fft, Ay_fft, Az_fft = fft_one_satellite_one_interval(one_sate_data, start_point=start_point)
        result.append(reformat_fft_result(Ax_fft, Ay_fft, Az_fft))
    # shape of result: 4(sates) * 513(omegas) * 3(components) now.

    for res_one_sate in result[1:]:
        for index in range(num_of_omega):
            result[0][index] += res_one_sate[index]
            # reshape to: 513(omegas) * 12(components).
            # 20190714note: the '+=' here implies the addition of tuples, which connect 2 tuples rather than
            #               add the components like that in the numpy array.
    return result[0]


if __name__ == '__main__':
    load_name = 'simulated_signal.npy'  # change this line to change the input file.
    s_data = np.load(load_name)

    import time

    start = time.time()

    fft_res = fft_one_satellite_one_interval(s_data[2])
    fft_power = [abs(fft) ** 2 for fft in fft_res]
    fft_real = [np.real(fft) for fft in fft_res]
    fft_img = [np.imag(fft) for fft in fft_res]
    omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:80]
    # check the power law of the spectrum

    a = fft_all_satellite(s_data)
    print(np.shape(a))

    end = time.time()
    print('it takes us', end - start, 'second(s) to do the whole fft, but we just do this once,\n'
                                      'so it may not be a time-consuming problem.')

    from matplotlib import pyplot as plt

    # plt.plot(omega_list, fft_power[0][:80], 'r')
    # plt.plot(omega_list, fft_power[1][:80], 'g')
    # plt.plot(omega_list, fft_power[2][:80], 'b')
    plt.plot(omega_list, fft_real[0][:80], 'r')
    plt.plot(omega_list, fft_real[1][:80], 'g')
    plt.plot(omega_list, fft_real[2][:80], 'b')
    plt.plot(omega_list, fft_img[0][:80], 'r', alpha=0.5)
    plt.plot(omega_list, fft_img[1][:80], 'g', alpha=0.5)
    plt.plot(omega_list, fft_img[2][:80], 'b', alpha=0.5)
    plt.xlabel('omega')
    plt.title('np.fft.rfft result | imaginary part being semi-transparent.')
    # plt.semilogy()
    # plt.semilogx()
    plt.show()
