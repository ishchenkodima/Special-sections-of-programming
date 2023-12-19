import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Button, Slider
from scipy import signal

class MPLTTask:

    @staticmethod
    def my_filter(data, window_size):
        # Створення фільтраційного ядра та застосування фільтрації до даних
        kernel = np.ones(window_size) / window_size
        filtered_data = np.convolve(data, kernel, mode='same')
        return filtered_data

    @staticmethod
    def check_noise_need(prev_mean, prev_covar, noise_mean, noise_covar):
        # Перевірка, чи потрібно застосувати шум до гармоніки
        return prev_mean != noise_mean or prev_covar != noise_covar, noise_mean, noise_covar

    @staticmethod
    def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean=0, noise_covariance=0, show_noise=True):
        # Гармоніка з можливістю застосування шуму
        need_noise, new_mean, new_covar = MPLTTask.check_noise_need(prev_mean, prev_covar, noise_mean, noise_covariance)
        if need_noise or not hasattr(MPLTTask.harmonic_with_noise, 'noise'):
            MPLTTask.harmonic_with_noise.noise = np.random.normal(new_mean, new_covar, len(t))

        harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
        noisy_harmonic = harmonic + MPLTTask.harmonic_with_noise.noise

        return noisy_harmonic if show_noise else harmonic

    @staticmethod
    def update_plot(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
        # Оновлення графіку під час зміни параметрів
        t, harmonic, signal_with_noise = MPLTTask.harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)
        with fig.batch_update():
            # Оновлення графіків гармоніки та гармоніки із шумом
            fig.data[0].x = t
            fig.data[0].y = harmonic
            fig.data[1].x = t
            fig.data[1].y = signal_with_noise

    @staticmethod
    def create_figure(t, init_amplitude, init_frequency, init_phase, init_noise_mean,
                      init_noise_covariance, init_filter, init_filter_m):
        # Створення графічного вікна та інтерфейсу користувача
        fig, (ax0, ax1) = plt.subplots(1, 2)

        # Побудова графіків та приховання їх
        line2, = ax0.plot(t, MPLTTask.harmonic_with_noise(t, init_amplitude, init_frequency, init_phase,
                                                          init_noise_mean, init_noise_covariance), visible=False,
                          color='#FF5722', lw=2)
        line, = ax0.plot(t, MPLTTask.harmonic_with_noise(t, init_amplitude, init_frequency, init_phase),
                         color='#3F51B5', lw=2)

        # Фільтрація гармоніки та приховання результатів
        b, a = signal.butter(4, init_filter, btype='low')
        my_filtered_harmonic = MPLTTask.my_filter(
            MPLTTask.harmonic_with_noise(t, init_amplitude, init_frequency, init_phase, init_noise_mean,
                                         init_noise_covariance),
            int(round(init_filter_m)))
        line4, = ax1.plot(t, my_filtered_harmonic, visible=False, lw=2)

        filtered_harmonic = signal.lfilter(b, a,
                                           MPLTTask.harmonic_with_noise(t, init_amplitude, init_frequency, init_phase,
                                                                       init_noise_mean, init_noise_covariance))
        line3, = ax1.plot(t, filtered_harmonic, visible=False, lw=2)

        # Налаштування вигляду та розташування графічних елементів
        ax0.set_xlabel('Time [s]')
        ax0.set_title('Harmonic')
        ax1.set_xlabel('Time [s]')
        ax1.set_title('Filtered Harmonic')
        fig.subplots_adjust(left=0.25, bottom=0.35, top=0.75, right=0.85)

        # Створення слайдерів
        axamp = fig.add_axes([0.25, 0.2, 0.65, 0.03])
        amp_slider = Slider(ax=axamp, label="Amplitude", valmin=0, valmax=10, valinit=init_amplitude, color='red')

        axfreq = fig.add_axes([0.25, 0.15, 0.65, 0.03])
        freq_slider = Slider(ax=axfreq, label='Frequency [Hz]', valmin=0.1, valmax=30, valinit=init_frequency,
                             color='grey')

        axphas = fig.add_axes([0.25, 0.1, 0.65, 0.03])
        phas_slider = Slider(ax=axphas, label='Phase', valmin=0, valmax=2 * np.pi, valinit=init_phase, color='purple')

        nmamp = fig.add_axes([0.15, 0.35, 0.0225, 0.53])
        noismean_slider = Slider(ax=nmamp, label="Mean", valmin=-5, valmax=5, valinit=init_noise_mean,
                                 orientation="vertical", color='#3F51B5')

        ncamp = fig.add_axes([0.08, 0.35, 0.0225, 0.53])
        noiscovar_slider = Slider(ax=ncamp, label="Covar", valmin=0, valmax=5, valinit=init_noise_covariance,
                                  orientation="vertical", color='#FF5722')

        fltamp = fig.add_axes([0.95, 0.35, 0.0225, 0.53])
        flt_slider = Slider(ax=fltamp, label="Filter", valmin=0.001, valmax=0.1, valinit=init_filter,
                            orientation="vertical")

        fltmamp = fig.add_axes([0.87, 0.35, 0.0225, 0.53])
        flt_m_slider = Slider(ax=fltmamp, label="My Filter", valmin=1, valmax=200, valinit=init_filter_m,
                              orientation="vertical")

        rax = fig.add_axes([0.40, 0.82, 0.35, 0.12])
        check = CheckButtons(rax, ('Harmonic with noise', 'Harmonic filtered', 'Harmonic with my filter'),
                             (False, False, False))

        resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
        button = Button(resetax, 'Reset', hovercolor='0.975')

        # Повернення об'єктів графічного вікна та елементів інтерфейсу користувача
        return fig, line, line2, line3, line4, amp_slider, freq_slider, phas_slider, noismean_slider, noiscovar_slider, flt_slider, flt_m_slider, check, button

    @staticmethod
    def update(val, t, line, line2, line3, line4, amp_slider, freq_slider, phas_slider, noismean_slider,
               noiscovar_slider, flt_slider, flt_m_slider):
        # Оновлення графіку при зміні параметрів
        b, a = signal.butter(4, flt_slider.val, btype='low')

        # Оновлення графіків
        line2.set_ydata(
            MPLTTask.harmonic_with_noise(t, amp_slider.val, freq_slider.val, phas_slider.val, noismean_slider.val,
                                         noiscovar_slider.val))
        line.set_ydata(MPLTTask.harmonic_with_noise(t, amp_slider.val, freq_slider.val, phas_slider.val))

        my_filtered_harmonic = MPLTTask.my_filter(
            MPLTTask.harmonic_with_noise(t, amp_slider.val, freq_slider.val, phas_slider.val, noismean_slider.val,
                                         noiscovar_slider.val), int(round(flt_m_slider.val)))
        line4.set_ydata(my_filtered_harmonic)

        filtered_harmonic = signal.lfilter(b, a, MPLTTask.harmonic_with_noise(t, amp_slider.val, freq_slider.val,
                                                                              phas_slider.val, noismean_slider.val,
                                                                              noiscovar_slider.val))
        line3.set_ydata(filtered_harmonic)

        plt.draw()

    @staticmethod
    def func(label, line, line2, line3, line4):
        # Реакція на подію перемикача
        if label == 'Harmonic with noise':
            line2.set_visible(not line2.get_visible())
        elif label == 'Harmonic filtered':
            line3.set_visible(not line3.get_visible())
        elif label == 'Harmonic with my filter':
            line4.set_visible(not line4.get_visible())
        plt.draw()

    @staticmethod
    def reset(event, freq_slider, amp_slider, phas_slider, noismean_slider, noiscovar_slider, flt_slider, flt_m_slider):
        # Скидання параметрів до значень за замовчуванням
        freq_slider.reset()
        amp_slider.reset()
        phas_slider.reset()
        noismean_slider.reset()
        noiscovar_slider.reset()
        flt_slider.reset()
        flt_m_slider.reset()

# Ініціалізація параметрів
t = np.linspace(0, 1, 1000)
init_amplitude = 5
init_frequency = 3
init_phase = 0
init_noise_mean = 0
init_noise_covariance = 0
init_filter = 0.03
init_filter_m = 50
prev_mean = None
prev_covar = None

# Створення графічного вікна
fig, line, line2, line3, line4, amp_slider, freq_slider, phas_slider, noismean_slider, noiscovar_slider, flt_slider, flt_m_slider, check, button = MPLTTask.create_figure(
    t, init_amplitude, init_frequency, init_phase, init_noise_mean, init_noise_covariance, init_filter, init_filter_m)

# Реєстрація функцій оновлення
check.on_clicked(lambda label: MPLTTask.func(label, line, line2, line3, line4))
freq_slider.on_changed(lambda val: MPLTTask.update(val, t, line, line2, line3, line4, amp_slider, freq_slider, phas_slider,
                                                  noismean_slider, noiscovar_slider, flt_slider, flt_m_slider))
amp_slider.on_changed(lambda val: MPLTTask.update(val, t, line, line2, line3, line4, amp_slider, freq_slider,
                                                 phas_slider, noismean_slider, noiscovar_slider, flt_slider, flt_m_slider))
phas_slider.on_changed(lambda val: MPLTTask.update(val, t, line, line2, line3, line4, amp_slider, freq_slider,
                                                  phas_slider, noismean_slider, noiscovar_slider, flt_slider, flt_m_slider))
noismean_slider.on_changed(lambda val: MPLTTask.update(val, t, line, line2, line3, line4, amp_slider, freq_slider,
                                                      phas_slider, noismean_slider, noiscovar_slider, flt_slider,
                                                      flt_m_slider))
noiscovar_slider.on_changed(lambda val: MPLTTask.update(val, t, line, line2, line3, line4, amp_slider, freq_slider,
                                                       phas_slider, noismean_slider, noiscovar_slider, flt_slider,
                                                       flt_m_slider))
flt_slider.on_changed(lambda val: MPLTTask.update(val, t, line, line2, line3, line4, amp_slider, freq_slider,
                                                  phas_slider, noismean_slider, noiscovar_slider, flt_slider, flt_m_slider))
flt_m_slider.on_changed(lambda val: MPLTTask.update(val, t, line, line2, line3, line4, amp_slider, freq_slider,
                                                   phas_slider, noismean_slider, noiscovar_slider, flt_slider,
                                                   flt_m_slider))
button.on_clicked(lambda event: MPLTTask.reset(event, freq_slider, amp_slider, phas_slider, noismean_slider,
                                               noiscovar_slider, flt_slider, flt_m_slider))

plt.show()






