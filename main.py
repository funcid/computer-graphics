from report_generator import ReportGenerator
import project_1
import project_2
import project_3
import project_4
import project_5
import project_6
import project_7
import project_8
import project_9
import project_10
import time
import os

def generate_full_report():
    """Генерация полного отчета"""
    report_gen = ReportGenerator()
    
    try:
        # Создаем временную директорию для изображений
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        # Генерируем все отчеты с использованием общего генератора
        canvas1, filepath1 = report_gen.create_new_canvas()
        project_1.create_report_simple(2, 3, canvas1)
        canvas1.save()
        
        canvas2, filepath2 = report_gen.create_new_canvas()
        project_2.create_report(2, 1, canvas2)
        canvas2.save()
        
        canvas3, filepath3 = report_gen.create_new_canvas()
        project_3.create_report(canvas3)
        canvas3.save()
        
        canvas4, filepath4 = report_gen.create_new_canvas()
        project_4.create_report(canvas4)
        canvas4.save()
        
        canvas5, filepath5 = report_gen.create_new_canvas()
        project_5.create_report(canvas5)
        canvas5.save()
        
        canvas6, filepath6 = report_gen.create_new_canvas()
        project_6.create_report(canvas6)
        canvas6.save()
        
        canvas7, filepath7 = report_gen.create_new_canvas()
        project_7.create_report(canvas7)
        canvas7.save()
        
        canvas8, filepath8 = report_gen.create_new_canvas()
        project_8.create_report(canvas8)
        canvas8.save()
        
        canvas9, filepath9 = report_gen.create_new_canvas()
        project_9.create_report(canvas9)
        canvas9.save()
        
        canvas10, filepath10 = report_gen.create_new_canvas()
        project_10.create_report(canvas10)
        canvas10.save()
        
        # Даем время на завершение записи файлов
        time.sleep(1)
        
        # Объединяем все отчеты в один файл
        report_gen.merge_reports()
        
    except Exception as e:
        print(f"Ошибка при генерации отчета: {str(e)}")
        raise
    
    finally:
        # Даем время на завершение всех операций
        time.sleep(1)
        # Очищаем временные файлы
        report_gen.cleanup()

if __name__ == "__main__":
    generate_full_report() 