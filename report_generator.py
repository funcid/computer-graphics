from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfMerger, PdfReader
import os

class ReportGenerator:
    def __init__(self):
        """Инициализация генератора отчетов"""
        self.setup_fonts()
        self.temp_dir = 'temp'
        self.ensure_temp_dir()
        self.current_page = 1
        
    def setup_fonts(self):
        """Настройка шрифтов"""
        pdfmetrics.registerFont(TTFont('Roboto', 'RobotoMono[wght].ttf'))
        
    def ensure_temp_dir(self):
        """Создание временной директории"""
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            
    def create_new_canvas(self):
        """Создание нового PDF холста"""
        filepath = os.path.join(self.temp_dir, f'page_{self.current_page}.pdf')
        self.current_page += 1
        c = canvas.Canvas(filepath, pagesize=A4)
        c.setFont('Roboto', 12)
        return c, filepath
    
    def merge_reports(self, output_filename='computer_graphics_report.pdf'):
        """Объединение всех PDF файлов в один"""
        merger = PdfMerger()
        
        try:
            # Собираем все PDF файлы из временной директории
            pdf_files = sorted([f for f in os.listdir(self.temp_dir) if f.endswith('.pdf')])
            
            # Добавляем каждый файл в merger
            for pdf in pdf_files:
                filepath = os.path.join(self.temp_dir, pdf)
                with open(filepath, 'rb') as file:
                    merger.append(PdfReader(file))
            
            # Сохраняем объединенный файл
            with open(output_filename, 'wb') as output:
                merger.write(output)
                
        except Exception as e:
            print(f"Ошибка при объединении PDF: {str(e)}")
            raise
        finally:
            merger.close()
    
    def cleanup(self):
        """Очистка временных файлов"""
        try:
            if os.path.exists(self.temp_dir):
                for file in os.listdir(self.temp_dir):
                    try:
                        os.remove(os.path.join(self.temp_dir, file))
                    except Exception as e:
                        print(f"Ошибка при удалении файла {file}: {str(e)}")
                os.rmdir(self.temp_dir)
        except Exception as e:
            print(f"Ошибка при очистке временных файлов: {str(e)}") 