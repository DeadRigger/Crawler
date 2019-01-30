from bs4 import BeautifulSoup
import requests
import csv


def print_dict(dictionary):
    print('{')
    for key in dictionary.keys():
        print('\t' + key + ': ' + dictionary[key])
    print('}')


def save_csv(cars, path):  # ФУНКЦИЯ ЗАПИСИ СПАРСЕННЫХ ФАЙЛОВ В CSV ФАЙЛ
    with open(path, 'w', newline='') as csvfile:
        fieldnames = []
        for key in cars[0].keys():
            fieldnames.append(key)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(cars)


def read_csv(path, fieldnames):
    with open(path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        cars = []
        for row in reader:
            car = {field: row[field] for field in fieldnames}
            cars.append(car)

    return cars


def parser_cars():
    global url
    global get
    global cars

    r = requests.get(url + get)
    soup = BeautifulSoup(r.text, 'html.parser')

    for tr in soup.find_all('tr', class_='search_result_model'):
        col = tr.find_all('td')

        url_car = col[1].a['href']
        r = requests.get(url_car)
        soup = BeautifulSoup(r.text, 'html.parser')

        name_car = soup.find(id='container_h1').h1.text.strip('\n\t')
        print(name_car + ": " + url_car)
        for mod_block in soup.find_all('tbody', class_='modifications_block'):
            m = True
            for row in mod_block.find_all('tr'):
                if m:
                    mod = row.th.text
                    print(mod + ':')
                    td = row.find_all('td')
                    fuel = td[0].text
                    drive = td[1].text
                    power = td[2].text.strip(' л.с.')
                    accel = td[3].text.strip(' с')
                    fuel_rate = td[4].text.strip(' л/100\xa0км')
                    m = not m
                else:
                    compare = row.find('td', class_='add_remove_compare')
                    if compare is not None:
                        add_mod = compare.a.text
                        url_mod = compare.a['href']

                    price = row.find('td', class_='price').text.strip('\n\t Руб.\n').replace(' ', '')

                    tco = requests.get(url_mod + 'tco')
                    soup = BeautifulSoup(tco.text, 'html.parser')

                    cost_with_kasko = \
                        soup.find('span', class_='with_kasko_with_maintenance').b.text.replace(' ', '').strip('Руб.')
                    cost_without_kasko = \
                        soup.find('span', class_='without_kasko_with_maintenance').b.text.replace(' ', '').strip('Руб.')

                    car = {
                        'name': name_car + ' ' + mod + ' ' + add_mod,
                        'url': url_mod,
                        'url_tco': url_mod + 'tco',
                        'fuel': fuel,
                        'drive': drive,
                        'power': power,
                        'acceleration': accel,
                        'fuel_rate': fuel_rate,
                        'price': price,
                        'cost_with_kasko': cost_with_kasko,
                        'cost_without_kasko': cost_without_kasko
                    }
                    print_dict(car)
                    cars.append(car)
            print()

    nav = soup.find(class_='pages_navigation')
    if nav is not None:
        next = nav.find('a', class_='right')
        if next is not None:
            get = next['href']
            print('...')
            print('Переход на новую страницу' + url + get)
            print('...')
            print('Парсинг данных...')
        else:
            return False

    else:
        return False

    return True


price_min = 1000000
price_max = 2000000
url = 'https://quto.ru/catalog/search/result/'

get = '?price_min=' + str(price_min) + '&price_max=' + str(price_max)
filename = 'price' + str(price_min) + '-' + str(price_max) + '.csv'

cars = []
parse = True

while parse:
    print('Переход на страницу ценовой категории ' + str(price_min) + '-' + str(price_max) + ' рублей: ' + url + get)
    print('...')
    print('Парсинг данных...')
    parse = parser_cars()

save_csv(cars, filename)

# fields = ['name', 'url', 'url_tco', 'fuel',
#           'drive', 'power', 'acceleration', 'fuel_rate',
#           'price', 'cost_with_kasko', 'cost_without_kasko']
#
# cars = read_csv(filename, fields)

# Car with minimal price on 5 years with kasko
car_with_kasko = None
# Car with minimal price on 5 years without kasko
car_without_kasko = None

for car in cars:
    if car_with_kasko is not None and car_without_kasko is not None:
        min_price_kasko = int(car_with_kasko['price']) + int(car_with_kasko['cost_with_kasko'])
        curr_price_kasko = int(car['price']) + int(car['cost_with_kasko'])
        if min_price_kasko > curr_price_kasko:
            car_with_kasko = car

        min_price = int(car_without_kasko['price']) + int(car_without_kasko['cost_without_kasko'])
        curr_price = int(car['price']) + int(car['cost_without_kasko'])
        if min_price > curr_price:
            car_without_kasko = car
    else:
        car_with_kasko = car
        car_without_kasko = car


print_dict(car_with_kasko)
print_dict(car_without_kasko)
print()
print(min_price_kasko)
print(min_price)