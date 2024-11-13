import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, solve, Matrix, simplify, latex
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from utils import setup_latex, save_figure_to_temp, render_latex_to_file

def find_normal_line():
    """Находит параметрическое уравнение нормали к плоскости"""
    # Коэффициенты плоскости x - y - 3z - 3 = 0
    a, b, c, d = 1, -1, -3, -3
    
    # Направляющий вектор нормали
    normal = np.array([a, b, c])
    normal = normal / np.linalg.norm(normal)  # нормализация
    
    # Точка пересечения с началом координат (0, 0, z0)
    z0 = -d / c
    intersection_point = np.array([0, 0, z0])
    
    return intersection_point, normal

def plot_plane_and_normal():
    """Визуализирует плоскость и нормаль"""
    setup_latex()
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Создаем сетку точек для плоскости
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = -(X - Y - 3) / 3
    
    # Строим плоскость
    surf = ax.plot_surface(X, Y, Z, alpha=0.5)
    
    point, normal = find_normal_line()
    
    # Строим нормаль
    t = np.linspace(-2, 2, 100)
    X_normal = point[0] + normal[0] * t[:, np.newaxis]
    Y_normal = point[1] + normal[1] * t[:, np.newaxis]
    Z_normal = point[2] + normal[2] * t[:, np.newaxis]
    
    ax.plot(X_normal, Y_normal, Z_normal, 'r-', linewidth=2, 
           label=r'$\vec{n}$')
    
    ax.scatter([point[0]], [point[1]], [point[2]], color='g', s=100, 
              label=r'$P_0$')
    
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.set_zlabel(r'$z$')
    ax.set_title(r'$x - y - 3z - 3 = 0$')
    ax.legend(fontsize=10)
    
    return fig

def find_projection_matrix():
    """Находит матрицу A для нелинейной проекции T"""
    # Определяем символьные переменные
    x1, x2, x3, x4 = symbols('x1 x2 x3 x4')
    a1, a2, a3 = symbols('a1 a2 a3')
    r1, r2, r3 = symbols('r1 r2 r3')  # Компоненты вектора r
    
    # Вектор x в R⁴
    x = Matrix([x1, x2, x3, x4])
    # Вектор a в R³
    a = Matrix([a1, a2, a3])
    # Вектор r в R³
    r = Matrix([r1, r2, r3])
    
    # T(r) = r/(a·r) при a·r ≠ 0
    # Для проективного пространства: T[x] = [Ax]
    # где A - матрица 4×4
    
    # Матрица A должна удовлетворять условию:
    # T([x1:x2:x3:x4]) = [x1/(a·r):x2/(a·r):x3/(a·r):1]
    
    A = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [a1, a2, a3, 0]
    ])
    
    return A, r

def create_report(canvas):
    """Создает PDF отчет с решением"""
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-10')
    
    # Часть 1 - Нормаль к плоскости
    y = 770
    
    canvas.drawString(50, y, '1. Нормаль к плоскости x - y - 3z - 3 = 0:')
    
    point, normal = find_normal_line()
    
    y -= 40
    canvas.drawString(50, y, 'а) Точка пересечения с осью OZ:')
    canvas.drawString(70, y-20, 'P0 = (0, 0, -1)')
    
    y -= 50
    canvas.drawString(50, y, 'Параметрическое уравнение нормали:')
    canvas.drawString(70, y-20, f'r(t) = ({point[0]}, {point[1]}, {point[2]}) + ')
    canvas.drawString(70, y-40, f't·({normal[0]:.3f}, {normal[1]:.3f}, {normal[2]:.3f})')
    
    # Сохраняем график с LaTeX
    fig = plot_plane_and_normal()
    filepath = save_figure_to_temp(fig, 'plot_10.png')
    canvas.drawImage(filepath, 50, 250, width=500, height=400)
    
    canvas.showPage()
    
    # Вторая страница - Нелинейная проекция
    canvas.setFont('Roboto', 12)
    canvas.drawString(50, 800, '2. Нелинейная проекция T:')
    
    y = 770
    for line in [
        'а) Доказательство нелинейности T:',
        '',
        '1) Проверим однородность:',
        '   T(cr) = cr/(a·r) = r/(a·r) = T(r)',
        '   Однородность выполняется',
        '',
        '2) Проверим аддитивность:',
        '   T(r₁ + r₂) = (r₁ + r₂)/(a·(r₁ + r₂))',
        '   T(r₁) + T(r₂) = r₁/(a·r₁) + r₂/(a·r₂)',
        '   T(r₁ + r₂) ≠ T(r₁) + T(r₂)',
        '',
        '3) Следовательно, T - нелинейное отображение',
        '',
        'б) Матрица A порядка 4 для T[x] = [Ax]:',
        '',
        '   |1  0  0  0|',
        '   |0  1  0  0|',
        '   |0  0  1  0|',
        '   |a₁ a₂ a₃ 0|',
        '',
        'где a = (a₁, a₂, a₃) - фиксированный вектор',
        '',
        'Проверка:',
        '1) Для x = (x₁, x₂, x₃, x₄) получаем:',
        '   Ax = (x₁, x₂, x₃, a·r)',
        '2) В проективном пространстве:',
        '   [Ax] = [x₁:x₂:x₃:a·r] = [x₁/(a·r):x₂/(a·r):x₃/(a·r):1]',
        '   что совпадает с определением T[x]'
    ]:
        if line == '':
            y -= 10
        else:
            canvas.drawString(50, y, line)
            y -= 20

if __name__ == "__main__":
    # Для локального тестирования
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("report_project_10.pdf", pagesize=A4)
    c.setFont('Roboto', 12)
    create_report(c)
    c.save() 