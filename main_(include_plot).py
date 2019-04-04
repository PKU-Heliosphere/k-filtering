"""
This is LinRonald's k-filtering project.
We used structured data of magnetic or electric field sampled by several satellites to calculate the
4 dimension spectrum of the wave in the space (omega, kx, ky, kz)

the structured data should be like:
[
[satellite one: (Ex1, Ey1, Ez1), (Ex2, Ey2, Ez2), ...],
[satellite two: (Ex1, Ey1, Ez1), (Ex2, Ey2, Ez2), ...],
...
]

My work started on March the 30th.

order of files to read:
eingabe, fft_data, matrices_and_multply
"""
from eingabe import input_data

if __name__ == '__main__':
    import numpy as np
    data = input_data()[1]
    print(np.shape(data)[1])
    pass

