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
    try:
        temp = dot(temp, inv(M_mat))  # = H_dagger * M_inv
    except Exception as e:
        print(e)
        return 0
    temp = dot(temp, H_mat)  # = H_dagger * M_inv * H
    try:
        temp = inv(temp)  # = (H_dagger * M_inv * H)_inv
        return trace(temp)
    except Exception as e:
        print(e)
        return 0


def my_sigmoid(x):
    t = (x - 1 / 2) * 10
    return 1 / (1 + np.exp(-t)) + 1e-6


def P_value_MUSIC(H_mat, M_mat, cut_level=0, power_level=0, automode=0):
    temp = dagger(H_mat)
    try:
        M_eigenvalues, M_feature_vectors = np.linalg.eig(M_mat)
        lambda_max = np.max(np.abs(M_eigenvalues))
        normalized_lambdas = M_eigenvalues / lambda_max
        if cut_level:
            # the MUSIC method (cut certain eigenvalues), see (Narita, 2010. Wave vector...)
            normalized_lambdas[:cut_level] = 1
            normalized_lambdas[cut_level:] = 1e-5
        elif power_level:
            # the extended MUSIC method (use a power function), see (Narita, 2010. Wave vector...)
            normalized_lambdas *= np.abs(normalized_lambdas) ** (power_level - 1)
        elif automode:
            # my method, replace the step function in MUSIC method with a function like sigmoid
            # (in a sense) auto-adaptive
            normalized_lambdas = (1 - my_sigmoid(1 / normalized_lambdas) + 1e-6) * 100
        else:
            print('No mode received, return 0.')
            return 0
        pseudo_M_inv = dot(dot(M_feature_vectors, np.diag(1 / (normalized_lambdas))),
                           M_feature_vectors.T.conj())
        temp = dot(temp, pseudo_M_inv)
    except Exception as e:
        print(e)
        return 0
    temp = dot(temp, H_mat)  # = H_dagger * M_inv * H
    try:
        temp = inv(temp)  # = (H_dagger * M_inv * H)_inv
        return trace(temp)
    except Exception as e:
        print(e)
        return 0


if __name__ == '__main__':
    k_vector = (0.2, 0.2, 0.2)
    H = H_matrix(k_vector)
    print(H)

    s_data = np.load('simulated_signal.npy')

    from M_matrices import build_M_matrices_list

    M_case = build_M_matrices_list(s_data)[10]
    print(M_case.shape)

    import time

    start = time.time()
    print('P(k=(0.2,0.2,0.2))', P_value(H, M_case))
    print('P(k=(0.2,0.2,0.2))', P_value_MUSIC(H, M_case))
    k_vector = (-0.2, 0.2, 0.2)
    H = H_matrix(k_vector)
    print('P(k=(-0.2,0.2,0.2))', P_value(H, M_case))
    # It seems that we should use np.real(P)
    end = time.time()
    print('it takes', end - start, 'seconds to calculate a P value.')
