import re  # Импортируем модуль регулярных выражений для анализа строк
from collections import Counter  # Импортируем Counter для подсчета элементов
from datetime import datetime  # Импортируем datetime для работы с датой и временем
import os  # Импортируем модуль os для работы с файловой системой

# Функция для анализа лог-файла

def parse_log(log_file):
    requests_count = 0  # Инициализируем счетчик общего количества запросов
    http_methods = Counter()  # Создаем Counter для подсчета количества запросов по каждому HTTP-методу
    ip_addresses = Counter()  # Создаем Counter для подсчета количества запросов от каждого IP-адреса
    request_times = []  # Создаем пустой список для хранения информации о времени запроса

    # Определяем абсолютный путь к лог-файлу
    log_file_path = os.path.join(os.getcwd(), 'resources', log_file)

    # Открываем лог-файл для чтения
    with open(log_file_path, 'r') as f:
        # Читаем файл построчно
        for line in f:
            # Используем регулярное выражение для извлечения информации из строки лога
            parts = re.match(r'(\S+) - - \[(.*?)\] "(\S+).*?"', line)
            if parts:  # Если строка соответствует формату записи лога
                ip_address = parts.group(1)  # Извлекаем IP-адрес
                timestamp = datetime.strptime(parts.group(2), '%d/%b/%Y:%H:%M:%S %z')  # Извлекаем дату и время
                http_method = parts.group(3).split()[0]  # Извлекаем HTTP-метод

                requests_count += 1  # Увеличиваем счетчик общего количества запросов
                http_methods[http_method] += 1  # Увеличиваем счетчик для текущего HTTP-метода
                ip_addresses[ip_address] += 1  # Увеличиваем счетчик для текущего IP-адреса
                # Добавляем информацию о запросе в список request_times
                request_times.append((http_method, parts.group(3).split()[1], ip_address, timestamp))

    return requests_count, http_methods, ip_addresses, request_times  # Возвращаем результаты анализа

log_file = 'access1.log'  # Имя лог-файла
requests_count, http_methods, ip_addresses, request_times = parse_log(log_file)  # Анализируем лог-файл

# Выводим общее количество запросов
print("Общее количество выполненных запросов:", requests_count)
print("Количество запросов по HTTP-методам:")
# Выводим количество запросов по каждому HTTP-методу
for method, count in http_methods.items():
    print(f"{method}: {count}")
print("Топ 3 IP адресов:")
# Выводим топ 3 IP-адресов
for ip, count in ip_addresses.most_common(3):
    print(f"{ip}: {count}")

# Функция для нахождения топ 3 самых долгих запросов
def top_slowest_requests(request_times, n=3):
    # Сортируем список request_times по длительности запроса в обратном порядке и берем первые n элементов
    slowest_requests = sorted(request_times, key=lambda x: x[-1], reverse=True)[:n]
    return slowest_requests

slowest_requests = top_slowest_requests(request_times)  # Находим топ 3 самых долгих запросов
print("Топ 3 самых долгих запросов:")
# Выводим топ 3 самых долгих запросов
for req in slowest_requests:
    method, url, ip, timestamp = req
    print(f"HTTP метод: {method}, URL: {url}, IP: {ip}, Время запроса: {timestamp}")
