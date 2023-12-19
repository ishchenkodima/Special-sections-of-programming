# Завдання 2
import numpy as np
import matplotlib.pyplot as plt

# Завдання 1
def generate_data(n_points, k, b, noise_std=5):
    x = np.random.rand(n_points) * 100
    noise = np.random.normal(0, noise_std, n_points)
    y = k * x + b + noise
    return x, y

# Задаємо параметри прямої
true_k = 2
true_b = 10

# Генеруємо дані
x, y = generate_data(100, true_k, true_b)

# Знаходимо оцінки за методом найменших квадратів
A = np.vstack([x, np.ones(len(x))]).T
k, b = np.linalg.lstsq(A, y, rcond=None)[0]

# Знаходимо оцінки за np.polyfit
polyfit_k, polyfit_b = np.polyfit(x, y, 1)

# Відображаємо графік
plt.scatter(x, y, label='Дані')
plt.plot(x, true_k * x + true_b, label='Справжня пряма', color='red', linestyle='--')
plt.plot(x, k * x + b, label='Оцінка (МНК)', color='green', linestyle='--')
plt.plot(x, polyfit_k * x + polyfit_b, label='Оцінка (polyfit)', color='blue', linestyle='--')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Оцінка лінії регресії')
plt.show()






def gradient_descent(x, y, learning_rate, n_iter):
    k, b = 0, 0
    m = len(x)
    for _ in range(n_iter):
        y_pred = k * x + b
        error = y_pred - y
        gradient_k = (2/m) * np.sum(error * x)
        gradient_b = (2/m) * np.sum(error)
        k -= learning_rate * gradient_k
        b -= learning_rate * gradient_b
    return k, b

# Визначаємо параметри градієнтного спуску
learning_rate = 0.01
n_iter = 1000

# Знаходимо оцінки за градієнтним спуском
gd_k, gd_b = gradient_descent(x, y, learning_rate, n_iter)

# Відображаємо графік
plt.scatter(x, y, label='Дані')
plt.plot(x, true_k * x + true_b, label='Справжня пряма', color='red', linestyle='--')
plt.plot(x, k * x + b, label='Оцінка (МНК)', color='green', linestyle='--')
plt.plot(x, polyfit_k * x + polyfit_b, label='Оцінка (polyfit)', color='blue', linestyle='--')
plt.plot(x, gd_k * x + gd_b, label='Оцінка (градієнтний спуск)', color='purple', linestyle='--')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Оцінка лінії регресії')
plt.show()
