import matplotlib.pyplot as plt
import scienceplots
from mplfonts import use_font

use_fornt()
plt.style.use()
import numpy as np

num_spkr=5
num_mic=6
num_ref=6

fs=1500
order_adaptive=64
order_2nd_path=128
fft_size=256
fft_real_size=fft_size//2+1
block_size=32 # 32 gengxin

data_mic=np.load()
#cijitongdao time frequnecy
def reload_complex(file_path:str)->np.ndarray:
  data=np.loadtxt(file_pth,delimiter=",")
  real=
  imag=
  restored=real+j*img
  return restored
fir_2nd_path_time=np.load
fir_2nd_path_freq=reload_complex

fir_2nd_path_time=fir_2nd_path_time.reshape((-1,num_spkr,order_2nd_path))
fir_2nd_path_freq=fir_2nd_path_freq.reshape((-1,num_spkr,fft_real_size))

from scipy.signal import welch

freq,psd=welch(data_mic[4],fs=fs,nperseg=2048,scaling="density")

plt.figure()
plt.plot(freq,20*np.log10(np.abs(psd)))
plt.show()

mu0=1e-3/num_ref
eps=1e-6
leaky=5e-3
alpha=0.05

n_sample=data_mic.shape[1]

e_buffer=np.zeros([num_ref,fft_size//2])
x_buffer=np.zeros([num_ref,num_spkr,fftsize])
y_buffer=np.zeros([num_spkr,order_2nd_path])

imc=np.zeros([num_ref,num_spkr])
#频域输入功率估计（用于归一化步长）
px_power=np.zeros([num_ref,num_spkr,fft_real_size])

#t梯度
grad_k=np.zeros([num_ref,num_spkr,fft_real_size],dype=np.complex64)

#自适应滤波器权重

w_n=np.zeros([num_ref,num_spkr,order_adaptive])
w_k=np.zeros([num_ref,num_spkr,fft_real_size])

#输出
y_n=np.zeros([num_spkr])

#闭环误差

e_closed=np.zeros([num_mic,n_sample])

#
ref_slice=slice(0,6) #修改这里来匹配参考信号数量
y_out=[]
#主循环

for i in range(1,n_samaple):
  #更新缓冲区
  x_buffer=np.roll(x_buffer,-1,axis=2)
  x_buffer
