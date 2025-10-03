import os
import sys
import getpass
import socket
import argparse
import zipfile

class VFS:
    #Виртуальная файловая система на основе ZIP-архива
    
    def __init__(self, zip_path=None):
        self.files = {}  # путь -> содержимое
        self.dirs = set(['/'])  # множество директорий
        self.current_path = "/"
        self.metadata = {}  # метаданные файлов и директорий (ЭТАП 5)
        
        # Инициализируем метаданные для корневой директории
        self.metadata['/'] = {'owner': 'root', 'group': 'root'}
        
        if zip_path:
            self.load_vfs(zip_path)

    def load_vfs(self, zip_path):
        #Загружает VFS из ZIP-архива в память
        print(f"Загрузка VFS из: {zip_path}")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Собираем все директории
                all_dirs = set(['/'])
                for file_info in zip_file.infolist():
                    path = file_info.filename
                    
                    # Добавляем родительские директории
                    dir_path = os.path.dirname(path)
                    while dir_path:
                        all_dirs.add(dir_path + '/')
                        dir_path = os.path.dirname(dir_path)
                
                self.dirs.update(all_dirs)
                
                # Инициализируем метаданные для всех директорий (ЭТАП 5)
                for directory in self.dirs:
                    if directory not in self.metadata:
                        self.metadata[directory] = {'owner': 'root', 'group': 'root'}
                
                # Загружаем файлы
                for file_info in zip_file.infolist():
                    if not file_info.is_dir():
                        path = file_info.filename
                        with zip_file.open(file_info) as f:
                            content = f.read()
                        self.files[path] = content
                        # Инициализируем метаданные для файлов (ЭТАП 5)
                        self.metadata[path] = {'owner': 'root', 'group': 'root'}
            
            print(f"VFS загружена: {len(self.files)} файлов, {len(self.dirs)} директорий")
            
        except Exception as e:
            print(f"ОШИБКА загрузки VFS: {e}")
            sys.exit(1)

    def list_directory(self):
        #Возвращает содержимое текущей директории
        contents = []
        current = self.current_path.rstrip('/') or '/'
        
        # Ищем файлы в текущей директории
        for file_path in self.files:
            file_dir = os.path.dirname(file_path) or '/'
            if file_dir == current:
                contents.append({
                    'name': os.path.basename(file_path), 
                    'type': 'file',
                    'metadata': self.metadata.get(file_path, {'owner': 'root', 'group': 'root'})
                })
        
        # Ищем поддиректории
        for dir_path in self.dirs:
            if dir_path == '/':
                continue
            dir_parent = os.path.dirname(dir_path.rstrip('/')) or '/'
            if dir_parent == current:
                dir_name = os.path.basename(dir_path.rstrip('/'))
                contents.append({
                    'name': dir_name, 
                    'type': 'dir',
                    'metadata': self.metadata.get(dir_path, {'owner': 'root', 'group': 'root'})
                })
        
        return sorted(contents, key=lambda x: (x['type'] != 'dir', x['name']))

    def change_directory(self, path):
        #Изменяет текущую директорию в VFS
     
        if not path or path == '~':
            self.current_path = '/'
            return True
            
        if path == '/':
            self.current_path = '/'
            return True
            
        # Абсолютный путь
        if path.startswith('/'):
            target = path
        else:
            # Относительный путь
            if self.current_path == '/':
                target = path
            else:
                target = self.current_path.rstrip('/') + '/' + path
        
        # Нормализуем путь
        normalized = os.path.normpath(target).replace('\\', '/')
        
        # Для директорий добавляем / в конец
        if not normalized.endswith('/'):
            normalized += '/'
            
        # Проверяем существует ли директория
        if normalized in self.dirs:
            self.current_path = normalized
            return True
            
        return False

    def _resolve_path(self, file_path):
        #Преобразует относительный путь в абсолютный путь в VFS
    
        if file_path.startswith('/'):
            # Абсолютный путь
            return file_path
        else:
            # Относительный путь
            current = self.current_path.rstrip('/') or '/'
            if current == '/':
                return file_path
            else:
                return current.rstrip('/') + '/' + file_path

    def read_file(self, file_path):
        #Читает содержимое файла из VFS
        
        resolved_path = self._resolve_path(file_path)
        
        if resolved_path in self.files:
            content = self.files[resolved_path]
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                return "[Бинарный файл]"
        return None

    def get_file_size(self, file_path):
        #Возвращает размер файла в VFS
        
        resolved_path = self._resolve_path(file_path)
        
        if resolved_path in self.files:
            return len(self.files[resolved_path])
        return 0

    def file_exists(self, file_path):
        #Проверяет существует ли файл в VFS
        resolved_path = self._resolve_path(file_path)
        return resolved_path in self.files

    def dir_exists(self, dir_path):
        #Проверяет существует ли директория в VFS (ЭТАП 5)
        resolved_path = self._resolve_path(dir_path)
        if not resolved_path.endswith('/'):
            resolved_path += '/'
        return resolved_path in self.dirs

    def calculate_directory_size(self, dir_path=None):
        #Вычисляет общий размер файлов в директории (рекурсивно)
        if dir_path is None:
            dir_path = self.current_path.rstrip('/') or '/'
        
        total_size = 0
        
        # Считаем файлы в текущей директории
        for file_path, content in self.files.items():
            file_dir = os.path.dirname(file_path) or '/'
            if file_dir == dir_path:
                total_size += len(content)
        
        # Рекурсивно считаем поддиректории
        for directory in self.dirs:
            if directory == '/':
                continue
            dir_parent = os.path.dirname(directory.rstrip('/')) or '/'
            if dir_parent == dir_path:
                dir_name = directory.rstrip('/')
                total_size += self.calculate_directory_size(dir_name)
        
        return total_size

    def change_owner(self, path, owner, group=None):
        #Изменяет владельца файла или директории (ЭТАП 5)
        resolved_path = self._resolve_path(path)
        
        # Проверяем файл
        if resolved_path in self.files:
            self.metadata[resolved_path]['owner'] = owner
            if group:
                self.metadata[resolved_path]['group'] = group
            return True
        
        # Проверяем директорию
        dir_path = resolved_path
        if not dir_path.endswith('/'):
            dir_path += '/'
        
        if dir_path in self.dirs:
            self.metadata[dir_path]['owner'] = owner
            if group:
                self.metadata[dir_path]['group'] = group
            return True
        
        return False

    def get_metadata(self, path):
        #Возвращает метаданные файла или директории (ЭТАП 5)
        resolved_path = self._resolve_path(path)
        
        # Проверяем файл
        if resolved_path in self.files:
            return self.metadata.get(resolved_path, {'owner': 'root', 'group': 'root'})
        
        # Проверяем директорию
        dir_path = resolved_path
        if not dir_path.endswith('/'):
            dir_path += '/'
        
        if dir_path in self.dirs:
            return self.metadata.get(dir_path, {'owner': 'root', 'group': 'root'})
        
        return None

def run_script(script_path, vfs):
    #Выполняет стартовый скрипт с поддержкой VFS
    print(f"Выполнение скрипта: {script_path}")
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            username = getpass.getuser()
            hostname = socket.gethostname()
            current_path = vfs.current_path.rstrip('/') or '/'
            prompt = f"{username}@{hostname}:{current_path}$ "
            print(prompt + line)
            
            success = execute_command(line, vfs, is_script=True)
            
            if not success:
                print(f"ОШИБКА: Остановка скрипта на строке {line_num}")
                return False
        
        print("Скрипт успешно выполнен")
        return True
        
    except FileNotFoundError:
        print(f"ОШИБКА: Скрипт '{script_path}' не найден")
        return False
    except Exception as e:
        print(f"ОШИБКА при выполнении скрипта: {e}")
        return False

def execute_command(cmd, vfs, is_script=False):
    #Выполняет команду с поддержкой VFS
    parts = cmd.split()
    if not parts:
        return True
    
    command = parts[0]
    args = parts[1:]

    try:
        if command == "exit":
            if is_script:
                return True
            else:
                print("Выход из эмулятора")
                sys.exit(0)

        elif command == "ls":
            show_long = '-l' in args
            contents = vfs.list_directory()
            if not contents:
                print("Директория пуста")
            else:
                if show_long:
                    print("Type\tOwner\tGroup\tSize\tName")
                    for item in contents:
                        metadata = item['metadata']
                        item_type = 'dir' if item['type'] == 'dir' else 'file'
                        size = vfs.get_file_size(item['name']) if item_type == 'file' else 0
                        print(f"{item_type}\t{metadata['owner']}\t{metadata['group']}\t{size}\t{item['name']}")
                else:
                    for item in contents:
                        if item['type'] == 'dir':
                            print(f"{item['name']}/")
                        else:
                            print(item['name'])
            return True

        elif command == "cd":
            target = args[0] if args else "~"
            if vfs.change_directory(target):
                return True
            else:
                print(f"cd: {target}: Нет такой директории")
                return False

        elif command == "pwd":
            current = vfs.current_path.rstrip('/') or '/'
            print(current)
            return True

        elif command == "tac":
            if not args:
                print("tac: не указан файл")
                return False
            
            if vfs.file_exists(args[0]):
                content = vfs.read_file(args[0])
                if content != "[Бинарный файл]":
                    lines = content.split('\n')
                    for line in reversed(lines):
                        if line:  # Не выводить пустые строки
                            print(line)
                else:
                    print(content)
            else:
                print(f"tac: {args[0]}: Нет такого файла")
                return False
            return True

        elif command == "du":
            if args:
                # Показать размер конкретного файла или директории
                target = args[0]
                
                # Проверяем файл
                if vfs.file_exists(target):
                    size = vfs.get_file_size(target)
                    print(f"{size}\t{target}")
                    return True
                
                # Проверяем директорию
                if vfs.dir_exists(target):
                    total_size = vfs.calculate_directory_size(target)
                    print(f"{total_size}\t{target}")
                    return True
                else:
                    print(f"du: {target}: Нет такого файла или директории")
                    return False
            else:
                # Показать размер текущей директории и её содержимого
                contents = vfs.list_directory()
                current_dir = vfs.current_path.rstrip('/') or '/'
                
                # Размер текущей директории
                total_size = vfs.calculate_directory_size()
                print(f"{total_size}\t.")
                
                # Размеры файлов и поддиректорий
                for item in contents:
                    if item['type'] == 'file':
                        size = vfs.get_file_size(item['name'])
                        print(f"{size}\t{item['name']}")
                    else:
                        dir_path = os.path.join(current_dir, item['name']).replace('\\', '/')
                        size = vfs.calculate_directory_size(dir_path)
                        print(f"{size}\t{item['name']}")
            
            return True

        # КОМАНДА CHOWN - изменяет владельца файла или директории (ЭТАП 5)
        elif command == "chown":
            if len(args) < 2:
                print("chown: использование: chown владелец[:группа] файл...")
                return False
            
            owner_spec = args[0]
            targets = args[1:]
            
            # Разбираем спецификацию владельца
            if ':' in owner_spec:
                owner, group = owner_spec.split(':', 1)
            else:
                owner = owner_spec
                group = None
            
            success_count = 0
            for target in targets:
                if vfs.file_exists(target) or vfs.dir_exists(target):
                    if vfs.change_owner(target, owner, group):
                        success_count += 1
                    else:
                        print(f"chown: не удалось изменить владельца '{target}'")
                else:
                    print(f"chown: {target}: Нет такого файла или директории")
            
            return success_count > 0

        else:
            print(f"{command}: команда не найдена")
            return False

    except Exception as e:
        print(f"ОШИБКА при выполнении команды: {e}")
        return False

def main():
    #Основная функция с поддержкой VFS
    parser = argparse.ArgumentParser(description='Эмулятор командной оболочки OS')
    parser.add_argument('--vfs', type=str, help='Путь к ZIP-архиву с VFS')
    parser.add_argument('--script', type=str, help='Путь к стартовому скрипту')
    
    args = parser.parse_args()
    
    print("Отладочный вывод параметров")
    print(f"VFS: '{args.vfs}'")
    print(f"Script: '{args.script}'")
    # Инициализация VFS
    vfs = VFS(args.vfs)
    
    if args.script:
        success = run_script(args.script, vfs)
        if not success:
            sys.exit(1)
    else:
        username = getpass.getuser()
        hostname = socket.gethostname()
        
        print("Эмулятор командной оболочки (Этап 5). Введите 'exit' для выхода.")
        
        while True:
            current_path = vfs.current_path.rstrip('/') or '/'
            prompt = f"{username}@{hostname}:{current_path}$ "
            
            try:
                user_input = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nВыход из эмулятора")
                break
                
            if not user_input:
                continue
                
            execute_command(user_input, vfs)

if __name__ == "__main__":
    main()
