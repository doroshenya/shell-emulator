import os
import sys
import getpass
import socket
import argparse
import zipfile
import base64

class VFS:
    def __init__(self, zip_path=None):
        self.files = {}
        self.dirs = set(['/'])
        self.current_path = "/"
        
        if zip_path:
            self.load_vfs(zip_path)

    def load_vfs(self, zip_path):
        print(f"Загрузка VFS из: {zip_path}")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                all_dirs = set(['/'])
                for file_info in zip_file.infolist():
                    path = file_info.filename
                    
                    dir_path = os.path.dirname(path)
                    while dir_path:
                        all_dirs.add(dir_path + '/')
                        dir_path = os.path.dirname(dir_path)
                
                self.dirs.update(all_dirs)
                
                for file_info in zip_file.infolist():
                    if not file_info.is_dir():
                        path = file_info.filename
                        with zip_file.open(file_info) as f:
                            content = f.read()
                        
                        binary_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', 
                                           '.pdf', '.exe', '.dll', '.so', '.bin',
                                           '.zip', '.rar', '.mp3', '.mp4', '.avi')
                        if any(path.lower().endswith(ext) for ext in binary_extensions):
                            content = base64.b64encode(content).decode('utf-8')
                            self.files[path] = f"base64:{content}"
                        else:
                            try:
                                text_content = content.decode('utf-8')
                                self.files[path] = text_content
                            except UnicodeDecodeError:
                                content = base64.b64encode(content).decode('utf-8')
                                self.files[path] = f"base64:{content}"
            
            print(f"VFS загружена: {len(self.files)} файлов, {len(self.dirs)} директорий")
            
        except Exception as e:
            print(f"ОШИБКА загрузки VFS: {e}")
            sys.exit(1)

    def _resolve_path(self, file_path):
        if file_path.startswith('/'):
            return file_path
        else:
            current = self.current_path.rstrip('/') or '/'
            if current == '/':
                return file_path
            else:
                return current.rstrip('/') + '/' + file_path

    def read_file(self, file_path):
        resolved_path = self._resolve_path(file_path)
        
        if resolved_path in self.files:
            content = self.files[resolved_path]
            if isinstance(content, str) and content.startswith('base64:'):
                try:
                    decoded = base64.b64decode(content[7:])
                    return decoded.decode('utf-8', errors='ignore')
                except:
                    return "[Бинарный файл]"
            else:
                return content
        return None

    def file_exists(self, file_path):
        resolved_path = self._resolve_path(file_path)
        return resolved_path in self.files

    def get_file_size(self, file_path):
        resolved_path = self._resolve_path(file_path)
        
        if resolved_path in self.files:
            content = self.files[resolved_path]
            if isinstance(content, str) and content.startswith('base64:'):
                return len(content) - 7
            return len(content)
        return 0

    def list_directory(self):
        contents = []
        current = self.current_path.rstrip('/') or '/'
        
        for file_path in self.files:
            file_dir = os.path.dirname(file_path) or '/'
            if file_dir == current:
                contents.append({'name': os.path.basename(file_path), 'type': 'file'})
        
        for dir_path in self.dirs:
            if dir_path == '/':
                continue
            dir_parent = os.path.dirname(dir_path.rstrip('/')) or '/'
            if dir_parent == current:
                dir_name = os.path.basename(dir_path.rstrip('/'))
                contents.append({'name': dir_name, 'type': 'dir'})
        
        return sorted(contents, key=lambda x: (x['type'] != 'dir', x['name']))

    def change_directory(self, path):
        if not path or path == '~':
            self.current_path = '/'
            return True
            
        if path == '/':
            self.current_path = '/'
            return True
            
        if path.startswith('/'):
            target = path
        else:
            if self.current_path == '/':
                target = path
            else:
                target = self.current_path.rstrip('/') + '/' + path
        
        normalized = os.path.normpath(target).replace('\\', '/')
        
        if not normalized.endswith('/'):
            normalized += '/'
            
        if normalized in self.dirs:
            self.current_path = normalized
            return True
            
        return False

def run_script(script_path, vfs):
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
            contents = vfs.list_directory()
            if not contents:
                print("Директория пуста")
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

        elif command == "cat":
            if not args:
                print("cat: не указан файл")
                return False
            
            content = vfs.read_file(args[0])
            if content is not None:
                print(content)
            else:
                print(f"cat: {args[0]}: Нет такого файла")
                return False
            return True

        else:
            print(f"{command}: команда не найдена")
            return False

    except Exception as e:
        print(f"ОШИБКА при выполнении команды: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Эмулятор командной оболочки OS')
    parser.add_argument('--vfs', type=str, help='Путь к ZIP-архиву с VFS')
    parser.add_argument('--script', type=str, help='Путь к стартовому скрипту')
    
    args = parser.parse_args()
    
    print("Отладочный вывод параметров")
    print(f"VFS: '{args.vfs}'")
    print(f"Script: '{args.script}'")

    
    vfs = VFS(args.vfs)
    
    if args.script:
        success = run_script(args.script, vfs)
        if not success:
            sys.exit(1)
    else:
        username = getpass.getuser()
        hostname = socket.gethostname()
        
        print("Эмулятор командной оболочки (Этап 3). Введите 'exit' для выхода.")
        
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
