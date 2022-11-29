LEN_FFT = 4096
dt = 0.007813  # for B brst, Eprime and interped E

LEN_DATA = 8064
LEN_MOVE_ONCE = 256
NUM_OF_OMEGAS = 80

if __name__ == '__main__':
    import numpy as np
    omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:NUM_OF_OMEGAS]
    print(omega_list[0], omega_list[-1])
