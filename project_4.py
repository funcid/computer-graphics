import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, diff, simplify, cos, sin, Matrix
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

def generate_rotation_surface(p, q, u_range, phi_range, n_points=50):
    """
    Генерирует точки поверхности вращения
    p(u) - радиус в плоскости XY
    q(u) - высота по оси Z
    """
    u = np.linspace(u_range[0], u_range[1], n_points)
    phi = np.linspace(0, 2*np.pi, n_points)
    
    # Создаем сетку параметров
    U, PHI = np.meshgrid(u, phi)
    
    # Вычисляем координаты точек поверхности
    X = p(U) * np.cos(PHI)
    Y = p(U) * np.sin(PHI)
    Z = q(U)
    
    return X, Y, Z

def plot_rotation_surface(p, q, u_range, title="Поверхность вращения"):
    """Строит поверхность вращения"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Генерируем поверхность
    X, Y, Z = generate_rotation_surface(p, q, u_range, (0, 2*np.pi))
    
    # Строим поверхность
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    
    # Добавляем цветовую шкалу
    fig.colorbar(surf)
    
    # Настраиваем вид
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    
    return fig

def verify_rotation_surface_equation():
    """
    Проверяет уравнение поверхности вращения символьно
    """
    # Определяем символьные переменные
    u, phi = symbols('u phi')
    p, q = symbols('p q', cls=lambda name: symbols(name)(u))
    
    # Параметрические уравнения поверхности
    x = p * cos(phi)
    y = p * sin(phi)
    z = q
    
    # Создаем матрицу поверхности
    surface_point = Matrix([x, y, z])
    
    return surface_point

def plot_cylinder_example():
    """Строит пример цилиндра"""
    # Определяем функции для цилиндра радиуса R
    R = 1
    p = lambda u: R
    q = lambda u: u
    
    # Строим цилиндр
    return plot_rotation_surface(p, q, (0, 2), "Цилиндр")

def create_report(canvas):
    """Создает PDF отчет с решением"""
    # Определяем диапазон параметров
    u_range = (0, 2*np.pi)
    
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-4')
    
    # Часть 1а - Поверхность вращения
    canvas.drawString(50, 770, '1а. Поверхность вращения кривой (u, (p(u)i + q(u)k)):')
    canvas.drawString(50, 750, 'При вращении вокруг оси OZ получаем:')
    canvas.drawString(50, 730, '((u, φ), (p(u)cos(φ)i + p(u)sin(φ)j + q(u)k))')
    canvas.drawString(50, 710, f'где {u_range[0]} ≤ u ≤ {u_range[1]}, 0 ≤ φ ≤ 2π')
    
    # Сохраняем график поверхности вращения
    fig = plot_rotation_surface(lambda u: np.sin(u), lambda u: u, u_range)
    fig.savefig('temp_plot_4a.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Добавляем график
    canvas.drawImage('temp_plot_4a.png', 50, 300, width=500, height=400)
    
    # Часть 1б - Цилиндр
    canvas.drawString(50, 280, '1б. Симметричное параметрическое представление цилиндра:')
    canvas.drawString(50, 260, 'p(u) = R (константа)')
    canvas.drawString(50, 240, 'q(u) = u')
    
    # Сохраняем график цилиндра
    fig = plot_cylinder_example()
    fig.savefig('temp_plot_4b.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    canvas.showPage()
    
    # Вторая страница - цилиндр
    canvas.drawImage('temp_plot_4b.png', 50, 400, width=500, height=400)
    
    # Доказательство для второй части
    canvas.setFont('Roboto', 12)
    canvas.drawString(50, 350, '2. Доказательство некоммутативности единицы S(2) с SO(2):')
    y = 320
    for line in [
        'Пусть E - единица в S(2) (отражение относительно оси x),',
        'и R(θ) - поворот на угол θ в SO(2).',
        '',
        'Тогда:',
        'E(x,y) = (x,-y)',
        'R(θ)(x,y) = (x·cos θ - y·sin θ, x·sin θ + y·cos θ)',
        '',
        'ER(θ)(x,y) = E(x·cos θ - y·sin θ, x·sin θ + y·cos θ) =',
        '           = (x·cos θ - y·sin θ, -(x·sin θ + y·cos θ))',
        '',
        'R(θ)E(x,y) = R(θ)(x,-y) =',
        '           = (x·cos θ + y·sin θ, x·sin θ - y·cos θ)',
        '',
        'ER(θ) ≠ R(θ)E, следовательно, единица S(2) не коммутирует с SO(2)'
    ]:
        if line == '':
            y -= 10
        else:
            canvas.setFont('Roboto', 12)
            canvas.drawString(50, y, line)
            y -= 20

if __name__ == "__main__":
    # Для локального тестирования
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("report_project_4.pdf", pagesize=A4)
    c.setFont('Roboto', 12)
    create_report(c)
    c.save() 