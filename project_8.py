import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, simplify, cos, sin, sqrt, Matrix, eye, expand, solve
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

def calculate_tangent_vector_at_zero():
    """Вычисляет касательный вектор в точке θ = 0"""
    # Определяем символьные переменные
    a, b, alpha = symbols('a b alpha')
    
    # Компоненты вектора при θ = 0
    x = -a * alpha / b
    y = 0
    z = a * sqrt(b**2 - alpha**2) / b
    
    # Нормализация вектора
    norm = sqrt(x**2 + y**2 + z**2)
    tangent = (x/norm, y/norm, z/norm)
    
    return simplify(tangent)

def calculate_eigenvalue_and_vector():
    """Вычисляет собственное значение и вектор для матрицы поворота"""
    # Определяем символьные переменные
    theta = symbols('theta')
    n1, n2, n3 = symbols('n1 n2 n3')
    
    # Создаем кососимметрическую матрицу An
    An = Matrix([
        [0, -n3, n2],
        [n3, 0, -n1],
        [-n2, n1, 0]
    ])
    
    # Формула Родрига: Wn(θ) = I + (1-cos θ)An² + sin θ An
    I = eye(3)
    An_squared = An * An
    Wn = I + (1 - cos(theta)) * An_squared + sin(theta) * An
    
    # Вектор n является собственным вектором с собственным значением 1
    n = Matrix([n1, n2, n3])
    result = Wn * n - n  # Должно быть равно 0
    
    return simplify(result)

def plot_cylinder_intersection_with_tangent():
    """Строит пересечение цилиндров с касательным вектором в точке θ = 0"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Параметры цилиндров
    l, h = 2, 3
    a, b = 1, 1.5
    alpha = 0.5
    
    # Генерируем точки кривой пересечения
    theta = np.linspace(0, 2*np.pi, 100)
    X = np.sqrt(b**2 - (alpha + a*np.sin(theta))**2)
    Y = a * np.cos(theta)
    Z = alpha + a * np.sin(theta)
    
    # Строим кривую пересечения
    ax.plot(X, Y, Z, 'b-', label='Кивая пересечения')
    
    # Добавляем касательный вектор в точке θ = 0
    x0 = np.sqrt(b**2 - alpha**2)
    y0 = a
    z0 = alpha
    
    # Вычисляем компоненты касательного вектора
    tx = -a * alpha / b
    ty = 0
    tz = a * np.sqrt(b**2 - alpha**2) / b
    norm = np.sqrt(tx**2 + ty**2 + tz**2)
    
    # Рисуем касательный вектор
    ax.quiver(x0, y0, z0, tx/norm, ty/norm, tz/norm,
             color='r', length=0.5, label='Касательный вектор')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Пересечение цилиндров с касательным вектором')
    ax.legend()
    
    return fig

def create_report(canvas):
    """Создает PDF отчет с решением"""
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-8')
    
    # Часть 1 - Касательный вектор
    canvas.drawString(50, 770, '1. Касательный вектор в точке θ = 0:')
    
    # Получаем компоненты касательного вектора
    tangent = calculate_tangent_vector_at_zero()
    
    canvas.drawString(50, 750, 'T(0) = 1/ab · (-aα, 0, a(b² - α²)^(1/2))')
    canvas.drawString(50, 730, 'где:')
    canvas.drawString(70, 710, 'a - радиус второго цилиндра')
    canvas.drawString(70, 690, 'b - радиус первого цилиндра')
    canvas.drawString(70, 670, 'α - смещение второго цилиндра')
    
    # Сохраняем график
    fig = plot_cylinder_intersection_with_tangent()
    fig.savefig('temp_plot_8.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Добавляем график
    canvas.drawImage('temp_plot_8.png', 50, 250, width=500, height=400)
    
    canvas.showPage()
    
    # Вторая страница - Собственный вектор
    canvas.setFont('Roboto', 12)
    canvas.drawString(50, 800, '2. Собственный вектор матрицы поворота Wn(θ):')
    
    y = 770
    for line in [
        'Доказательство того, что n является собственным вектором:',
        '',
        '1) Матрица поворота Wn(θ) = I + (1-cos θ)An² + sin θ An',
        '',
        '2) Для собственного вектора n должно выполняться:',
        '   Wn(θ)n = n',
        '',
        '3) Подставляя выражение для Wn(θ):',
        '   (I + (1-cos θ)An² + sin θ An)n = n',
        '',
        '4) Упрощая:',
        '   In + (1-cos θ)An²n + sin θ Ann = n',
        '   n + (1-cos θ)(-n) + sin θ(0) = n',
        '   n - n + n = n',
        '',
        '5) Следовательно, n действительно является собственным',
        '   вектором с собственным значением 1 при любом θ',
        '',
        'Геометрическая интерпретация:',
        '- Вектор n является осью вращения',
        '- Все точки на прямой, задаваемой вектором n,',
        '  остаются неподвижными при повороте',
        '- Собственное значение 1 означает, что поворот',
        '  не меняет направление оси вращения'
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
    c = canvas.Canvas("report_project_8.pdf", pagesize=A4)
    c.setFont('Roboto', 12)
    create_report(c)
    c.save() 