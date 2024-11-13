import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import io

def curve_point(u, a, b):
    """Вычисляет точку на кривой для заданного параметра u"""
    x = a * np.cos(u)
    y = b * (1 - np.exp(-u/2))
    return np.array([x, y])

def tangent_vector(u, a, b):
    """Вычисляет касательный вектор к кривой"""
    dx = -2 * a * np.sin(u)
    dy = b * np.exp(-u/2)
    norm = np.sqrt(4 * a**2 * np.sin(u)**2 + b**2 * np.exp(-u))
    return np.array([dx, dy]) / norm

def normal_vector(u, a, b):
    """Вычисляет нормальный вектор к кривой"""
    t = tangent_vector(u, a, b)
    # Поворачиваем касательный вектор на 90 градусов
    return np.array([-t[1], t[0]])

def plot_curve(a, b):
    """Строит кривую и векторы"""
    # Создаем массив параметра u
    u = np.linspace(0, 2*np.pi, 1000)
    
    # Вычисляем точки кривой
    points = np.array([curve_point(ui, a, b) for ui in u])
    
    # Создаем график
    plt.figure(figsize=(10, 10))
    plt.plot(points[:, 0], points[:, 1], 'b-', label='Кривая')
    
    # Добавляем несколько касательных и нормальных векторов
    u_samples = np.linspace(0, 2*np.pi, 8)
    for ui in u_samples:
        point = curve_point(ui, a, b)
        tangent = tangent_vector(ui, a, b)
        normal = normal_vector(ui, a, b)
        
        # Рисуем касательный вектор
        plt.arrow(point[0], point[1], tangent[0], tangent[1], 
                 color='r', head_width=0.1, head_length=0.1)
        
        # Рисуем нормальный вектор
        plt.arrow(point[0], point[1], normal[0], normal[1], 
                 color='g', head_width=0.1, head_length=0.1)
    
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.title('Кривая с касательными (красные) и нормалями (зеленые)')
    return plt.gcf()  # Возвращаем текущую фигуру

def create_report_simple(a, b, canvas):
    """Создает PDF отчет с использованием переданного canvas"""
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-1')
    
    # Условие
    canvas.drawString(50, 770, f'1. Плоская кривая определена формулой:')
    canvas.drawString(50, 750, f'(u, ((a*cos(u))i + b(1-e^(-u/2))j)), 0 ≤ u < ∞')
    canvas.drawString(50, 730, f'где a={a} и b={b} – действительные числа.')
    
    # Сохраняем график во временный файл
    fig = plot_curve(a, b)
    fig.savefig('temp_plot.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Добавляем график из файла
    canvas.drawImage('temp_plot.png', 50, 300, width=500, height=400)
    
    # Добавляем описание
    canvas.drawString(50, 280, 'На графике:')
    canvas.drawString(50, 260, '- Синяя линия - кривая')
    canvas.drawString(50, 240, '- Красные стрелки - касательные векторы')
    canvas.drawString(50, 220, '- Зеленые стрелки - нормальные векторы')
    
    canvas.showPage()
    
    # Вторая страница с доказательством
    canvas.setFont('Roboto', 12)
    canvas.drawString(50, 800, '2. Доказательство изоморфизма групп T(2) и R²:')
    y = 770
    for line in [
        '1. φ: T(2) → R² определяется как отображение, сопоставляющее',
        '   каждому движению плоскости вектор смещения начала координат.',
        '2. Это отображение является биекцией:',
        '   - Инъективность: разные движения дают разные векторы смещения',
        '   - Сюръективность: любой вектор смещения достижим некоторым движением',
        '3. φ сохраняет операцию: φ(x ∘ y) = φ(x) + φ(y)',
        'Следовательно, φ является изоморфизмом групп.'
    ]:
        canvas.drawString(50, y, line)
        y -= 20

if __name__ == "__main__":
    # Для локального тестирования
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("report_project_1.pdf", pagesize=A4)
    c.setFont('Roboto', 12)
    create_report_simple(2, 3, c)
    c.save()
