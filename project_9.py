import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, solve, Matrix, simplify, cos, sin
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

def find_normal_line():
    """Находит параметрическое уравнение нормали к плоскости"""
    # Коэффициенты плоскости 2x - y + z + 2 = 0
    a, b, c, d = 2, -1, 1, 2
    
    # Направляющий вектор нормали
    normal = np.array([a, b, c])
    normal = normal / np.linalg.norm(normal)  # нормализация
    
    # Точка пересечения с плоскостью (0, 0, z0)
    z0 = -d / c
    intersection_point = np.array([0, 0, z0])
    
    return intersection_point, normal

def plot_plane_and_normal():
    """Визуализирует плоскость и нормаль"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Создаем сетку точек для плоскости
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    # Из уравнения плоскости 2x - y + z + 2 = 0
    Z = -(2*X - Y + 2)
    
    # Строим плоскость
    surf = ax.plot_surface(X, Y, Z, alpha=0.5)
    
    # Получаем точку пересечения и направляющий вектор нормали
    point, normal = find_normal_line()
    
    # Строим нормаль
    t = np.linspace(-2, 2, 100)
    X_normal = point[0] + normal[0] * t[:, np.newaxis]
    Y_normal = point[1] + normal[1] * t[:, np.newaxis]
    Z_normal = point[2] + normal[2] * t[:, np.newaxis]
    
    ax.plot(X_normal, Y_normal, Z_normal, 'r-', linewidth=2, label='Нормаль')
    
    # Отмечаем точку пересечения
    ax.scatter([point[0]], [point[1]], [point[2]], color='g', s=100, label='Точка пересечения')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    
    return fig

def prove_isomorphism():
    """Доказывает изоморфизм подгрупп Sn и SO(2)"""
    # Определяем символьные переменные
    theta = symbols('theta')
    n1, n2, n3 = symbols('n1 n2 n3')
    
    # Матрица поворота в SO(2)
    R = Matrix([
        [cos(theta), -sin(theta)],
        [sin(theta), cos(theta)]
    ])
    
    # Свойства:
    # 1. det(R) = 1
    det_R = R.det()
    # 2. R * R.T = I
    orthogonality = R * R.transpose() - Matrix.eye(2)
    
    return R, det_R, simplify(orthogonality)

def create_report(canvas):
    """Создает PDF отчет с решением"""
    # Заголовок
    canvas.drawString(50, 800, 'Проект 1-9')
    
    # Часть 1 - Нормаль к плоскости
    canvas.drawString(50, 770, '1. Нормаль к плоскости 2x - y + z + 2 = 0:')
    
    # Получаем точку пересечения и направляющий вектор
    point, normal = find_normal_line()
    
    # Выводим результаты
    canvas.drawString(50, 750, 'а) Точка пересечения с осью OZ:')
    canvas.drawString(70, 730, f'P₀ = (0, 0, {-2})')
    
    canvas.drawString(50, 700, 'Параметрическое уравнение нормали:')
    canvas.drawString(70, 680, f'r(t) = ({point[0]}, {point[1]}, {point[2]}) + ')
    canvas.drawString(70, 660, f't·({normal[0]:.3f}, {normal[1]:.3f}, {normal[2]:.3f})')
    
    # Сохраняем график
    fig = plot_plane_and_normal()
    fig.savefig('temp_plot_9.png', format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Добавляем график
    canvas.drawImage('temp_plot_9.png', 50, 250, width=500, height=400)
    
    canvas.showPage()
    
    # Вторая страница - Изоморфизм подгрупп
    canvas.setFont('Roboto', 12)
    canvas.drawString(50, 800, '2. Доказательство изоморфизма Sn и SO(2):')
    
    y = 770
    for line in [
        'Доказательство:',
        '',
        '1) Sn = {Wn(θ): 0 ≤ θ < 2π} - подгруппа поворотов вокруг оси n',
        '',
        '2) SO(2) - группа поворотов плоскости',
        '',
        '3) Построим изоморфизм φ: Sn → SO(2):',
        '   φ(Wn(θ)) = R(θ), где R(θ) - матрица поворота на угол θ',
        '',
        '4) Проверим свойства изоморфизма:',
        '   - Инъективность: разные углы дают разные повороты',
        '   - Сюръективность: любой поворот SO(2) достижим',
        '   - Гомоморфизм: φ(Wn(θ₁)·Wn(θ₂)) = φ(Wn(θ₁))·φ(Wn(θ₂))',
        '',
        '5) Матрица поворота R(θ) в SO(2):',
        '   ⎡cos θ  -sin θ⎤',
        '   ⎣sin θ   cos θ⎦',
        '',
        '6) Свойства:',
        '   - det(R(θ)) = 1',
        '   - R(θ)·R(θ)ᵀ = I',
        '   - R(θ₁)·R(θ₂) = R(θ₁ + θ₂)',
        '',
        'Следовательно, Sn ≅ SO(2)'
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
    c = canvas.Canvas("report_project_9.pdf", pagesize=A4)
    c.setFont('Roboto', 12)
    create_report(c)
    c.save() 