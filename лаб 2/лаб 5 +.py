# Імпорт необхідних бібліотек
import plotly.graph_objects as go
import numpy as np
from ipywidgets import interact, widgets, Layout
from IPython.display import display

class Plot:
    def __init__(self):
        # Визначення відсутніх змінних (замініть їх реальними значеннями)
        self.init_amplitude = 1.0
        self.init_noise_amplitude = 0.1
        self.init_frequency = 1.0
        self.init_noise_covariance = 0.5
        self.x = np.linspace(0, 10, 100)

        # Виправлена назва змінної
        # Визначте гармонічну та гармонічну з шумом функції
        self.harmonic = lambda x, a, f, phi: a * np.sin(2 * np.pi * f * x + phi)
        self.harmonic_with_noise = lambda x, a, f, phi, mean, cov, show_noise: \
            self.harmonic(x, a, f, phi) + np.random.normal(mean, cov, len(x))

        self.show_in_time = True

        # Вертикальна частина віджетів
        # Створення вертикальних слайдерів для амплітуди та шумової амплітуди
        self.amplitude = widgets.FloatSlider(
            value=self.init_amplitude,
            min=0.0,
            max=30.0,
            step=0.01,
            description='Амплітуда',
            orientation='vertical',
            continuous_update=self.show_in_time,
            layout=Layout(height='auto')
        )

        # Виправлена назва змінної
        self.noise_amplitude = widgets.FloatSlider(
            value=self.init_noise_amplitude,
            min=-1.0,
            max=1.0,
            step=0.01,
            description='Амплітуда шуму',
            orientation='vertical',
            continuous_update=self.show_in_time,
            layout=Layout(height='auto')
        )

        # Створення вертикальної коробки для утримання слайдерів амплітуди та шумової амплітуди
        self.vertical_box_layout = Layout(display='flex',
                                          flex_flow='row',
                                          align_items='stretch',
                                          width='20%')
        self.vertical_box = widgets.Box(children=[self.amplitude, self.noise_amplitude],
                                       layout=self.vertical_box_layout)

        # Горизонтальна частина віджетів
        # Створення горизонтальних слайдерів для частоти, коваріації, епсілону та N
        self.frequency = widgets.FloatSlider(
            value=self.init_frequency,
            min=.0,
            max=30.0,
            step=.01,
            description='Частота',
            continuous_update=self.show_in_time,
            layout=Layout(width='auto')
        )

        self.covariance = widgets.FloatSlider(
            value=self.init_noise_covariance,
            min=.0,
            max=5.0,
            step=.01,
            description='Коваріація',
            continuous_update=self.show_in_time,
            layout=Layout(width='auto')
        )

        self.epsilon = widgets.FloatSlider(
            value=.5,
            min=.0,
            max=1,
            step=.001,
            description='Епсілон',
            continuous_update=False,
            layout=Layout(width='auto')
        )

        self.N = widgets.FloatSlider(
            value=20,
            min=0,
            max=30,
            step=1,
            description='N',
            continuous_update=False,
            layout=Layout(width='auto')
        )

        # Створення горизонтальної коробки для утримання слайдерів частоти, коваріації, епсілону та N
        self.horizontal_box_layout = Layout(display='flex',
                                            flex_flow='column',
                                            align_items='stretch',
                                            width='auto')
        self.horizontal_box = widgets.Box(children=[self.frequency, self.covariance, self.epsilon, self.N],
                                         layout=self.horizontal_box_layout)

        # Прапорці
        # Створення прапорців для відображення гармоніки, гармоніки з шумом та фільтрованої лінії
        self.show_harmonic = widgets.Checkbox(
            value=True,
            description='Гармоніка',
            disabled=False,
            indent=False
        )

        self.show_harmonic_with_noise = widgets.Checkbox(
            value=False,
            description='Гармоніка з шумом',
            disabled=False,
            indent=False
        )

        self.show_filtered_line = widgets.Checkbox(
            value=False,
            description='Фільтрована лінія',
            disabled=False,
            indent=False
        )

        # Створення коробки для утримання прапорців
        self.checkbox_box_layout = Layout(display='flex',
                                          flex_flow='column',
                                          align_items='center',
                                          width='auto')
        self.checkbox_box = widgets.Box(children=[self.show_harmonic, self.show_harmonic_with_noise, self.show_filtered_line],
                                        layout=self.checkbox_box_layout)

        # Кнопка "Скидання"
        self.reset = widgets.Button(
            description='Скинути',
            disabled=False,
            button_style='',
            tooltip='Клацніть мене'
        )

        # Функція для скидання значень до початкових
        self.reset.on_click(self.reset_own)

        # Створення коробки для утримання кнопки скидання
        self.reset_layout = Layout(display='flex',
                                  flex_flow='column',
                                  align_items='center',
                                  width='auto')
        self.reset_box = widgets.Box(children=[self.reset], layout=self.reset_layout)

        # Функція для експоненційного згладжування сигналу
        def complex_filter(signal, N):
            # Ваша реалізація складного фільтра
            # Наприклад, можна використовувати складний фільтр, такий як Калманівський фільтр
            # або будь-який інший більш складний фільтр, відповідно до ваших потреб.
            pass

        self.complex_filter = complex_filter

        # Головне поле з графіком
        self.fig = go.FigureWidget()

        # Додаємо гармоніку з шумом
        self.harmonic_noisef = self.fig.add_scatter(name='Гармоніка з шумом', line=dict(color='blue'))
        self.line_harmonic_with_noise = self.harmonic_noisef.data[0]

        # Додаємо гармоніку
        self.harmonicf = self.fig.add_scatter(name='Гармоніка', line=dict(color='red'))
        self.line_harmonic = self.harmonicf.data[0]

        # Додаємо фільтровану лінію
        self.filteredf = self.fig.add_scatter(name='Фільтрована', line=dict(color='green'))
        self.line_filtered = self.filteredf.data[0]

        # Налаштування вигляду графіку
        self.fig.layout.xaxis.title = 'x'
        self.fig.layout.yaxis.range = [-8, 8]

        self.fig.update_layout(
            width=800,
            height=400,
            title='Інтерактивний гармонійний графік',
            xaxis_title='x',
            yaxis_title='Амплітуда'
        )

        # Додаємо відгук до зміни значень віджетів
        self.amplitude.observe(self.response, names="value")
        self.frequency.observe(self.response, names="value")
        self.noise_amplitude.observe(self.response, names="value")  # Виправлена назва змінної
        self.covariance.observe(self.response, names="value")
        self.show_harmonic.observe(self.response, names="value")
        self.show_harmonic_with_noise.observe(self.response, names="value")
        self.show_filtered_line.observe(self.response, names="value")
        self.epsilon.observe(self.response, names="value")

        # Відображення віджетів
        display(widgets.HBox([self.vertical_box,
                              widgets.VBox([self.fig,
                                            self.horizontal_box,
                                            self.checkbox_box,
                                            self.reset_box])]))

    # Функція для скидання значень до початкових
    def reset_own(self, a):
        self.amplitude.value = self.init_amplitude
        self.noise_amplitude.value = self.init_noise_amplitude  # Виправлена назва змінної
        self.frequency.value = self.init_frequency
        self.covariance.value = self.init_noise_covariance

    # Функція для відгуку на зміни віджетів
    def response(self, change):
        with self.fig.batch_update():
            # Оновлення трас для гармоніки з шумом
            self.fig.data[0].x = self.x
            self.fig.data[0].y = self.harmonic_with_noise(self.x, self.amplitude.value, self.frequency.value, .0,
                                                          self.noise_amplitude.value, self.covariance.value, True)

            # Оновлення трас для гармоніки
            self.fig.data[1].x = self.x
            self.fig.data[1].y = self.harmonic(self.x, self.amplitude.value, self.frequency.value, .0)

            # Оновлення трас для фільтрованого сигналу
            if self.show_filtered_line.value:
                self.fig.data[2].x = self.x
                self.fig.data[2].y = self.complex_filter(self.harmonic_with_noise(self.x, self.amplitude.value,
                                                                                 self.frequency.value, .0,
                                                                                 self.noise_amplitude.value,
                                                                                 self.covariance.value, True),
                                                         self.N.value)

# Створення екземпляру класу та виклик його конструктору
plot_instance = Plot()