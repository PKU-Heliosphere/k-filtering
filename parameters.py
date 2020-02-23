LEN_FFT = 4096
dt = 0.007813

LEN_DATA = 6144
LEN_MOVE_ONCE = 512
NUM_OF_OMEGAS = 75

BIG_NUM_OMEGAS = 320
# for the use of BIG_NUM_OMEGAS, see main_calc_4d_spectrum.py

##################################
# the case abandoned.

# LEN_FFT = 1024
# dt = 0.0625  # second(s)
# LEN_DATA = 4096-256  # 4096 for B field
# LEN_MOVE_ONCE = 256  # 256 for B field
# NUM_OF_OMEGAS = 73

##################################
if __name__ == '__main__':
    import numpy as np

    omega_list = 2 * np.pi * np.fft.rfftfreq(LEN_FFT, dt)[:BIG_NUM_OMEGAS]
    print(omega_list[0], omega_list[-1])
