import numpy as np
from matplotlib import pyplot as plt
from location_and_klist import get_k_list


def plot_ki_kj_plane_accumulated(ax, spectrum_4d, ki='kx', kj='ky'):
    accumulated_spec = spectrum_4d.sum(axis=0)  # add P values of different omegas.
    summing_axis = {('kx', 'ky'): 2, ('ky', 'kz'): 0, ('kx', 'kz'): 1}[(ki, kj)]
    spec_for_plot = accumulated_spec.sum(axis=summing_axis)

    k_list_dic = {'kx': kx_list, 'ky': ky_list, 'kz': kz_list}
    ax.pcolor(k_list_dic[kj], k_list_dic[ki], spec_for_plot)  # the ki_list is the same
    ax.set_xlabel(kj + '(km^-1)')
    ax.set_ylabel(ki + '(km^-1)')
    ax.set_title('P(' + ki + ',' + kj + '),omega accumulated')


def plot_ki_kj_plane_single_omega(ax, spectrum_one_omega, omega, ki='kx', kj='ky'):
    summing_axis = {('kx', 'ky'): 2, ('ky', 'kz'): 0, ('kx', 'kz'): 1}[(ki, kj)]
    spec_for_plot = spectrum_one_omega.sum(axis=summing_axis)

    k_list_dic = {'kx': kx_list, 'ky': ky_list, 'kz': kz_list}
    ax.pcolor(k_list_dic[kj], k_list_dic[ki], spec_for_plot)  # the ki_list is the same
    ax.set_xlabel(kj + '(km^-1)')
    ax.set_ylabel(ki + '(km^-1)')
    ax.set_title('P(' + ki + ',' + kj + '),omega =' + str(omega)[:5])


def plot_omega_ki_plane(ax, spectrum_4d, ki='kx'):
    summing_axis = {'kx': (3, 2), 'ky': (3, 1), 'kz': (1, 1)}[ki]
    spec_for_plot = spectrum_4d.sum(axis=summing_axis[0])
    spec_for_plot = spec_for_plot.sum(axis=summing_axis[1])

    k_list_dic = {'kx': kx_list, 'ky': ky_list, 'kz': kz_list}
    ax.pcolor(k_list_dic[ki], omega_list, spec_for_plot)
    ax.set_ylabel('omega(rad/s)')
    ax.set_xlabel(ki + '(km^-1)')
    ax.set_title('P(omega,' + ki + ')')


if __name__ == '__main__':
    spectrum_4d = np.load('spectrum_4d.npy')
    omega_list = 2 * np.pi * np.fft.rfftfreq(1024, 0.03125)[1:128]
    kx_list, ky_list, kz_list = get_k_list()[1:]
    '''
    figure, axes = plt.subplots(2, 3, figsize=(15, 10))
    plot_ki_kj_plane_accumulated(axes[0, 0], spectrum_4d[1:128], ki='kx', kj='ky')
    plot_ki_kj_plane_accumulated(axes[0, 1], spectrum_4d[1:128], ki='ky', kj='kz')
    plot_ki_kj_plane_accumulated(axes[0, 2], spectrum_4d[1:128], ki='kx', kj='kz')

    plot_omega_ki_plane(axes[1, 0], spectrum_4d[1:128], ki='kx')
    plot_omega_ki_plane(axes[1, 1], spectrum_4d[1:128], ki='ky')
    plot_omega_ki_plane(axes[1, 2], spectrum_4d[1:128], ki='kz')

    # axes[1, 0].plot([0, -0.2], [0, -0.2*-102], 'k-')
    # axes[1, 1].plot([0, -0.2], [0, -0.2*-94], 'k-')
    # axes[1, 2].plot([0, 0.2], [0, 0.2*19], 'k-')
    # 画出速度

    
    [-102.3152   -94.38133   18.816  ] [22.831957 18.871883 21.592825]
    [-102.02163  -93.91957   18.82654] [23.450603 19.106739 21.603088]
    [-102.23699   -94.21786    18.677534] [23.117826 19.140852 21.665476]
    [-102.55533   -94.41209    18.782299] [22.32191  18.927166 21.5276  ]
    

    plt.savefig('anisotropic_accumulated_and_dispersion_0513')
    plt.show()
    '''

    for i in range(63):
        my_figure, ax = plt.subplots()
        plot_ki_kj_plane_single_omega(ax, spectrum_4d[i], omega_list[i], ki='kx', kj='ky')
        plt.savefig('P_kx_ky_omega_' + str(omega_list[i])[:5] + '.png')
        plot_ki_kj_plane_single_omega(ax, spectrum_4d[i], omega_list[i], ki='ky', kj='kz')
        plt.savefig('P_ky_kz_omega_' + str(omega_list[i])[:5] + '.png')
        plot_ki_kj_plane_single_omega(ax, spectrum_4d[i], omega_list[i], ki='kx', kj='kz')
        plt.savefig('P_kx_kz_omega_' + str(omega_list[i])[:5] + '.png')
        print(i)

    # spec = spectrum_4d.sum(axis=1)
    # spec = spec.sum(axis=1)
    # spec = spec.sum(axis=1)
    # from fft_data import LEN_FFT, dt
    # omega_list = 2 * np.pi * np.fft.rfftfreq(1024, 0.03125)[:128]
    # plt.plot(omega_list, 2*spec ** 2/LEN_FFT*dt)
    # plt.semilogy()
    # plt.semilogx()
    # plt.xlabel('frequency(Hz)')
    # plt.ylabel('PSD(nT^2/Hz) * A CONSTANT')
    # plt.title('PSD power law test')
    # plt.savefig('power_law_test.png')
    # plt.show()
