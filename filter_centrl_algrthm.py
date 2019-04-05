import numpy as np
from location_and_klist import LOC_SATELLITES


def H_matrix(k_vec):
    """

    :param k_vec: k vector
    :return: H matrix  = [ I * exp(-j*(k dot r1),
                           I * exp(-j*(k dot r2),
                           I * exp(-j*(k dot r3),
                           I * exp(-j*(k dot r4)]
    """
    n_satellite = len(LOC_SATELLITES)
    H_mat = np.zeros([3 * n_satellite, 3], dtype=np.complex128)
    for i, loc in enumerate(LOC_SATELLITES):
        term = np.exp(-1j * np.dot(k_vec, loc))
        H_mat[i * 3 + 0, 0] = term
        H_mat[i * 3 + 1, 1] = term
        H_mat[i * 3 + 2, 2] = term
    return H_mat


dagger = lambda x: np.conj(x.T)
inv = np.linalg.inv
dot = np.dot
trace = np.trace


def P_value(H_mat, M_mat):
    temp = dagger(H_mat)  # = H_dagger
    temp = dot(temp, inv(M_mat))  # = H_dagger * M_inv
    temp = dot(temp, H_mat)  # = H_dagger * M_inv * H
    temp = inv(temp)  # = (H_dagger * M_inv * H)_inv
    try:
        return trace(temp)
    except:
        print(temp)
        return 0


if __name__ == '__main__':
    k_vector = (0.2, 0.2, 0.2)
    H = H_matrix(k_vector)
    print(H)

    from eingabe import input_data

    t_s, s_data = input_data()

    from M_matrices import build_M_matrices_list

    M_case = build_M_matrices_list(s_data)[15]

    import time

    start = time.time()
    print('P(k=(0.2,0.2,0.2))', P_value(H, M_case))
    k_vector = (-0.2, 0.2, 0.2)
    H = H_matrix(k_vector)
    print('P(k=(-0.2,0.2,0.2))', P_value(H, M_case))
    # It seems that we should use np.real(P)
    end = time.time()
    print('it takes', end - start, 'seconds to calculate a P value.')
