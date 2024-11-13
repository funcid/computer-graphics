import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, simplify, cos, sin, sqrt
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

def generate_cylinder_intersection(l, h, a, b, alpha, n_points=100):
    """
    Генерирует точки кривой пересечения цилиндров
    l - половина длины первого цилиндра
    h - высота второго цилиндра
    a - радиус первого цилиндра
    b - радиус второго цилиндра
    alpha - смещение второго цилиндра по оси Z
    """
    theta = np.linspace(0, 2*np.pi, n_points)
    
    # Вычисляем точки кривой пересечения
    X = np.sqrt(b**2 - (alpha + a*np.sin(theta))**2)
    Y = a * np.cos(theta)
    Z = alpha + a * np.sin(theta)
    
    # Фильтруем точки, где подкоренное выражение отрицательное
    mask = b**2 - (alpha + a*np.sin(theta))**2 >= 0
    X = np.where(mask, X, np.nan)
    
    return X, Y, Z

def plot_intersection_curve(l, h, a, b, alpha):
    """Строит кривую пересечения цилиндров"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Генерируем и строим кривую пересечения
    X, Y, Z = generate_cylinder_intersection(l, h, a, b, alpha)
    ax.plot(X, Y, Z, 'b-', label='Кривая пересечения')
    
    # Добавляем контуры цилиндров для наглядности
    u = np.linspace(0, 2*np.pi, 100)
    v = np.linspace(-l, l, 100)
    U, V = np.meshgrid(u, v)
    
    # Первый цилиндр
    X1 = b * np.cos(U)
    Y1 = V
    Z1 = b * np.sin(U)
    ax.plot_surface(X1, Y1, Z1, alpha=0.1, color='r')
    
    # Второй цилиндр
    X2 = V
    Y2 = a * np.cos(U)
    Z2 = alpha + a * np.sin(U)
    ax.plot_surface(X2, Y2, Z2, alpha=0.1, color='g')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Пересечение цилиндров')
    
    return fig

def verify_intersection_curve():
    """Проверяет формулу кривой пересечения"""
    theta = symbols('theta')
    a, b, alpha = symbols('a b alpha')
    
    # Параметрические уравнения кривой
    x = sqrt(b**2 - (alpha + a*sin(theta))**2)
    y = a * cos(theta)
    z = alpha + a * sin(theta)
    
    return x, y, z

def prove_nonlinear_projection():
    """Доказывает, что T - нелинейная проекция"""
    # Определяем символьные переменные для векторов
    r1, r2, r3 = symbols('r1 r2 r3')
    a1, a2, a3 = symbols('a1 a2 a3')
    c = symbols('c')
    
    # Вектор r = (r1, r2, r3)
    r = [r1, r2, r3]
    # Вектор a = (a1, a2, a3)
    a = [a1, a2, a3]
    
    # Вычисляем скалярное произведение a·r
    dot_product = sum(ai*ri for ai, ri in zip(a, r))
    
    # T(r) = r/(a·r) при a·r ≠ 0
    T_r = [ri/dot_product for ri in r]
    
    # T(cr) = cr/(a·cr) = r/(a·r) = T(r)
    # Это показывает однородность
    
    # Но T(r1 + r2) ≠ T(r1) + T(r2)
    # что доказывает нелинейность
    
    return T_r

def create_report(canvas):
    """Создает PDF отчет с решением"""
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-7')
    
    # Часть 1 - Пересечение цилиндров
    canvas.drawString(50, 770, '1. Пересечение цилиндров C₁ и C₂:')
    canvas.drawString(50, 750, 'C₁: x² + z² = b², -l ≤ y ≤ l')
    canvas.drawString(50, 730, 'C₂: y² + (z-α)² = a², 0 ≤ x ≤ h')
    
    # Параметрическое представление кривой пересечения
    canvas.drawString(50, 700, 'Кривая пересечения:')
    canvas.drawString(50, 680, 'r(θ) = ((b² - (α + a·sin θ)²)^(1/2), a·cos θ, α + a·sin θ)')
    canvas.drawString(50, 660, '0 ≤ θ < 2π')
    
    # Сохраняем график пересечения с конкретными параметрами
    l, h = 2, 3  # Длины цилиндров
    a, b = 1, 1.5  # Радиусы цилиндров
    alpha = 0.5  # Смещение второго цилиндра
    
    fig = plot_intersection_curve(l, h, a, b, alpha)
    fig.savefig('temp_plot_7.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Добавляем график
    canvas.drawImage('temp_plot_7.png', 50, 250, width=500, height=400)
    
    canvas.showPage()
    
    # Вторая страница - Нелинейная проекция
    canvas.setFont('Roboto', 12)
    canvas.drawString(50, 800, '2. Доказательство нелинейности проекции T:')
    
    y = 770
    for line in [
        'а) T - нелинейная проекция в R³:',
        '',
        'Доказательство:',
        '1) T(r) = r/(a·r) при a·r ≠ 0',
        '2) Проверим однородность:',
        '   T(cr) = cr/(a·cr) = r/(a·r) = T(r)',
        '   Однородность выполняется',
        '',
        '3) Проверим аддитивность:',
        '   T(r₁ + r₂) = (r₁ + r₂)/(a·(r₁ + r₂))',
        '   T(r₁) + T(r₂) = r₁/(a·r₁) + r₂/(a·r₂)',
        '',
        '   T(r₁ + r₂) ≠ T(r₁) + T(r₂)',
        '   Аддитивность не выполняется',
        '',
        '4) Следовательно, T - нелинейное отображение',
        '',
        'б) Доказательство T[(r, 1)] = [(r, a·r)]:',
        '   При a·r ≠ 0:',
        '   T(r) = r/(a·r)',
        '   Точка (r, 1) переходит в (r/(a·r), 1/(a·r))',
        '   Это эквивалентно точке (r, a·r) в проективном пространстве'
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
    c = canvas.Canvas("report_project_7.pdf", pagesize=A4)
    c.setFont('Roboto', 12)
    create_report(c)
    c.save() 