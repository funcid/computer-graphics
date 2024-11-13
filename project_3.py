import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, simplify, cos, sin
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

def calculate_tangent_vector_explicit():
    """Вычисляет касательный вектор для явного представления кривой"""
    # Определяем символьные переменные
    x, y = symbols('x y')
    dy_dx = diff(y, x)
    
    # Касательный вектор T(x) = (1, dy/dx) / sqrt(1 + (dy/dx)²)
    T_x = (1, dy_dx)
    norm = (1 + dy_dx**2)**(1/2)
    
    return T_x, norm

def calculate_curvature_explicit():
    """Вычисляет кривизну для явного представления кривой"""
    x, y = symbols('x y')
    dy_dx = diff(y, x)
    d2y_dx2 = diff(dy_dx, x)
    
    # Кривизна κ(x) = d²y/dx² / (1 + (dy/dx)²)^(3/2)
    curvature = d2y_dx2 / (1 + dy_dx**2)**(3/2)
    
    return curvature

def calculate_tangent_vector_parametric():
    """Вычисляет касательный вектор для параметрического представления"""
    u, x, y = symbols('u x y')
    dx_du = diff(x, u)
    dy_du = diff(y, u)
    
    # Касательный вектор T(u) = (dx/du, dy/du) / sqrt((dx/du)² + (dy/du)²)
    T_u = (dx_du, dy_du)
    norm = (dx_du**2 + dy_du**2)**(1/2)
    
    return T_u, norm

def calculate_curvature_parametric():
    """Вычисляет кривизну для параметрического представления"""
    u, x, y = symbols('u x y')
    dx_du = diff(x, u)
    dy_du = diff(y, u)
    d2x_du2 = diff(dx_du, u)
    d2y_du2 = diff(dy_du, u)
    
    # Кривизна κ(u) = (dx/du * d²y/du² - dy/du * d²x/du²) / ((dx/du)² + (dy/du)²)^(3/2)
    numerator = dx_du * d2y_du2 - dy_du * d2x_du2
    denominator = (dx_du**2 + dy_du**2)**(3/2)
    curvature = numerator / denominator
    
    return curvature

def plot_example_curve():
    """Строит пример кривой с касательными векторами"""
    # Создаем простую параболу как пример
    x = np.linspace(-2, 2, 100)
    y = x**2
    
    fig = plt.figure(figsize=(10, 8))
    plt.plot(x, y, 'b-', label='Кривая')
    
    # Добавляем касательные векторы
    for xi in np.linspace(-1.5, 1.5, 5):
        yi = xi**2
        # Касательный вектор (1, 2x) / sqrt(1 + 4x²)
        dx = 1
        dy = 2*xi
        norm = np.sqrt(1 + 4*xi**2)
        plt.arrow(xi, yi, dx/norm, dy/norm,
                 color='r', head_width=0.1, head_length=0.1)
    
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.title('Пример кривой с касательными векторами')
    return fig

def create_report(canvas):
    """Создает PDF отчет с решением"""
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-3')
    
    # Часть 1а - явное представление
    canvas.drawString(50, 770, '1а. Для явного представления кривой (x, (x, y(x))):')
    canvas.drawString(50, 750, 'Касательный вектор T(x):')
    canvas.drawString(50, 730, 'T(x) = (1, dy/dx) / sqrt(1 + (dy/dx)²)')
    
    canvas.drawString(50, 700, 'Кривизна κ(x):')
    canvas.drawString(50, 680, 'κ(x) = d²y/dx² / (1 + (dy/dx)²)^(3/2)')
    
    # Часть 1б - параметрическое представление
    canvas.drawString(50, 650, '1б. Для параметрического представления (u, (x(u), y(u))):')
    canvas.drawString(50, 630, 'Касательный вектор T(u):')
    canvas.drawString(50, 610, 'T(u) = (dx/du, dy/du) / sqrt((dx/du)² + (dy/du)²)')
    
    canvas.drawString(50, 580, 'Кривизна κ(u):')
    canvas.drawString(50, 560, 'κ(u) = (dx/du * d²y/du² - dy/du * d²x/du²) / ((dx/du)² + (dy/du)²)^(3/2)')
    
    # Сохраняем график во временный файл
    fig = plot_example_curve()
    fig.savefig('temp_plot_3.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Добавляем график
    canvas.drawImage('temp_plot_3.png', 50, 150, width=500, height=400)
    
    canvas.showPage()
    
    # Вторая страница - доказательство некоммутативности S(2) и SO(2)
    canvas.setFont('Roboto', 14)
    canvas.drawString(50, 800, '2. Доказательство некоммутативности S(2) и SO(2)')
    
    canvas.setFont('Roboto', 12)
    y = 770
    for line in [
        'Рассмотрим конкретный пример:',
        '',
        '1) Пусть S ∈ S(2) - отражение относительно оси x:',
        '   S(x,y) = (x, -y)',
        '',
        '2) Пусть R ∈ SO(2) - поворот на угол θ:',
        '   R(x,y) = (x·cos θ - y·sin θ, x·sin θ + y·cos θ)',
        '',
        '3) Вычислим композиции SR и RS:',
        '',
        '   SR(x,y) = S(R(x,y)) = S(x·cos θ - y·sin θ, x·sin θ + y·cos θ) =',
        '           = (x·cos θ - y·sin θ, -(x·sin θ + y·cos θ))',
        '',
        '   RS(x,y) = R(S(x,y)) = R(x, -y) =',
        '           = (x·cos θ + y·sin θ, x·sin θ - y·cos θ)',
        '',
        '4) Сравним результаты:',
        '   В SR: первая координата = x·cos θ - y·sin θ',
        '        вторая координата = -(x·sin θ + y·cos θ)',
        '',
        '   В RS: первая координата = x·cos θ + y·sin θ',
        '        вторая координата = x·sin θ - y·cos θ',
        '',
        '5) Очевидно, что SR ≠ RS при θ ≠ 0',
        '   Следовательно, элементы групп S(2) и SO(2) в общем случае не коммутируют'
    ]:
        if line == '':
            y -= 10
        else:
            canvas.drawString(50, y, line)
            y -= 20
    
    # Добавляем визуальное представление
    y -= 30
    canvas.drawString(50, y, 'Геометрическая интерпретация:')
    y -= 20
    canvas.drawString(50, y, '- SR сначала поворачивает точку, затем отражает результат')
    y -= 20
    canvas.drawString(50, y, '- RS сначала отражает точку, затем поворачивает результат')
    y -= 20
    canvas.drawString(50, y, '- Эти операции дают разные результаты для общего случая')

if __name__ == "__main__":
    create_report() 