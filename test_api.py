import requests
import json
import os
from datetime import datetime

ANSWERS_DIR = 'answers'
os.makedirs(ANSWERS_DIR, exist_ok=True)


def save_response(test_number, test_name, response):
    filename = f"{ANSWERS_DIR}/test_{test_number:02d}_{test_name}.json"

    try:
        data = response.json()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f" Сохранено: {filename}")
    except:
        print(f" Не JSON ответ (Content-Type: {response.headers.get('Content-Type')})")


headers = {
    'AUTHORIZATION': 'Bearer cb1d3a52-d4a1-1234-8045-75ae7a493bd7'
}

print("=" * 50)
print("Тест 1: Получение METAR для URSS (Сочи)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'metar',
        'code': 'URSS'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Аэродром: {data['properties']['aerodrome']['name']}")
    print(f"METAR: {data['properties']['raw']}")
    save_response(1, 'metar', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 2: Получение TAF для UUDD (Домодедово)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'taf',
        'code': 'UUDD'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Аэродром: {data['properties']['aerodrome']['name']}")
    print(f"TAF: {data['properties']['raw']}")
    save_response(2, 'taf', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 3: Получение VFR для URSS, UUDD, UUEE")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'vfr',
        'code': 'URSS.UUDD.UUEE'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество аэродромов: {data['totalFeatures']}")
    for feature in data['features']:
        props = feature['properties']
        print(f"  {props['code']}: ICAO={props['icao']}, NOAA={props['noaa']}")
    save_response(3, 'vfr', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 4: Получение справочника ДМРЛ")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/cat/',
    params={'code': 'dmrl-list'},
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество радаров: {data['totalFeatures']}")
    save_response(4, 'dmrl_list', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 5: Получение SIGMET")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={'device': 'test-device-001', 'kind': 'sigmet', 'code': 'ULLL'},
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество сводок: {data['totalFeatures']}")
    save_response(5, 'sigmet', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 6: Получение AIRMET")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={'device': 'test-device-001', 'kind': 'airmet', 'code': 'ULLL'},
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество сводок: {data['totalFeatures']}")
    save_response(6, 'airmet', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 7: Получение GAMET")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'gamet',
        'area_name': 'TVER',
        'area_number': '5'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество сводок: {data['totalFeatures']}")
    save_response(7, 'gamet', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 8: Ветер/температура по маршруту (rwindtmp)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'rwindtmp',
        'p[0]': 'x37.5y55.6z150t1685450553',
        'p[1]': 'x38.5y56.6z200t1685454153'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество точек: {data['totalFeatures']}")
    for feature in data['features']:
        props = feature['properties']
        print(f"  FL{props['pointFl']}: T={props['tmp']}°C, Wind={props['wind']} м/с")
    save_response(8, 'rwindtmp', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 9: Предупреждения по аэродрому (adwrng)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'adwrng',
        'code': 'URSS.UUDD'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество предупреждений: {data['totalFeatures']}")
    for feature in data['features']:
        props = feature['properties']
        print(f"  {props['icao']}: {props['msg']}")
    save_response(9, 'adwrng', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 10: Предупреждения о сдвиге ветра (wswrng)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'wswrng',
        'code': 'URSS'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество предупреждений: {data['totalFeatures']}")
    for feature in data['features']:
        props = feature['properties']
        print(f"  {props['icao']}: {props['msg']}")
    save_response(10, 'wswrng', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 11: Данные ДМРЛ - метеоявления (wdmrl)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'wdmrl',
        'code': 'rudn'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество полигонов: {data['totalFeatures']}")
    print(f"Радар: {data['radar']}")
    save_response(11, 'wdmrl', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 12: Данные ДМРЛ - осадки (pdmrl)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'pdmrl',
        'code': 'rudn'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество полигонов: {data['totalFeatures']}")
    save_response(12, 'pdmrl', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 13: Сообщения с бортов (AIREP)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'airep',
        'code': 'ULLL'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество сообщений: {data['totalFeatures']}")
    if data['features']:
        print(f"AIREP: {data['features'][0]['properties']['raw']}")
    save_response(13, 'airep', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 14: Радиозонды (zond)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'zond',
        'code': 'ULLL'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество зондов: {data['totalFeatures']}")
    if data['features']:
        props = data['features'][0]['properties']
        print(f"Точек в траектории: {len(props['path'])}")
    save_response(14, 'zond', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 15: Вулканический пепел (VAAC)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'vaac',
        'code': 'RJTD'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество сообщений: {data['totalFeatures']}")
    save_response(15, 'vaac', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 16: Тропический циклон (TCAC)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'tcac',
        'code': 'KNHC'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество сообщений: {data['totalFeatures']}")
    save_response(16, 'tcac', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 17: Космическая погода (SWX)")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'swx'
    },
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Количество сообщений: {data['totalFeatures']}")
    save_response(17, 'swx', response)
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 18: Полетная документация (brief)")
print("=" * 50)

fpl = """(FPL-PPP1441-IS
-A319/M-SDFGHIRWY/B1L
-ULMM1735
-K0768F320 ASGO1K ASGOR T693 PILAN/K0779F330 M856 KUKUM/K0788F340
M856 GIKUR/K0801F350 T458 BEPOL BEPO1A
-ULLI0142 UUEE
-PBN/B1D1A1S2O1 DOF/230220 REG/PP00000 EET/ULLL0005 SEL/SSSS
CODE/000000 OPR/PPP RALT/ULMM ULLI RMK/ACASII EQUIPPED)"""

response = requests.post(
    'http://localhost:5000/meteo/',
    params={
        'device': 'test-device-001',
        'kind': 'brief'
    },
    data=fpl,
    headers=headers
)

print(f"Статус: {response.status_code}")
if response.status_code == 200:
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    with open('briefing.pdf', 'wb') as f:
        f.write(response.content)
    print(f"PDF сохранен как 'briefing.pdf' ({len(response.content)} байт)")
    pdf_info = {
        'test': 18,
        'name': 'brief',
        'status_code': response.status_code,
        'content_type': response.headers.get('Content-Type'),
        'content_disposition': response.headers.get('Content-Disposition'),
        'file_size_bytes': len(response.content)
    }
    with open(f"{ANSWERS_DIR}/test_18_brief_info.json", 'w', encoding='utf-8') as f:
        json.dump(pdf_info, f, ensure_ascii=False, indent=2)
    print(f"Информация о PDF сохранена: {ANSWERS_DIR}/test_18_brief_info.json")
else:
    print(f"Ошибка: {response.text}")

print("\n" + "=" * 50)
print("Тест 19: Проверка ошибок")
print("=" * 50)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={'device': 'test-device-001', 'kind': 'metar', 'code': 'XXXX'},
    headers=headers
)
print(f"Несуществующий аэродром: {response.status_code}")
save_response(19, 'error_aerodrome_not_found', response)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={'device': 'test-device-001', 'kind': 'metar', 'code': 'URSS'}
)
print(f"Без авторизации: {response.status_code}")
save_response(20, 'error_unauthorized', response)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={'device': 'test-device-001', 'kind': 'wdmrl', 'code': 'xxxx'},
    headers=headers
)
print(f"Несуществующий радар: {response.status_code}")
save_response(21, 'error_radar_not_found', response)

response = requests.get(
    'http://localhost:5000/meteo/',
    params={'device': 'test-device-001', 'kind': 'rwindtmp'},
    headers=headers
)
print(f"Нет точек для rwindtmp: {response.status_code}")
save_response(22, 'error_no_points', response)

print("\n" + "=" * 50)
print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
print(f"JSON ответы сохранены в папке: {ANSWERS_DIR}/")
print("=" * 50)