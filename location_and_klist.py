import numpy as np

LOC_SATELLITES = ((0., 0., 0.),
                  (-12.63475547, -1.83494033, 6.15835298),
                  (-5.7646454, 10.19749119, 3.15906013),
                  (-11.64747854, 2.69249175, -8.91394894))

N_k = 20
k_MAX = 0.21


def get_k_list():
    kx_list = np.linspace(-k_MAX, k_MAX, N_k)
    ky_list = np.linspace(-k_MAX, k_MAX, N_k + 1)
    kz_list = np.linspace(-k_MAX, k_MAX, N_k - 1)
    # trick: apply +1/-1 in ky/kz to help us guarantee the right match of ki and P(ki)

    k_list = list()

    for kx in kx_list:
        for ky in ky_list:
            for kz in kz_list:
                k_list.append((kx, ky, kz))

    # it will be like: (kx1, ky1, kz1), (kx1, ky1, kz2), ...
    return k_list, kx_list, ky_list, kz_list


if __name__ == '__main__':
    # show satellite configuration
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    color = ['k', 'orange', 'green', 'blue']
    for i, s in enumerate(LOC_SATELLITES_GSE):
        ax.scatter(s[0], s[1], s[2], label=str(i + 1), color=color[i], linewidth=10)
    ax.set_xlabel('$x$', fontsize=15)
    ax.set_ylabel('$y$', fontsize=15)
    ax.set_zlabel('$z$', fontsize=15)
    plt.legend()
    plt.show()
