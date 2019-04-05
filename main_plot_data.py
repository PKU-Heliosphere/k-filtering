import numpy as np
from matplotlib import pyplot as plt
from location_and_klist import get_k_list


def plot_ki_kj_plane_accumulated(ax,spectrum_4d, ki='kx', kj='ky'):
    accumulated_spec = spectrum_4d.sum(axis=0)  # add P values of different omegas.
    summing_axis = {('kx', 'ky'): 2, ('ky', 'kz'): 0, ('kx', 'kz'): 1}[(ki, kj)]
    spec_for_plot = accumulated_spec.sum(axis=summing_axis)
    ax.pcolor(kx_list, ky_list, spec_for_plot)  # the ki_list is the same
    ax.set_xlabel(ki + '(km^-1)')
    ax.set_ylabel(kj + '(km^-1)')
    ax.set_title('P(' + ki + ',' + kj + '),omega accumulated')


def plot_ki_kj_plane_single_omega(ax,spectrum_one_omega, omega, ki='kx', kj='ky'):
    pass


def plot_omega_ki_plane(ax,spectrum_4d, ki='kx'):
    summing_axis = {'kx': (3, 2), 'ky': (3, 1), 'kz': (1, 1)}[ki]
    spec_for_plot = spectrum_4d.sum(axis=summing_axis[0])
    spec_for_plot = spec_for_plot.sum(axis=summing_axis[1])
    ax.pcolor(kx_list, omega_list, spec_for_plot)
    ax.set_ylabel('omega(rad/s)')
    ax.set_xlabel(ki + '(km^-1)')
    ax.set_title('P(omega,' + ki + ')')


if __name__ == '__main__':
    spectrum_4d = np.load('spectrum 4d.npy')
    omega_list = 2*np.pi*np.fft.rfftfreq(1024, 0.0625)[1:256]
    kx_list, ky_list, kz_list = get_k_list()[1:]
    figure,axes = plt.subplots(2,3,figsize=(15,10))
    plot_ki_kj_plane_accumulated(axes[0,0],spectrum_4d, ki='kx', kj='ky')
    plot_ki_kj_plane_accumulated(axes[0,1],spectrum_4d, ki='ky', kj='kz')
    plot_ki_kj_plane_accumulated(axes[0,2],spectrum_4d, ki='kx', kj='kz')

    plot_omega_ki_plane(axes[1,0],spectrum_4d, ki='kx')
    plot_omega_ki_plane(axes[1,1],spectrum_4d, ki='ky')
    plot_omega_ki_plane(axes[1,2],spectrum_4d, ki='kz')

    plt.show()

