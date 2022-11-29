import numpy as np
from matplotlib import pyplot as plt
from location_and_klist import get_k_list
from scipy.ndimage.filters import gaussian_filter

kx_list, ky_list, kz_list = get_k_list()[1:]

kdi_REPRESENT = False
d_i = 59
if kdi_REPRESENT:
    kx_list *= d_i
    ky_list *= d_i
    kz_list *= d_i


def plot_ki_kj_plane_accumulated(ax, spectrum_4d, ki='kx', kj='ky', field='B', save=False, savename='name',my_level=10,fixed_separation_level=0):
    accumulated_spec = spectrum_4d.sum(axis=0)  # add P values of different omegas.
    summing_axis = {('kx', 'ky'): 2, ('ky', 'kz'): 0, ('kx', 'kz'): 1}[(ki, kj)]
    spec_for_plot = accumulated_spec.sum(axis=summing_axis)

    k_list_dic = {'kx': kx_list, 'ky': ky_list, 'kz': kz_list}
    k_i, k_j = ki[0] + '_' + ki[1], kj[0] + '_' + kj[1]

    DO_LOG = True
    
    if DO_LOG:
        if fixed_separation_level:
            my_level = get_levels(np.log(spec_for_plot), fixed_separation_level)
        contour = ax.contourf(k_list_dic[kj], k_list_dic[ki], np.log(spec_for_plot), levels=my_level)
        ax.set_title('$\\log{P}_' + field + '(' + k_i + ',' + k_j + ')$ ', fontsize=12)
    else:
        if fixed_separation_level:
            my_level = get_levels(spec_for_plot, fixed_separation_level)
        contour = ax.contourf(k_list_dic[kj], k_list_dic[ki], spec_for_plot, levels=my_level)  # the ki_list is the same
        ax.set_title('$\\log{P}_' + field + '(' + k_i + ',' + k_j + ')$ ', fontsize=12)

    if kdi_REPRESENT:
        ax.set_xlabel('$' + k_j + 'd_\mathrm{i}$', fontsize=12)
        ax.set_ylabel('$' + k_i + 'd_\mathrm{i}$', fontsize=12)
    else:
        ax.set_xlabel('$' + k_j + '\\rm{(km^{-1})}$', fontsize=12)
        ax.set_ylabel('$' + k_i + '\\rm{(km^{-1})}$', fontsize=12)

    if save:
        np.save(savename, spec_for_plot)
    return contour

def plot_omega_ki_plane_accumulated(ax, spectrum_4d, ki='kx', ltype='contour', field='B'):
    summing_axis = {'kx': (3, 2), 'ky': (3, 1), 'kz': (1, 1)}[ki]
    spec_for_plot = spectrum_4d.sum(axis=summing_axis[0])
    spec_for_plot = spec_for_plot.sum(axis=summing_axis[1])

    k_list_dic = {'kx': kx_list, 'ky': ky_list, 'kz': kz_list}
    k_i = ki[0] + '_' + ki[1]
    DO_LOG = True
    if ltype == 'contour':
        sigma = 2  # this depends on how noisy your data is, play with it!
        spec_for_plot = gaussian_filter(spec_for_plot, sigma)
        if DO_LOG:
            contour = ax.contourf(k_list_dic[ki], omega_list, np.log(spec_for_plot), )
            ax.set_title('$\\log{P}_' + field + '(\\omega ,' + k_i + ')$', fontsize=12)
        else:
            contour = ax.contourf(k_list_dic[ki], omega_list, spec_for_plot, cmap=plt.get_cmap('Greens'))
            ax.set_title('${P}_' + field + '(\\omega ,' + k_i + ')$', fontsize=12)
    elif ltype == 'pcolor':
        if DO_LOG:
            contour = ax.pcolormesh(k_list_dic[ki], omega_list, np.log(spec_for_plot))
            ax.set_title('$\\log{P}_' + field + '(\\omega ,' + k_i + ')$', fontsize=12)
        else:
            contour = ax.pcolormesh(k_list_dic[ki], omega_list, spec_for_plot, cmap=plt.get_cmap('viridis'))
            ax.set_title('${P}_' + field + '(\\omega ,' + k_i + ')$', fontsize=12)
    if OMEGA_CI_PRESENT:
        ax.set_ylabel('$\\omega/\\omega_{ci}$', fontsize=12)
    else:
        ax.set_ylabel('$\\omega \\rm{(rad^{-1})}$', fontsize=12)
    if kdi_REPRESENT:
        ax.set_xlabel('$' + k_i + 'd_i$', fontsize=12)
    else:
        ax.set_xlabel('$' + k_i + '\\rm{(km^{-1})}$', fontsize=12)
    return contour

if __name__ == '__main__':
    from parameters import dt, LEN_FFT, NUM_OF_OMEGAS
    from location_and_klist import N_k

    print('dt =', dt, 'N_k =', N_k)
    omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:NUM_OF_OMEGAS]

    OMEGA_CI_PRESENT = False
    OMEGA_CI = 3.72
    if OMEGA_CI_PRESENT:  # remember: the in-plasma spectrum doesn't have omega = 0.
        omega_list /= OMEGA_CI

    spectrum_4d = np.load('spectrum_4d_simulated.npy')
    print(spectrum_4d.shape)
    
    figure, axes = plt.subplots(1, 3, figsize=(17,4))  # for my paper
    plt.subplots_adjust(wspace=0.4, hspace=0.3, left=0.12, right=0.88, top=0.85, bottom=0.15)

    plot_option = 'ki_kj'
    # plot_option = 'omega_ki'

    if plot_option == 'ki_kj':
        a = plot_ki_kj_plane_accumulated(axes[0], spectrum_4d, ki='kx', kj='ky')
        b = plot_ki_kj_plane_accumulated(axes[1], spectrum_4d, ki='ky', kj='kz')
        c = plot_ki_kj_plane_accumulated(axes[2], spectrum_4d, ki='kx', kj='kz')
    elif plot_option == 'omega_ki':
        a = plot_omega_ki_plane_accumulated(axes[0], spectrum_4d, ki='kx')
        b = plot_omega_ki_plane_accumulated(axes[1], spectrum_4d, ki='ky')
        c = plot_omega_ki_plane_accumulated(axes[2], spectrum_4d, ki='kz')
    else:
        raise TypeError('plot_option must be ki_kj or omega_ki.')

    plt.colorbar(a, ax=axes[0])
    plt.colorbar(b, ax=axes[1])
    plt.colorbar(c, ax=axes[2])
    axes[0].text(-11, -11, '(a)', color='white', fontsize=20)
    axes[1].text(-11, -11, '(b)', color='white', fontsize=20)
    axes[2].text(-11, -11, '(c)', color='white', fontsize=20)

    save_filename = {'ki_kj':'spectrum_4d_in_k_domain.png','omega_ki':'spectrum_4d_dispersion.png'}[plot_option]
    plt.savefig(save_filename,dpi=200)
    plt.show()

