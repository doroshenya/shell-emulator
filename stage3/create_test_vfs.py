import zipfile

def create_test_vfs():
    with zipfile.ZipFile('test_vfs.zip', 'w') as zf:
        # Создаем файлы
        zf.writestr('file1.txt', 'Содержимое file1.txt')
        zf.writestr('readme.txt', 'README файл')
        zf.writestr('documents/note.txt', 'Заметка в documents')
        zf.writestr('documents/report.txt', 'Отчет в documents')
        # Явно создаем директории
        zf.writestr('documents/', '')
        zf.writestr('photos/', '')
        zf.writestr('work/', '')

if __name__ == "__main__":
    create_test_vfs()
    print("Тестовый VFS архив создан: test_vfs.zip")
