import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, diff, simplify, cos, sin, Matrix, eye, expand
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

def generate_cone_surface(h, r, u_range, phi_range, n_points=50):
    """
    Генерирует точки конической поверхности
    h - высота конуса
    r - радиус основания
    """
    u = np.linspace(u_range[0], u_range[1], n_points)
    phi = np.linspace(phi_range[0], phi_range[1], n_points)
    
    # Создаем сетку параметров
    U, PHI = np.meshgrid(u, phi)
    
    # Параметрические уравнения конуса
    X = (r * U / h) * np.cos(PHI)
    Y = (r * U / h) * np.sin(PHI)
    Z = U
    
    return X, Y, Z

def plot_cone(h, r):
    """Строит коническую поверхность"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Генерируем поверхность конуса
    X, Y, Z = generate_cone_surface(h, r, (0, h), (0, 2*np.pi))
    
    # Строим поверхность
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    
    # Добавляем цветовую шкалу
    fig.colorbar(surf)
    
    # Настраиваем вид
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Коническая поверхность')
    
    return fig

def calculate_An_matrix():
    """Вычисляет матрицу An для векторного произведения"""
    # Определяем символьные переменные
    n1, n2, n3 = symbols('n1 n2 n3')
    n = Matrix([n1, n2, n3])
    
    # Создаем кососимметрическую матрицу для векторного произведения
    An = Matrix([
        [0, -n3, n2],
        [n3, 0, -n1],
        [-n2, n1, 0]
    ])
    
    return An, n

def calculate_rotation_matrix():
    """Вычисляет матрицу поворота Wn(θ)"""
    theta = symbols('theta')
    An, n = calculate_An_matrix()
    
    # Формула Родрига: Wn(θ) = I + (1-cos θ)An² + sin θ An
    I = eye(3)
    An_squared = An * An
    
    Wn = I + (1 - cos(theta)) * An_squared + sin(theta) * An
    
    return expand(Wn)

def create_report(canvas):
    """Создает PDF отчет с решением"""
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-5')
    
    # Часть 1а - Поверхность вращения
    canvas.drawString(50, 770, '1а. Поверхность вращения кривой (u, (p(u)i + q(u)k)):')
    canvas.drawString(50, 750, 'При вращении вокруг оси OZ получаем:')
    canvas.drawString(50, 730, '((u, φ), (p(u)cos(φ)i + p(u)sin(φ)j + q(u)k))')
    canvas.drawString(50, 710, '0 ≤ φ ≤ 2π')
    
    # Часть 1б - Конус
    canvas.drawString(50, 680, '1б. Параметрическое представление конуса:')
    canvas.drawString(50, 660, 'p(u) = ru/h')
    canvas.drawString(50, 640, 'q(u) = u')
    canvas.drawString(50, 620, 'где h - высота конуса, r - радиус основания')
    
    # Сохраняем график конуса
    fig = plot_cone(2, 1)
    fig.savefig('temp_plot_5.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Добавляем график
    canvas.drawImage('temp_plot_5.png', 50, 200, width=500, height=400)
    
    canvas.showPage()
    
    # Вторая страница - Матричные преобразования
    canvas.setFont('Roboto', 12)
    canvas.drawString(50, 800, '2. Матричные преобразования в R³:')
    
    # Получаем матрицы
    An, n = calculate_An_matrix()
    Wn = calculate_rotation_matrix()
    
    y = 770
    canvas.drawString(50, y, 'а) Матрица An для векторного произведения n × r:')
    y -= 30
    
    # Выводим матрицу An в более простом формате
    matrix_rows = [
        '⎡  0   -n3   n2  ⎤',
        '⎢  n3    0   -n1 ⎥',
        '⎣ -n2   n1    0  ⎦'
    ]
    
    for row in matrix_rows:
        canvas.drawString(70, y, row)
        y -= 20
    
    y -= 20
    canvas.drawString(50, y, 'где n = (n1, n2, n3) - заданный вектор')
    y -= 40
    
    canvas.drawString(50, y, 'б) Матрица поворота Wn(θ):')
    y -= 30
    
    # Выводим формулу для Wn
    canvas.drawString(70, y, 'Wn(θ) = I + (1-cos θ)An² + sin θ An')
    y -= 40
    
    # Выводим развернутую матрицу Wn в более простом формате
    canvas.drawString(50, y, 'Развернутая матрица поворота:')
    y -= 30
    
    # Получаем матрицу Wn
    Wn = calculate_rotation_matrix()
    
    # Разбиваем каждый элемент матрицы на строки фиксированной длины
    for row in Wn.tolist():
        elements = []
        for elem in row:
            # Преобразуем элемент в строку и разбиваем на части
            elem_str = str(elem)
            if len(elem_str) > 60:
                parts = [elem_str[i:i+60] for i in range(0, len(elem_str), 60)]
                elements.extend(parts)
            else:
                elements.append(elem_str)
        
        # Выводим элементы матрицы
        for element in elements:
            canvas.drawString(70, y, element)
            y -= 20
        y -= 10  # Дополнительный отступ между строками матрицы

if __name__ == "__main__":
    # Для локального тестирования
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("report_project_5.pdf", pagesize=A4)
    c.setFont('Roboto', 12)
    create_report(c)
    c.save() 