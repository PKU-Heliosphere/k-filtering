import numpy as np


def generate_random_polarity_l(num):
    theta_s = np.random.rand(num, 1) * np.pi
    phi_s = np.random.rand(num, 1) * np.pi * 2
    polarity_list = list()
    for i in range(num):
        theta = theta_s[i,0]
        phi = phi_s[i,0]
        polarity_list.append([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
        # (sin theta* cos phi, sin theta* sin phi, cos theta)
    return polarity_list

import numpy as np


class Wave:
    def __init__(self, amp, k_vec, omega, polarity, init_phase=0.0):
        self.k_vec = k_vec  # 1*3 np.array
        self.amp = amp  # scalar
        self.omega = omega  # scalar
        self.kx = k_vec[0]
        self.ky = k_vec[1]
        self.kz = k_vec[2]
        self.polarity = polarity  # 1*3 np.array normalized
        self.amp_vec = amp * polarity  # 1*3 np.array
        self.init_phase = init_phase  # scalar

    def signal(self, r, t, noise_level=0.3, background=None):
        phase = np.dot(self.k_vec, r) - self.omega * t + self.init_phase
        res_complex = self.amp_vec * (np.exp(1j * phase))
        if background is None:
            res_complex += np.array([1, 1, 1])
        noise_phase = np.random.rand(3) * 2 * np.pi
        noise = np.cos(noise_phase)
        # print(noise,type(noise),np.shape(noise),type(res_complex),np.shape(res_complex),res_complex)
        res_complex += noise * noise_level
        return np.real(res_complex)


class WavePacket:
    def __init__(self, wave_tuple=()):
        self.wave_list = list(wave_tuple)

    def add_wave(self, new_wave):
        self.wave_list.append(new_wave)

    def generate_signal_series_at_r(self, r, t_series):
        res = np.zeros((len(t_series), 3))
        for wave in self.wave_list:
            for i, t in enumerate(t_series):
                res[i, :] += wave.signal(r, t)
        return res

    def generate_signal_series_at_many_rs(self, rs_list, t_series):
        res = np.zeros((len(rs_list), len(t_series), 3))
        for i, r in enumerate(rs_list):
            for wave in self.wave_list:
                for j, t in enumerate(t_series):
                    res[i, j, :] += wave.signal(r, t)
        return res


if __name__ == '__main__':
    from parameters import LEN_DATA, dt
    from location_and_klist import LOC_SATELLITES
    from matplotlib import pyplot as plt

    k_wave_1 = np.array([0.1, 0.08, 0.05])
    k_wave_2 = np.array([-0.15, -0.12, -0.075])
    polarity_l = generate_random_polarity_l(4)
    my_wave_1 = Wave(1.0, k_wave_1, omega=11, polarity=np.array(polarity_l[0]),
                     init_phase=float(np.random.rand()) * 2 * np.pi)
    my_wave_2 = Wave(1.0, k_wave_2, omega=7.06, polarity=np.array(polarity_l[1]),
                     init_phase=float(np.random.rand()) * 2 * np.pi)
    print('Polarities:')
    for polarity in polarity_l:
        print(polarity)
    myWP = WavePacket((my_wave_1, my_wave_2,))

    t_s = np.array(range(LEN_DATA)) * dt
    signal_series = myWP.generate_signal_series_at_many_rs(LOC_SATELLITES, t_s)
    np.save('simulated_signal_by_wave_generator', signal_series)

    fig, ax = plt.subplots(4, 1, figsize=(8, 6))
    for i_ in range(4):
        ax[i_].plot(t_s, signal_series[i_])

    plt.show()
