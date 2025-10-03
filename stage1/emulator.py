import os #текущая директория, пути
import sys #выход из программы
import getpass #получение информации о пользователе
import socket #имя компьютера

def execute_command(cmd):
    #Выполняет одну команду эмулятора
    parts = cmd.split() 
    if not parts:
        return True
    
    command = parts[0] #имя команды
    args = parts[1:] #аргументы

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

    except Exception as e: #любые ошибки при исполнении команды
        print(f"ОШИБКА при выполнении команды: {e}")
        return False

def main():
    #Основная функция программы - REPL цикл
    username = getpass.getuser()#получение имени текущего пользователя ОС
    hostname = socket.gethostname()#получение имени компьютера
    
    print("Эмулятор командной оболочки (Этап 1). Введите 'exit' для выхода.")#приветственное сообщение
    
    # REPL цикл (Read-Eval-Print Loop)
    while True:
        current_dir = os.getcwd()#получение текущей рабочей директории
        prompt = f"{username}@{hostname}:{current_dir}$ "#формирование приглашения
        
        try:
            user_input = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из эмулятора")
            break
            
        if not user_input:
            continue
            
        execute_command(user_input)

if __name__ == "__main__": #запуск, если файл выполняется напрямую (не импортируется как модуль)
    main()
