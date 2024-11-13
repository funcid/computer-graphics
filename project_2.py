import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, simplify, cos, sin
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import io

def curve_point(u, a, b):
    """Вычисляет точку на кривой для заданного параметра u"""
    x = a * np.cos(u)
    y = a * np.sin(u)
    z = b * u
    return np.array([x, y, z])

def tangent_vector(u, a, b):
    """Вычисляет касательный вектор к кривой"""
    dx = -a * np.sin(u)
    dy = a * np.cos(u)
    dz = b
    norm = np.sqrt(dx**2 + dy**2 + dz**2)
    return np.array([dx, dy, dz]) / norm

def calculate_curvature_symbolic():
    """Вычисляет кривизну кривой символьно"""
    # Определяем символьные переменные
    u, a, b = symbols('u a b')
    
    # Определяем параметрические уравнения кривой
    x = a * cos(u)
    y = a * sin(u)
    z = b * u
    
    # Вычисляем первые производные
    dx = diff(x, u)
    dy = diff(y, u)
    dz = diff(z, u)
    
    # Вычисляем вторые производные
    d2x = diff(dx, u)
    d2y = diff(dy, u)
    d2z = diff(dz, u)
    
    # Вычисляем векторное произведение r' × r''
    cross_product = [
        dy*d2z - dz*d2y,
        dz*d2x - dx*d2z,
        dx*d2y - dy*d2x
    ]
    
    # Вычисляем норму векторного произведения
    cross_norm = simplify((sum(cp**2 for cp in cross_product))**0.5)
    
    # Вычисляем норму вектора скорости в кубе
    velocity_norm = simplify((dx**2 + dy**2 + dz**2)**(3/2))
    
    # Кривизна
    curvature = cross_norm / velocity_norm
    
    return simplify(curvature)

def plot_3d_curve(a, b):
    """Строит трехмерную кривую с касательными векторами"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Создаем массив параметра u
    u = np.linspace(-2*np.pi, 2*np.pi, 1000)
    
    # Вычисляем точки кривой
    points = np.array([curve_point(ui, a, b) for ui in u])
    
    # Строим кривую
    ax.plot(points[:, 0], points[:, 1], points[:, 2], 'b-', label='Кривая')
    
    # Добавляем касательные векторы
    u_samples = np.linspace(-2*np.pi, 2*np.pi, 8)
    for ui in u_samples:
        point = curve_point(ui, a, b)
        tangent = tangent_vector(ui, a, b)
        
        # Рисуем касательный вектор
        ax.quiver(point[0], point[1], point[2],
                 tangent[0], tangent[1], tangent[2],
                 color='r', length=1.0)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Винтовая линия с касательными векторами')
    plt.legend()
    return fig

def create_report(a, b, canvas):
    """Создает PDF отчет с решением"""
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-2')
    
    # Условие
    canvas.drawString(50, 770, '1. Кривая задана параметрически:')
    canvas.drawString(50, 750, f'(u, (a*cos(u), a*sin(u), b*u)), -∞ < u < ∞')
    canvas.drawString(50, 730, f'где a={a} и b={b}')
    
    # Касательный вектор
    canvas.drawString(50, 700, 'Касательный вектор T(u):')
    canvas.drawString(50, 680, '(-a*sin(u), a*cos(u), b) / sqrt(a² + b²)')
    
    # Сохраняем график во временный файл
    fig = plot_3d_curve(a, b)
    fig.savefig('temp_plot_3d.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Добавляем график из файла
    canvas.drawImage('temp_plot_3d.png', 50, 250, width=500, height=400)
    
    # Кривизна
    canvas.drawString(50, 230, 'Кривизна κ(u):')
    canvas.drawString(50, 210, f'κ = a/(a² + b²) = const')
    canvas.drawString(50, 190, 'Кривизна постоянна и зависит только от a и b')
    
    canvas.showPage()
    
    # Вторая страница - доказательство для S(2)
    canvas.setFont('Roboto', 12)
    canvas.drawString(50, 800, '2. Доказательство коммутативности S(2):')
    y = 770
    for line in [
        'S(2) - подгруппа линейных преобразований R².',
        'Для любых A, B ∈ S(2):',
        '1) AB и BA - линейные преобразования',
        '2) det(AB) = det(A)det(B) = 1',
        '3) (AB)ᵀ(AB) = I',
        'Следовательно, S(2) - коммутативная подгруппа.'
    ]:
        canvas.drawString(50, y, line)
        y -= 20

if __name__ == "__main__":
    # Для локального тестирования
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("report_project_2.pdf", pagesize=A4)
    c.setFont('Roboto', 12)
    create_report(2, 1, c)
    c.save() 