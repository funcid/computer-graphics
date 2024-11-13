import matplotlib.pyplot as plt
from matplotlib import rc
import os
from io import BytesIO
import matplotlib
matplotlib.use('Agg')

def setup_latex():
    """Настраивает поддержку LaTeX в matplotlib"""
    rc('text', usetex=True)
    rc('font', family='serif')
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}\usepackage{amssymb}'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titlesize'] = 10

def save_figure_to_temp(fig, filename, dpi=300):
    """Сохраняет фигуру во временный файл"""
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    filepath = os.path.join(temp_dir, filename)
    fig.savefig(filepath, format='png', bbox_inches='tight', dpi=dpi)
    plt.close(fig)
    return filepath

def render_latex_to_file(formula, filename, fontsize=12, dpi=300):
    """Рендерит LaTeX формулу в файл с улучшенным качеством"""
    setup_latex()
    
    # Создаем фигуру с прозрачным фоном и меньшим размером
    fig = plt.figure(figsize=(4, 0.3))
    fig.patch.set_alpha(0.0)
    
    # Добавляем текст с выравниванием по центру
    fig.text(0.5, 0.5, f'${formula}$', 
             fontsize=fontsize, 
             horizontalalignment='center',
             verticalalignment='center',
             usetex=True)
    
    # Сохраняем в файл с высоким разрешением
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    filepath = os.path.join(temp_dir, filename)
    
    # Увеличиваем DPI для компенсации меньшего размера
    fig.savefig(filepath, 
                format='png',
                dpi=dpi,
                bbox_inches='tight',
                pad_inches=0.02,
                transparent=True,
                facecolor='none')
    plt.close(fig)
    return filepath

def cleanup_temp_files():
    """Удаляет временные файлы"""
    temp_dir = 'temp'
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir) 