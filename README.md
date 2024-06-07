Статус "Принято" ставится, если:

Приложен скриншот с примером работы скрипта (в папке resource)
Приложен json-файл с результатом обработки access.log (в корне репозитория)
Задание выполнено и сдаётся в формате pull-request
Соблюдается минимальный код-стайл (для этого установлен форматер Блэк)
В pull-request не попали никакие лишние изменения, которые не связаны с заданием
Рекомендации:
Первое, что нужно сделать - это распаковать архив с файлом лога:

tar -xzvf access.tar.gz
Для того чтобы определить директорий или конкретный файл, был передан скрипту - можно использовать следующие методы:

os.path.isfile
os.path.isdir
Если скрипту был передан директорий - можно получить список всех файлов с помощью метода:

os.listdir
При этом стоит учесть, что os.listdir возвращает список имён файлов. Таким образом полные пути до файлов с логами нужно составить из пути до директория с файлами логов и полученных имён файлов.

Так как файл access.log достаточно большой (3216723 строк) - нужно собрать всю статистику за один проход по файлу.

Общее количество запросов в файле access.log можно сверить с выводом команды wc -l

wc -l access.log 
3216723 access.log
Количество запросов по HTTP-методам можно сверить с выводом команды grep -c. Например, чтобы определить количество GET-запросов в файле лога можно выполнить следующую команду:

grep -c '"GET ' access.log 
2247848
Топ 3 IP адресов с которых было сделано наибольшее количество запросов можно получить объединением в pipeline утилит, о которых мы говорили на лекции:

awk '{print $1}' access.log | sort | uniq -c | sort -r -s -n -k 1,1 | head -3
10 1.1.1.1
 9 2.2.2.2
 8 3.3.3.3
Здесь с помощью awk мы получаем список IP-адресов из файла лога. Далее с помощью sort сортируем этот список и с помощью uniq -с получаем количество вхождений каждого IP-адреса в отсортированный список. Затем с помощью sort мы сортируем полученную статистику по убыванию количества вхождений и c помощью head выводим первые 3 результата.

Топ 3 самых долгих запросов можно получить используя комбинацию описанного ранее подхода с утилитой grep. С помощью следующей команды мы получаем время исполнения самого долгого запроса:

awk '{print $NF}' access.log | sort | uniq | sort -r -s -n -k 1,1 | head -1
10000
Теперь мы можем найти 3 первых запроса с такой длительностью:

grep '10000$' access.log | head -3
1.1.1.1 - - [23/Dec/2015:07:27:57 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "-" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11" 10000
2.2.2.2 - - [06/Jan/2016:18:47:57 +0100] "GET /media/system/css/modal.css HTTP/1.1" 200 1159 "http://www.almhuette-raith.at/index.php?option=com_phocagallery&view=category&id=1&Itemid=53" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9" 10000
3.3.3.3 - - [06/Jan/2016:21:29:02 +0100] "GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_terasse.jpg HTTP/1.1" 200 5126 "http://www.almhuette-raith.at/index.php?option=com_phocagallery&view=category&id=1&Itemid=53" "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1" 10000
Команды приведённые выше нужно использовать исключительно для проверки работы вашего скрипта. В коде скрипта нельзя вызывать и использовать эти команды.