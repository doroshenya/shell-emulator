import os
import sys
import getpass
import socket
import argparse #обработка аргументов командной строки

def run_script(script_path):
    #Выполняет стартовый скрипт (ЭТАП 2)
    print(f"Выполнение скрипта: {script_path}")
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f: #правильная кодировка для русских символов
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1): 
        #enumerate(lines, 1) - получает и номер строки (начиная с 1), и содержимое
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Показываем команду как в реальной консоли
            username = getpass.getuser()
            hostname = socket.gethostname()
            current_dir = os.getcwd()
            prompt = f"{username}@{hostname}:{current_dir}$ "
            print(prompt + line)
            
            # Выполняем команду
            success = execute_command(line)
            
            if not success: #остановка при первой ошибке
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

def execute_command(cmd):
    #Выполняет одну команду эмулятора

    parts = cmd.split()
    if not parts:
        return True
    
    command = parts[0]
    args = parts[1:]

    try:
        # КОМАНДА EXIT - выход из эмулятора
        if command == "exit":
            print("Выход из эмулятора")
            sys.exit(0)

        # КОМАНДА LS - заглушка
        elif command == "ls":
            print(f"ls: аргументы {args}" if args else "ls: команда ls")
            return True

        # КОМАНДА CD - заглушка  
        elif command == "cd":
            if args:
                print(f"cd: переход в '{args[0]}'")
            else:
                print("cd: переход в домашнюю директорию")
            return True

        # НЕИЗВЕСТНАЯ КОМАНДА
        else:
            print(f"{command}: команда не найдена")
            return False

    except Exception as e:
        print(f"ОШИБКА при выполнении команды: {e}")
        return False

def main():
    #Основная функция программы

    # Парсер аргументов командной строки (ЭТАП 2)
    parser = argparse.ArgumentParser(description='Эмулятор командной оболочки OS') #создание парсера
    parser.add_argument('--vfs', type=str, help='Путь к физическому расположению VFS') #путь к виртуальной файловой системе (пока не используется)
    parser.add_argument('--script', type=str, help='Путь к стартовому скрипту') #путь к скрипту для выполнения
    
    args = parser.parse_args() # разбирает аргументы командной строки
    
    # Отладочный вывод параметров
    print("Отладочный вывод параметров")
    print(f"VFS: '{args.vfs}'")
    print(f"Script: '{args.script}'")
    
    # Если указан скрипт - выполняем его (ЭТАП 2)
    if args.script:
        success = run_script(args.script)
        if not success:
            sys.exit(1)
    else:
        # Иначе интерактивный режим (ЭТАП 1)
        username = getpass.getuser()
        hostname = socket.gethostname()
        
        print("Эмулятор командной оболочки (Этап 2). Введите 'exit' для выхода.")
        
        while True:
            current_dir = os.getcwd()
            prompt = f"{username}@{hostname}:{current_dir}$ "
            
            try:
                user_input = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nВыход из эмулятора")
                break
                
            if not user_input:
                continue
                
            execute_command(user_input)

if __name__ == "__main__":
    main()
