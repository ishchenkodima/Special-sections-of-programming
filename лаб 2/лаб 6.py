import numpy as np
import matplotlib.pyplot as plt
from numba import njit


@njit(nogil=True)
def least_squares(x, y):
    k, b, sum_up, sum_down = 0, 0, 0, 0

    for i in range(x.shape[0]):
        sum_up += (x[i] - x.mean()) * (y[i] - y.mean())
        sum_down += (x[i] - x.mean()) ** 2
    k = sum_up / sum_down
    b = y.mean() - k * x.mean()
    return k, b


@njit(nogil=True)
def not_in_treshhold(element, treshhold):
    # print(element, treshhold)
    if (abs(element) < treshhold):
        return True
    return False


@njit(nogil=True)
def gradient_descent(x, y, learning_rate_k=0.00000001, learning_rate_b=0.001, treshhold=1e-4, n_iter=150000,
                     cost_needed=False):
    b = 0
    k = 0
    i = 0
    stop = False

    while i != n_iter and not stop:
        y0 = b + k * x
        # if i == 0:
        #     epsilon = [np.mean((y0 - y) ** 2), i]
        dLdb = -2 * np.mean(y - y0)
        dLdk = -2 * np.mean(x * (y - y0))
        # print(dLdb, dLdk)
        b = b - learning_rate_b * dLdb
        k = k - learning_rate_k * dLdk

        # if epsilon_needed and i != 0:
        #     epsilon += [np.mean((y0 - y) ** 2), i]

        stop = not_in_treshhold(dLdk, treshhold)
        if not stop:
            stop = not_in_treshhold(dLdb, treshhold)

        i += 1
    # print(i)
    if cost_needed:
        return [k, b, i]
    # elif epsilon_needed:
    #     return [k, b, epsilon]
    else:
        return [k, b]


@njit(nogil=True)
def gradient_descent_with_cost(x, y, learning_rate_k=0.00000001, learning_rate_b=0.001, treshhold=1e-4, n_iter=150000,
                               cost_needed=False):
    b = 0
    k = 0
    i = 0
    stop = False

    while i != n_iter and not stop:
        y0 = b + k * x
        if i == 0:
            epsilon = [[np.mean((y0 - y) ** 2), i]]
        dLdb = -2 * np.mean(y - y0)
        dLdk = -2 * np.mean(x * (y - y0))
        # print(dLdb, dLdk)
        b = b - learning_rate_b * dLdb
        k = k - learning_rate_k * dLdk

        if i != 0:
            epsilon += [[np.mean((y0 - y) ** 2), i]]

        stop = not_in_treshhold(dLdk, treshhold)
        if not stop:
            stop = not_in_treshhold(dLdb, treshhold)

        i += 1
    # print(i)
    return k, b, epsilon


@njit(nogil=True)
def search(k_s, b_s, polyfit_k, polyfit_b, x, y):
    lrn_rates_to_try = [1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1e-2]
    n_iters_to_try = [1e6, 1e4, 1e2]
    min_cost = np.inf

    for lrn_rate_k in lrn_rates_to_try:
        for lrn_rate_b in lrn_rates_to_try:
            for n_iter in n_iters_to_try:
                [k1, b1, iter_used] = gradient_descent(x, y, learning_rate_k=lrn_rate_k, learning_rate_b=lrn_rate_b,
                                                       n_iter=n_iter, cost_needed=True)
                # print(k1, b1, cost)
                if min_cost >= iter_used and polyfit_k - 1e-3 < k1 < polyfit_k + 1e-3 and polyfit_b - 1 < b1 < polyfit_b + 1:
                    min_cost = iter_used
                    the_best_way = [lrn_rate_k, lrn_rate_b, n_iter, iter_used]
                    print('\nk:', k1, 'b:', b1)
                    print('learning rate for k:', lrn_rate_k, '\nlearning rate for b:', lrn_rate_b, '\nn iterations: ',
                          n_iter, '\niterations used: ', iter_used)
    return the_best_way


@njit(nogil=True)
def split_list_into_two(array):
    # for i in range(len(lst)):
    #     lst_for_mean += [lst[i][0]]
    #     lst_for_k += [lst[i][1]]
    i = 0
    for mean, k in array:
        if i == 0:
            lst_for_mean = np.array([mean])
            lst_for_k = np.array([k])
        else:
            lst_for_mean = np.concatenate((lst_for_mean, np.array([mean])))
            lst_for_k = np.concatenate((lst_for_k, np.array([k])))
        i += 1
    return lst_for_mean, lst_for_k


# Завдання 1 (2б):
# 1. Згенеруйте двовимірні дані (x, y) за допомогою numpy.random : бажано, щоб розподіл
# точок був навколо деякої наперед заданої прямої (y = k*x + b) для подальшого аналізу
# результатів.
# 2. Напишіть функцію, яка реалізує метод найменших квадратів для пошуку оптимальних
# оцінок kk� та bb�.
# 3. Порівняйте знайдені параметри з оцінкою np.polyfit(x,y,1) (оцінка полінома
# степеню 1 методом найменших квадратів), та з початковими параметрами прямої (якщо
# такі є).
# 4. Відобразіть на графіку знайдені оцінки лінії регресії (вашої та numpy). Якщо ви
# генерували вхідні дані навколо лінії, відобразіть також її.

# Завдання 2 (2б):
# 1. Напишіть функцію, яка реалізує метод градієнтного спуску для пошуку оптимальних
# оцінок kk� та bb�. Визначіть оптимальні вхідні параметри: learning_rate, n_iter
# 2. Додайте отриману лінію регресії на загальний графік
# 3. Побудуйте графік похибки від кількості ітерацій, зробіть висновки
# 4. Порівняйте отримані результати з результатами попереднього завдання

# Корисні посилання
# 1. https://uk.wikipedia.org/wiki/Проста_лінійна_регресія
# 2. https://uk.wikipedia.org/wiki/Градієнтний_спуск
# 3. https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
# 4. https://numpy.org/doc/stable/reference/arrays.html
# 5. McKinney Wes. 2012. Python for data analysis (1st. ed.). O'Reilly Media, Inc.

def UI(need_best_way):
    k_s = 2.5
    b_s = 10
    n = 1000
    x = np.linspace(0, 500, n)
    y = k_s * x + b_s + np.random.normal(0, 10, x.shape[0])

    print(f"Початкові параметри: k = {k_s}, b = {b_s}")

    # Знайдемо оцінки параметрів
    ks, bs = least_squares(x, y)
    print(f"Оцінка методом найменших квадратів: k = {ks}, b = {bs}")

    # Порівняння з np.polyfit
    polyfit_k, polyfit_b = np.polyfit(x, y, 1)
    print(f"Оцінка за допомогою np.polyfit: k = {polyfit_k}, b = {polyfit_b}")

    # Знайдемо оцінки параметрів за допомогою градієнтного спуску
    gd_k, gd_b = gradient_descent(x, y)  # , epsilon
    print(f"Оцінка методом градієнтного спуску: k = {gd_k}, b = {gd_b}")

    if need_best_way:
        the_best_way = search(k_s, b_s, polyfit_k, polyfit_b, x, y)
        print(
            f'\nThe best way is: \nlearning rate for k: {the_best_way[0]}, \nlearning rate for b: {the_best_way[1]}, \niterations used: {the_best_way[3]}')

    gd_k_c, gd_b_c, epsilon = gradient_descent_with_cost(x, y)

    lst_for_mean, lst_for_k = split_list_into_two(np.array(epsilon))  # , lst_for_mean, lst_for_k)

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.scatter(x, y, label='Згенеровані дані')
    ax1.plot(x, k_s * x + b_s, color='red', label='Пряма')
    ax1.plot(x, ks * x + bs, color='green', label='Метод найменших квадратів')
    ax1.plot(x, polyfit_k * x + polyfit_b, color='purple', label='np.polyfit')
    ax1.plot(x, gd_k * x + gd_b, color='orange', label='Градієнтний спуск')

    ax2.plot(lst_for_k, lst_for_mean, label='Похибка від кількості')

    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax2.set_xlabel('Кількість ітерацій')
    ax2.set_ylabel('Похибка')

    ax1.legend()
    ax2.legend()

    plt.show()


need_best_way = input('1 if bestway needed, anything (except 1) if not: ') == '1'
UI(need_best_way)