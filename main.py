from prettytable import PrettyTable
import datetime
import json
import easygui

def get_results(results):
    results_line = '' # Строка, собирающая из символов изначальные строки и отдающая их массиву
    results_line_arr = [] # Массив строк с результатами
    results_arr = [] # Массив номеров и времени забега

    for i in results: # Заполнение массива results_line_arr
        if i == '\n':
            results_line_arr.append(results_line)
            results_line = ''
        else:
            results_line += i.replace(',', '.')
    results_line_arr.append(results_line)

    index = 0 # Индекс, используемый для получения текущей строки и вычисление разницы между временем начала забега и конца
    while index < len(results_line_arr) - 2 / 2: # Заполнение массива results_arr
        start_arr = results_line_arr[index][len(results_line_arr[index]) - 15:].split(':')
        finish_arr = results_line_arr[index + 1][len(results_line_arr[index + 1]) - 15:].split(':')
        finish = datetime.timedelta(hours=int(finish_arr[0]), minutes=int(finish_arr[1]), seconds=float(finish_arr[2]))
        start = datetime.timedelta(hours=int(start_arr[0]), minutes=int(start_arr[1]), seconds=float(start_arr[2]))
        time = str(finish - start)
        try:
            number = int(results_line_arr[index][:3])
        except:
            number = int(results_line_arr[index][:1])
        results_arr.append([str(number).replace(' ', ''), time[:-3]])
        index += 2
    return results_arr # возвращение массива

def get_competitors_info(competitors, results_arr, competitors_arr):
    # Цикл сопоставления и добавления данных в массив competitors_arr
    for j in competitors:
        participated = False
        for k in results_arr:
            if str(j) == str(k[0]):
                competitors_arr.append([str(j), str(competitors[j]['Name']), str(competitors[j]['Surname']), k[1]])
                participated = True
        if not participated:
            competitors_arr.append([j, competitors[j]['Name'], competitors[j]['Surname'], 'Дисквалификация'])

    competitors_arr.sort(key=custom_key) # Сортировка массива по времени
    return competitors_arr # возвращение массива

def custom_key(competitors_arr):
    return competitors_arr[3]

def draw_table(competitors_arr):
    table = PrettyTable() # Таблица
    table.field_names = ['Место', 'Номер', 'Фамилия', 'Имя', 'Результат'] # "Шапка" таблицы

    place = 0 # Счетчик места участника
    for i in competitors_arr: # Заполнение таблицы
        place += 1
        table.add_row([place, i[0], i[1], i[2], i[3]])

    print(table)

def main():
    competitors_arr = [] # Массив, который будет хранить значения нагрудного номера, имени, фамилии и времени забега

    try: # открытие и чтение файла с результатами
        with open('results_RUN.txt', 'r', encoding='utf-8-sig') as results_file:
            results = results_file.read().rstrip()
    except Exception as ex:
        res = easygui.fileopenbox('Откройте файл с результатами')
        with open(res, 'r', encoding='utf-8-sig') as results_file:
            results = results_file.read().rstrip()


    results_arr = get_results(results) # Получение массива номеров и времени забега

    try: # Открытие, чтение и загрузка json файла с номерами, фамилиями и именами участников
        competitors_file = open('files\competitors2.json', 'r', encoding='utf8')
        competitors_data = competitors_file.read()
        competitors = json.loads(competitors_data)
    except:
        comp = easygui.fileopenbox('Откройте файл с участниками')
        competitors_file = open(comp, 'r', encoding='utf8')
        competitors_data = competitors_file.read()
        competitors = json.loads(competitors_data)

    # Получение массива данных об участниках и их результатах
    competitors_arr = get_competitors_info(competitors, results_arr, competitors_arr)

    draw_table(competitors_arr) # "Отрисовка" таблицы

if __name__ == '__main__': #Запуск программы
    main()