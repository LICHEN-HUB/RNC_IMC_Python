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
  x_buffer[:,:,-1]=np.repeat(data_mic[ref_slice,i-1],num_spkr).reshape(num_ref,num_spkr))


  #频域更新
  if i% block_size==block_size -1:


    X_k=np.fft.rfft(x)
    Xs_k=X_k*fir_2nd_path_freq[ref_slice]
    Xs_k_conj=Xs_k.conj()


    #更新频域输入功率估计，用于归一化步长


    instant_px=np.abs(Xs_k)**2
    px_power=(1-alpha)*px_power+alpha*instant_px


    #构造归一化步长
    D_k=1/(px_power+eps)


    #计算误差  
    e_buf_pad=np.pad(e_buffer,((0,0),(fft_size//2,0)),mode="constant")
    E_k=np.fft.rfft(e_buf_pad)


    # 梯度，求与对应误差互相关
    for idx_ref in range(num_ref):
       grad_k[idx_ref]=(D_k[idx_ref]*Xs_k_conj[idx_ref]*E_k[idx_ref])


    #舍去无用的部分，频域 时域 频域 防止频谱泄漏干扰
    grad_time=np.fft.irfft(grad_k)
    grad_time[:,:,fft_size2:]=0
    grad_k=np.fft.rfft(grad_time)
    #更新
    W_K=(1-leaky)*W_K-mu0*grad_k
    w_n=np.fft.irfft(W_K)[:,:,:order_adaptive]
    w_n=W_n[:,:,::-1]
#时域更新
y_n=np.sum(w_n*x_buffer[:,:,-order_adaptive:],axis=2)
y_n=np.sum(y_n,axis=0)
y_out.append(y_n)

#更新激励信号缓冲，注意匹配卷积定义

y_buffer=np.roll(y_buffer,-1,axis=1)
y_buffer[:,-1]=y_n

#模拟降噪效果，实际算法中替换成mic

for idx_mic in range (num_mic):
  e_closed[idx_mic][i]=data_mic[idx_mic][i]+np.sum(fir_2nd_path_time[idx_mic]*y_buffer)
  e_buffer=np.roll(e_buffer,-1,axis=1)
  e_buffer[:,-1]=e_closed[ref_slice,i]
