import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
import japanize_matplotlib

# パラメータ設定
sampling_rate = 1000  # サンプリングレート (Hz)
T = 1.0 / sampling_rate  # サンプリング間隔
L = 1000  # 信号の長さ
t = np.arange(0, L) * T  # 時間ベクトル

# 矩形波の生成
freq = 20/(2*np.pi) # 矩形波の周波数 (Hz)
print(f"矩形波の周波数は: {freq:.2f} Hz")
# square_wave = 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t)))
square_wave = np.sin(2 * np.pi *freq * t)

# 正規分布に従う全体的なノイズを追加
overall_noise = np.random.normal(0, 0.1, square_wave.shape)
noisy_signal = square_wave + overall_noise

# 複数のランダムな周波数と振幅のノイズを追加
num_noises = 20  # ノイズの数

for _ in range(num_noises):
    random_freq = np.random.uniform(30, 100)  # 20Hzから300Hzの間のランダムな周波数
    random_amplitude = np.random.uniform(0.1, 0.4)  # 0.1から0.5の間のランダムな振幅
    noise = random_amplitude * np.sin(2 * np.pi * random_freq * t)
    noisy_signal += noise

# RC回路のパラメータ
R = 10e3  # 抵抗値 (オーム)
C = 1e-6  # 静電容量 (ファラド)
cutoff = 1 / (2 * np.pi * R * C)  # カットオフ周波数 (Hz)

print(f"カットオフ周波数は: {cutoff:.2f} Hz")

# RC回路の伝達関数に基づくフィルタの設計
def rc_lowpass_filter(signal, R, C, sampling_rate):
    dt = 1 / sampling_rate
    alpha = dt / (R * C + dt)
    filtered_signal = np.zeros_like(signal)
    for i in range(1, len(signal)):
        filtered_signal[i] = filtered_signal[i-1] + alpha * (signal[i] - filtered_signal[i-1])
    return filtered_signal

filtered_signal = rc_lowpass_filter(noisy_signal, R, C, sampling_rate)

# FFTの計算
def compute_fft(signal):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, T)[:N//2]
    return xf, 2.0/N * np.abs(yf[0:N//2])

xf_square, yf_square = compute_fft(square_wave)
xf_noisy, yf_noisy = compute_fft(noisy_signal)
xf_filtered, yf_filtered = compute_fft(filtered_signal)

# 周波数帯域の調整
freq_range = (0, 100)  # 表示したい周波数帯域 (Hz)
mask = (xf_square >= freq_range[0]) & (xf_square <= freq_range[1])

# プロット
plt.figure(figsize=(15, 12))

# Original Square Wave
plt.subplot(4, 2, 1)
plt.plot(t, square_wave, label='ノイズがない正弦波')
plt.title('ノイズがない正弦波')
plt.xlabel('時間 [s]')
plt.ylabel('電圧 [V]')
plt.grid()
plt.legend()

plt.subplot(4, 2, 2)
plt.plot(xf_square[mask], yf_square[mask], label='高速フーリエ変換したノイズがない正弦波')
plt.title('高速フーリエ変換したノイズがない正弦波')
plt.xlabel('周波数 [s]')
plt.ylabel('電圧 [V]')
plt.grid()
plt.legend()

# Noisy Signal
plt.subplot(4, 2, 3)
plt.plot(t, noisy_signal, label='ノイズありのsin波の入力信号', color='orange')
plt.title('ノイズありのsin波の入力信号')
plt.xlabel('時間 [s]')
plt.ylabel('電圧 [V]')
plt.grid()
plt.legend()

plt.subplot(4, 2, 4)
plt.plot(xf_noisy[mask], yf_noisy[mask], label='高速フーリエ変換したノイズありのsin波の入力信号', color='orange')
plt.title('高速フーリエ変換したノイズありのsin波の入力信号')
plt.xlabel('周波数 [s]')
plt.ylabel('電圧 [V]')
plt.grid()
plt.legend()

# Filtered Signal
plt.subplot(4, 2, 5)
plt.plot(t, filtered_signal, label='フィルタ後の出力信号', color='green')
plt.title('フィルタ後の出力信号')
plt.xlabel('時間 [s]')
plt.ylabel('電圧 [V]')
plt.grid()
plt.legend()

plt.subplot(4, 2, 6)
plt.plot(xf_filtered[mask] , yf_filtered[mask], label='高速フーリエ変換したフィルタ後の出力信号', color='green')
plt.title('高速フーリエ変換したフィルタ後の出力信号')
plt.xlabel('周波数 [s]')
plt.ylabel('電圧 [V]')
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()

# フィルタのゲインと位相のボード線図のプロット
plt.figure(figsize=(15, 6))

# RC回路の伝達関数
w = np.logspace(-2, 4, 1000)
h = 1 / (1 + 1j * w * R * C)

plt.subplot(1, 2, 1)
plt.plot(w, 20 * np.log10(abs(h)), label='RC Lowpass')
plt.xscale('log')
plt.title('ゲインのボード線図')
plt.xlabel('時間 [rad/s]')
plt.ylabel('ゲイン [dB]')
plt.grid(which='both', axis='both')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(w, np.angle(h) * 180 / np.pi, label='RC Lowpass')
plt.xscale('log')
plt.title('位相のボード線図')
plt.xlabel('時間 [rad/s]')
plt.ylabel('位相 [°]')
plt.grid(which='both', axis='both')
plt.legend()

plt.tight_layout()
plt.show()

# カットオフ周波数での位相遅延を確認
cutoff_phase_delay = np.angle(1 / (1 + 1j * 2 * np.pi * cutoff * R * C)) * 180 / np.pi
print(f"カットオフ周波数での位相遅延は: {cutoff_phase_delay:.2f} 度")
