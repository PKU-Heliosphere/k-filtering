# k-filtering

这个程序由林荣在张磊博士的源程序上修改完成。

## 程序功能

根据给定的格式化数据，计算空间中磁场或电场波动四维谱$P(\omega,k_x,k_y,k_z)$估计，绘制$\vec k$值各向异性和$\omega-k_i$关系图。

## 建议阅读顺序

location_and_klist.py是参数文件

1. eingabe.py
2. fft_data.py
3. M_matrices.py
4. filter_(centrl_algrthm).py
5. main_calc_4d_spectrum.py
6. main_plot_data.py

相信你在阅读完成之后一定能掌握如何使用它。

## 备注

源程序中求$M$矩阵的时候用的是平均。
$$
\mathrm{M}_{A}(\omega)=E\left[\boldsymbol{A}(\omega) \boldsymbol{A}^{\dagger}(\omega)\right],\quad M_{A}(\omega)=\frac{1}{Q} \sum_{q=1}^{Q} A^{q}(\omega) A^{q \dagger}(\omega)
$$
但在我的程序里偷了个懒。直接加总，也就是说
$$
M_{A}(\omega)= \sum_{q=1}^{Q} A^{q}(\omega) A^{q \dagger}(\omega)
$$
所以P值的绝对值失去了意义（但相对值仍然有）。如果你看不懂这段的意义，那么忽略它。