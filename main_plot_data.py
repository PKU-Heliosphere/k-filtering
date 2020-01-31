import numpy as np
from matplotlib import pyplot as plt
from location_and_klist import get_k_list

kx_list, ky_list, kz_list = get_k_list()[1:]


def plot_ki_kj_plane_accumulated(ax, spectrum_4d, ki='kx', kj='ky'):
    accumulated_spec = spectrum_4d.sum(axis=0)  # add P values of different omegas.
    summing_axis = {('kx', 'ky'): 2, ('ky', 'kz'): 0, ('kx', 'kz'): 1}[(ki, kj)]
    spec_for_plot = accumulated_spec.sum(axis=summing_axis)

    k_list_dic = {'kx': kx_list, 'ky': ky_list, 'kz': kz_list}
    k_i, k_j = ki[0] + '_' + ki[1], kj[0] + '_' + kj[1]

    DO_LOG = False
    if DO_LOG:
        contour = ax.contourf(k_list_dic[kj], k_list_dic[ki], np.log(spec_for_plot))
        ax.set_title('$\\log{P}(' + k_i + ',' + k_j + ')$', fontsize=15)
    else:
        contour = ax.contourf(k_list_dic[kj], k_list_dic[ki], spec_for_plot)  # the ki_list is the same
        ax.set_title('${P}(' + k_i + ',' + k_j + ')$', fontsize=15)
    ax.set_xlabel('$' + k_j + '\\rm{(km^{-1})}$', fontsize=13)
    ax.set_ylabel('$' + k_i + '\\rm{(km^{-1})}$', fontsize=13)
    return contour


def plot_ki_kj_plane_single_omega(ax, spectrum_one_omega, omega, ki='kx', kj='ky'):
    summing_axis = {('kx', 'ky'): 2, ('ky', 'kz'): 0, ('kx', 'kz'): 1}[(ki, kj)]
    spec_for_plot = spectrum_one_omega.sum(axis=summing_axis)

    k_list_dic = {'kx': kx_list, 'ky': ky_list, 'kz': kz_list}
    pcolor_obj = ax.contourf(k_list_dic[kj], k_list_dic[ki], spec_for_plot)  # the ki_list is the same
    ax.set_xlabel(kj + '(km^-1)')
    ax.set_ylabel(ki + '(km^-1)')
    ax.set_title(
        'P_{E\'}/P{E}(' + ki + ',' + kj + ') \nat omega=' + str(omega)[:5] +
        'rad/s\n with integral at the other k_i' +
        ' direction')
    # \' = E + V cross B
    plt.colorbar(pcolor_obj, ax=ax)


def plot_omega_ki_plane_accumulated(ax, spectrum_4d, ki='kx'):
    summing_axis = {'kx': (3, 2), 'ky': (3, 1), 'kz': (1, 1)}[ki]
    spec_for_plot = spectrum_4d.sum(axis=summing_axis[0])
    spec_for_plot = spec_for_plot.sum(axis=summing_axis[1])

    k_list_dic = {'kx': kx_list, 'ky': ky_list, 'kz': kz_list}
    k_i = ki[0] + '_' + ki[1]
    DO_LOG = False
    if DO_LOG:
        contour = ax.contourf(k_list_dic[ki], omega_list, np.log(spec_for_plot))
        ax.set_title('$\\log{P}(\\omega ,' + k_i + ')$', fontsize=15)
    else:
        contour = ax.contourf(k_list_dic[ki], omega_list, spec_for_plot)
        ax.set_title('${P}(\\omega ,' + k_i + ')$', fontsize=15)
    ax.set_ylabel('$\\omega \\rm{(rad/s)}$', fontsize=13)
    ax.set_xlabel('$' + k_i + '\\rm{(km^{-1})}$', fontsize=13)
    return contour


if __name__ == '__main__':
    from parameters import dt, LEN_FFT, NUM_OF_OMEGAS, BIG_NUM_OMEGAS

    # NUM_OF_OMEGAS = BIG_NUM_OMEGAS
    #
    # spectrum_4d = np.load('modified_spectrum_4d_Eprime3.npy')
    # omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[1:NUM_OF_OMEGAS]
    # 74 rather than 75

    # spectrum_4d = np.load('spectrum_4d_B.npy')
    # omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:NUM_OF_OMEGAS]

    # spectrum_4d = np.load('spectrum_4d_E.npy')
    # omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:NUM_OF_OMEGAS]

    spectrum_4d = np.load('inplasma_spectrum_Eprime3.npy')
    omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[1:NUM_OF_OMEGAS]
    '''
    remember: the in-plasma spectrum doesn't have omega = 0.
    '''

    # spectrum_4d = np.load('spectrum_4d_Eprime3.npy')
    # omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:NUM_OF_OMEGAS]

    # spectrum_4d = np.load('spec_Epr_over_E_(modified).npy')
    # omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[1:NUM_OF_OMEGAS]

    figure, axes = plt.subplots(2, 3, figsize=(15, 9))
    plt.subplots_adjust(wspace=0.4, hspace=0.3)
    a = plot_ki_kj_plane_accumulated(axes[0, 0], spectrum_4d[:NUM_OF_OMEGAS], ki='kx', kj='ky')
    b = plot_ki_kj_plane_accumulated(axes[0, 1], spectrum_4d[:NUM_OF_OMEGAS], ki='ky', kj='kz')

    c = plot_ki_kj_plane_accumulated(axes[0, 2], spectrum_4d[:NUM_OF_OMEGAS], ki='kx', kj='kz')

    d = plot_omega_ki_plane_accumulated(axes[1, 0], spectrum_4d[:NUM_OF_OMEGAS], ki='kx')
    e = plot_omega_ki_plane_accumulated(axes[1, 1], spectrum_4d[:NUM_OF_OMEGAS], ki='ky')
    f = plot_omega_ki_plane_accumulated(axes[1, 2], spectrum_4d[:NUM_OF_OMEGAS], ki='kz')

    # plt.colorbar(a, ax=axes[0, 0], format='%.1e')
    # plt.colorbar(b, ax=axes[0, 1], format='%.1e')
    # plt.colorbar(c, ax=axes[0, 2], format='%.1e')
    # plt.colorbar(d, ax=axes[1, 0], format='%.1e')
    # plt.colorbar(e, ax=axes[1, 1], format='%.1e')
    # plt.colorbar(f, ax=axes[1, 2], format='%.1e')

    # plot the B-direction
    B_avg = [-2.7201579, 17.27789, 34.078583]
    zoom_rate = 300
    axes[0, 0].arrow(0, 0, B_avg[1] / zoom_rate, B_avg[0] / zoom_rate, color='r',width=0.005)
    axes[0, 1].arrow(0, 0, B_avg[2] / zoom_rate, B_avg[1] / zoom_rate, color='r',width=0.005)
    axes[0, 2].arrow(0, 0, B_avg[2] / zoom_rate, B_avg[0] / zoom_rate, color='r',width=0.005)

    plt.savefig('images/anisotropic_accumulated_and_dispersion')
    # plt.show()

    do_slices = input('input a \'y\' to start drawing slices of ki kj planes.\n')
    if do_slices == 'y':
        for i in range(NUM_OF_OMEGAS):
            my_figure, axis = plt.subplots()
            plot_ki_kj_plane_single_omega(axis, spectrum_4d[i], omega_list[i], ki='kx', kj='ky')
            plt.savefig('images/P_kx_ky_omega_' + str(omega_list[i])[:5] + '.png')

            my_figure, axis = plt.subplots()
            plot_ki_kj_plane_single_omega(axis, spectrum_4d[i], omega_list[i], ki='ky', kj='kz')
            plt.savefig('images/P_ky_kz_omega_' + str(omega_list[i])[:5] + '.png')

            my_figure, axis = plt.subplots()
            plot_ki_kj_plane_single_omega(axis, spectrum_4d[i], omega_list[i], ki='kx', kj='kz')
            plt.savefig('images/P_kx_kz_omega_' + str(omega_list[i])[:5] + '.png')
            print(i)
    else:
        print('don\'t receive a \'y\', now quit.')

    do_psd = input('input a \'y\' to start drawing PSD.\n')
    if do_psd == 'y':
        spec = spectrum_4d.sum(axis=1)
        spec = spec.sum(axis=1)
        spec = spec.sum(axis=1)
        from fft_data import LEN_FFT, dt

        omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:NUM_OF_OMEGAS]

        my_figure, axis = plt.subplots()
        plt.plot(omega_list, 2 * spec ** 2 / LEN_FFT * dt)
        plt.semilogy()
        plt.semilogx()
        plt.xlabel('omega(rad/s)')
        plt.ylabel('PSD(nT^2/Hz) * A CONSTANT')
        plt.title('PSD power law test')
        plt.savefig('images/power_law_test.png')
        # plt.show()
    else:
        print('don\'t receive a \'y\', now quit.')

'''
def plot_omega_kx_plane_with_kykz_fixed(ax, spectrum_4d, i_ky, i_kz):
    spec_for_plot = spectrum_4d[:, :, i_ky, i_kz]
    ax.pcolor(kx_list, omega_list, spec_for_plot)
    ax.set_ylabel('omega(rad/s)')
    ax.set_xlabel('kx(km^-1)')
    ax.set_title('P(omega, kx), ky=' + ky_list[i_ky] + 'kz=' + kz_list[i_kz])


def plot_omega_ky_plane_with_kxkz_fixed(ax, spectrum_4d, i_kx, i_kz):
    spec_for_plot = spectrum_4d[:, i_kx, :, i_kz]
    ax.pcolor(ky_list, omega_list, spec_for_plot)
    ax.set_ylabel('omega(rad/s)')
    ax.set_xlabel('ky(km^-1)')
    ax.set_title('P(omega, ky), kx=' + kx_list[i_kx] + 'kz=' + kz_list[i_kz])


def plot_omega_kz_plane_with_kxky_fixed(ax, spectrum_4d, i_kx, i_ky):
    spec_for_plot = spectrum_4d[:, i_kx, i_ky, :]
    ax.pcolor(kz_list, omega_list, spec_for_plot)
    ax.set_ylabel('omega(rad/s)')
    ax.set_xlabel('kz(km^-1)')
    ax.set_title('P(omega, kz), kx=' + kx_list[i_kx] + 'ky=' + ky_list[i_ky])
'''
