import zipfile
import os

def create_test_vfs():
    #Создает тестовый VFS архив для этапа 4
   
    print("Создаем тестовый VFS архив...")
    
    with zipfile.ZipFile('test_vfs.zip', 'w') as zf:
        # Файлы в корне
        zf.writestr('file1.txt', 'Строка 1\nСтрока 2\nСтрока 3')
        zf.writestr('readme.txt', 'README файл\nВторая строка README\nТретья строка')
        zf.writestr('data.bin', b'binary_data_here_12345')
        
        # Файлы в поддиректориях
        zf.writestr('documents/note.txt', 'Заметка 1\nЗаметка 2\nЗаметка 3')
        zf.writestr('documents/report.txt', 'Отчет\nГлава 1\nГлава 2')
        zf.writestr('photos/avatar.jpg', b'fake_jpeg_data_56789')
        zf.writestr('work/project1/source.py', 'print("Hello")\nprint("World")\n# Конец файла')
        zf.writestr('work/project1/config.txt', 'host=localhost\nport=8080\ndebug=true')
        zf.writestr('work/project2/readme.txt', 'Project 2\nDescription here')
    
    print("Тестовый архив создан: test_vfs.zip")
    
    # Показываем содержимое
    print("\nСодержимое архива:")
    with zipfile.ZipFile('test_vfs.zip', 'r') as zf:
        for file_info in zf.infolist():
            print(f"  {file_info.filename}")

if __name__ == "__main__":
    create_test_vfs()
