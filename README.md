# shell-emulator
Дорохова А.С. ИКБО-30-24. Вариант 5. 
Проект: эмулятор командной оболочки (как командная строка), который работает с виртуальной файловой системой. Выполнен в 5 этапов, каждый этап добавляет новую функциональность.

Этап 1 - Базовые команды
exit - выход из программы
ls - список файлов
cd - переход между папками

Этап 2 - Скрипты
Запуск программы со скриптами
Автоматическое выполнение команд из файла

Этап 3 - Виртуальная файловая система (VFS)
Работа с файлами из ZIP-архива
Команды `pwd` и `cat` для работы с файлами

Этап 4 - Новые команды
tac - показывает файл задом наперед
du - показывает размеры файлов и папок

Этап 5 - Права доступа
chown - меняет владельца файлов
ls -l - показывает подробную информацию о файлах

В каждой папке (кроме первой )есть:
emulator.py - основная программа
run_interactive.bat - для запуска в Windows
run_test.bat - для тестирования
test_script.txt - тестовые команды


Этап 1. REPL
Цель: создать минимальный прототип. Большинство функций в нем пока представляют собой заглушки, но диалог с пользователем уже поддерживается.
Требования:
1.Приложение должно быть реализовано в форме консольного интерфейса (CLI).
Код:

<img width="823" height="355" alt="Снимок экрана 2025-10-09 092340" src="https://github.com/user-attachments/assets/eb59df00-58d2-42e2-8ca8-dcd08758c75d" />
Вывод:


<img width="775" height="52" alt="Снимок экрана 2025-10-09 092603" src="https://github.com/user-attachments/assets/433ff0b4-4eb9-49fb-a0f0-d70cb1295cf6" />

2.Приглашение к вводу должно формироваться на основе реальных данных ОС, в которой исполняется эмулятор. Пример: username@hostname:~$.
Код:

<img width="568" height="34" alt="Снимок экрана 2025-10-09 092406" src="https://github.com/user-attachments/assets/d48edefa-df65-430d-a9cb-a753d7c35a30" />

<img width="609" height="38" alt="Снимок экрана 2025-10-09 092412" src="https://github.com/user-attachments/assets/87c13d6a-e6d9-44eb-81a2-03d0202b764b" />

Вывод:

<img width="758" height="42" alt="Снимок экрана 2025-10-09 092621" src="https://github.com/user-attachments/assets/fa5fa28c-6b22-4983-adfe-a9572812dc31" />

3.Реализовать простой парсер, который разделяет ввод на команду и аргументы по пробелам.
Код:

<img width="328" height="140" alt="Снимок экрана 2025-10-09 092437" src="https://github.com/user-attachments/assets/81895011-d47f-4da5-a990-07ddbaaf8cee" />

Вывод:

<img width="836" height="41" alt="Снимок экрана 2025-10-09 092640" src="https://github.com/user-attachments/assets/770d2a53-db0a-40a9-87cd-277a8184d57a" />

4.Реализовать команды-заглушки, которые выводят свое имя и аргументы: ls, cd.
Код:

<img width="532" height="204" alt="Снимок экрана 2025-10-09 092450" src="https://github.com/user-attachments/assets/368b287e-c5d3-4042-9d76-2f7859482306" />

Вывод:

<img width="853" height="80" alt="Снимок экрана 2025-10-09 092702" src="https://github.com/user-attachments/assets/2924f8d6-2bbb-4158-893b-c8b85c729869" />

5.Реализовать команду exit.
Код:

<img width="310" height="70" alt="Снимок экрана 2025-10-09 092458" src="https://github.com/user-attachments/assets/1e3c7f98-4a12-4fae-ab8d-99b907e65f44" />

Вывод:

<img width="814" height="52" alt="Снимок экрана 2025-10-09 092721" src="https://github.com/user-attachments/assets/065b1193-489a-47d7-a2a0-883691a3ca7d" />

6.Продемонстрировать работу прототипа в интерактивном режиме. Необходимо показать примеры работы всей реализованной функциональности, включая обработку ошибок.
Код:

<img width="512" height="148" alt="image" src="https://github.com/user-attachments/assets/0c069ac3-4bb8-4579-b848-291f877cbdd5" />

Вывод:

<img width="818" height="87" alt="Снимок экрана 2025-10-09 092758" src="https://github.com/user-attachments/assets/adec2255-5533-4427-b442-c7fb22b050f7" />

Этап 2. Конфигурация
Цель: сделать эмулятор настраиваемым, то есть поддержать ввод параметров пользователя в приложение. Организовать для этого этапа отладочный вывод всех заданных параметров при запуске эмулятора.
Требования:
1.Параметры командной строки:
–Путь к физическому расположению VFS.
–Путь к стартовому скрипту.
Код:

<img width="896" height="232" alt="Снимок экрана 2025-10-09 092903" src="https://github.com/user-attachments/assets/32d1be71-e426-47f8-b5c6-46329bc42b5a" />

Вывод:

<img width="414" height="84" alt="Снимок экрана 2025-10-09 093152" src="https://github.com/user-attachments/assets/1c40c23b-dd3f-4484-977c-8b5a7dc6b55b" />

2.Стартовый скрипт для выполнения команд эмулятора: останавливается при первой ошибке. При выполнении скрипта на экране отображается как ввод, так и вывод, имитируя диалог с пользователем.
Код:

<img width="840" height="447" alt="image" src="https://github.com/user-attachments/assets/4d85f93a-22f6-4786-8592-d89a7e727097" />

Вывод:

<img width="852" height="191" alt="Снимок экрана 2025-10-09 093205" src="https://github.com/user-attachments/assets/5f1f5f61-8984-474a-a168-6d58ab56f7ba" />

3.Сообщить об ошибке во время исполнения стартового скрипта.
Код:

<img width="474" height="114" alt="image" src="https://github.com/user-attachments/assets/9d30b3ce-1889-4917-9c13-e8657f63e4f0" />

Вывод:

<img width="459" height="130" alt="Снимок экрана 2025-10-09 093701" src="https://github.com/user-attachments/assets/19d29f5f-5786-41d7-ad0a-9cf654971884" />

Для проверки работы кода на несуществующем скрипте, создадим несуществующий скрипт test_missing_script.bat

<img width="428" height="144" alt="Снимок экрана 2025-10-09 093829" src="https://github.com/user-attachments/assets/9d22f700-8ef8-452b-9707-4c00bca4e2e4" />

Вывод:

<img width="459" height="130" alt="Снимок экрана 2025-10-09 093701" src="https://github.com/user-attachments/assets/22b9e3e4-55a8-4e8e-ac87-6d7995a57e23" />

4.Создать несколько скриптов реальной ОС, в которой выполняется эмулятор. Включить в каждый скрипт вызовы эмулятора для тестирования всех поддерживаемых параметров командной строки.
run_test.bat

<img width="409" height="135" alt="Снимок экрана 2025-10-09 093048" src="https://github.com/user-attachments/assets/388aa866-ada6-4db7-8484-f3e1787a1dd3" />

run_interactive.bat

<img width="452" height="145" alt="Снимок экрана 2025-10-09 093108" src="https://github.com/user-attachments/assets/7845113c-cd33-48f5-b1c0-e60e1c3d837e" />

Этап 3. VFS
Цель: подключить виртуальную файловую систему (VFS).
Требования:
1.Все операции должны производиться в памяти. Запрещается распаковывать или иным образом модифицировать данные VFS, за исключением возможных служебных команд.
Код:

<img width="521" height="496" alt="Снимок экрана 2025-10-09 094121" src="https://github.com/user-attachments/assets/c1538f25-147c-4d25-a1df-3622fcdd8fa5" />

Вывод:

<img width="344" height="45" alt="Снимок экрана 2025-10-09 094539" src="https://github.com/user-attachments/assets/d378c31d-59ab-4a6a-a67a-0ad9bb34fd7b" />

2.Источником VFS является ZIP-архив. Для двоичных данных используется base64 или аналогичный формат.
Код:

<img width="561" height="234" alt="Снимок экрана 2025-10-09 094143" src="https://github.com/user-attachments/assets/7eccb0bf-40dd-4d4a-a860-84b82ac9d225" />

3.Создать несколько скриптов реальной ОС, в которой выполняется эмулятор. Включить в каждый скрипт вызовы эмулятора для тестирования работы c различными вариантами VFS (минимальный, несколько файлов, не менее 3 уровней файлов и папок).
Код:
create_test_vfs.py

<img width="539" height="186" alt="Снимок экрана 2025-10-09 094220" src="https://github.com/user-attachments/assets/c46b2c31-f366-44f5-acb9-3b68086daea3" />

4.Создать стартовый скрипт для тестирования всех реализованных на этом и прошлых этапах команд. Добавить туда примеры всех режимов команд, включая работу с VFS и обработку ошибок.
test_script.txt

<img width="168" height="197" alt="Снимок экрана 2025-10-09 094301" src="https://github.com/user-attachments/assets/dd20deb2-29c5-417e-93d0-f0e51d40ca6f" />

Вывод:

<img width="485" height="399" alt="Снимок экрана 2025-10-09 094457" src="https://github.com/user-attachments/assets/188a69ec-b9be-4fd5-a0bd-a3c6fbdd4fd7" />

Этап 4. Основные команды
Цель: поддержать команды, имитирующие работу в UNIX-подобной командной строке.
Требования:
1.Необходимо реализовать логику для ls и cd.
Код:
ls:

<img width="363" height="189" alt="Снимок экрана 2025-10-09 094637" src="https://github.com/user-attachments/assets/cd980c7b-132f-4358-8b5b-5f91fd535d47" />

cd:

<img width="441" height="128" alt="Снимок экрана 2025-10-09 094642" src="https://github.com/user-attachments/assets/86b078ac-e123-40a0-a59b-8f3448c7c518" />

2.Реализовать новые команды: tac, du.
Код:
tac:

<img width="473" height="297" alt="Снимок экрана 2025-10-09 094707" src="https://github.com/user-attachments/assets/7af805a7-b9f2-40a7-b472-a17e645f461e" />

du:

<img width="682" height="374" alt="Снимок экрана 2025-10-09 094724" src="https://github.com/user-attachments/assets/0bb39046-1887-48f3-9e01-9d56799d2524" />

3.Создать стартовый скрипт для тестирования всех реализованных на этом этапе команд. Добавить туда примеры всех режимов команд, включая работу с VFS и обработку ошибок.
test_script.txt

<img width="435" height="254" alt="Снимок экрана 2025-10-09 094743" src="https://github.com/user-attachments/assets/4e660d97-080d-47d0-b3d1-0253ea12d264" />

Вывод:

<img width="457" height="929" alt="Снимок экрана 2025-10-09 095519" src="https://github.com/user-attachments/assets/7e107613-dc8d-463d-bdc9-c485e06a0881" />

Этап 5. Дополнительные команды
Цель: поддержать более сложные команды, изменяющие состояние VFS, при этом модификации должны осуществляться только в памяти.
Требования:
1.Реализовать команды: chown.
Код:

<img width="647" height="422" alt="Снимок экрана 2025-10-09 095612" src="https://github.com/user-attachments/assets/8fb006ec-ba4b-47b4-b7e5-97be6958f3ca" />

Вывод:

<img width="627" height="619" alt="Снимок экрана 2025-10-09 095941" src="https://github.com/user-attachments/assets/1418fde5-88e1-44c9-a6ff-10ace2eecc0d" />

<img width="563" height="238" alt="Снимок экрана 2025-10-09 100117" src="https://github.com/user-attachments/assets/289117e5-f989-4be9-8f1d-9f528b084bc8" />

<img width="519" height="380" alt="Снимок экрана 2025-10-09 100105" src="https://github.com/user-attachments/assets/cd4240c8-246f-492a-9137-09c23f2ab48f" />

3. Команда ls -l с подробной информацией

<img width="851" height="329" alt="Снимок экрана 2025-10-09 100148" src="https://github.com/user-attachments/assets/85f47ebf-e90e-44db-9b3e-62b362b6e07f" />

Вывод:

<img width="601" height="748" alt="Снимок экрана 2025-10-09 100210" src="https://github.com/user-attachments/assets/bffabe74-49b4-40b8-9f7c-017e81ed924b" />

2.Создать стартовый скрипт для тестирования всех реализованных на этом этапе команд. Добавить туда примеры всех режимов команд, включая работу с VFS и обработку ошибок.
test_script.txt

<img width="449" height="196" alt="Снимок экрана 2025-10-09 100236" src="https://github.com/user-attachments/assets/3e294b60-fbba-4247-a33e-24c3c13838a6" />

Полный вывод:

<img width="610" height="969" alt="Снимок экрана 2025-10-09 100305" src="https://github.com/user-attachments/assets/033345ba-7ea8-4e1a-8796-8b84d5d44f9d" />

run_test.bat

<img width="515" height="218" alt="Снимок экрана 2025-10-09 100336" src="https://github.com/user-attachments/assets/2edc1614-2907-49bf-873d-9cbcd7f62d3e" />

run_interactive.bat

<img width="461" height="146" alt="Снимок экрана 2025-10-09 100427" src="https://github.com/user-attachments/assets/3c132994-837f-4c84-b462-7f7fe1bb5177" />




run_interactive.bat
<img width="461" height="146" alt="Снимок экрана 2025-10-09 100427" src="https://github.com/user-attachments/assets/7f708c70-7ee1-4f23-be61-26236c7ef590" />
