# Weather Server — Эмулятор Метеорологического Сервера

## 📋 Оглавление
1. [О проекте](#о-проекте)
2. [Технологический стек](#технологический-стек)
3. [Установка и запуск](#установка-и-запуск)
4. [Структура проекта](#структура-проекта)
5. [API Endpoints](#api-endpoints)
6. [Метеорологические данные](#метеорологические-данные)
7. [Справочники](#справочники)
8. [Авторизация и регистрация](#авторизация-и-регистрация)
9. [База данных](#база-данных)
10. [Тестирование](#тестирование)
11. [Сокращения и термины](#сокращения-и-термины)
12. [Примеры запросов](#примеры-запросов)
13. [Docker](#docker)

---

## О проекте

**Weather Server** — это эмулятор метеорологического сервера «МетеоИнтерфейс», который имитирует работу реального API для предоставления метеорологической информации пользователям воздушного пространства (пилотам, авиакомпаниям, диспетчерам).

Сервер генерирует реалистичные метеорологические данные для аэродромов России и возвращает их в формате JSON (или PDF для полетной документации).

### Основные возможности
- ✅ Генерация 17 видов метеорологических данных
- ✅ 26 реальных аэродромов России
- ✅ 26 метеорологических радаров
- ✅ Авторизация через Bearer токен
- ✅ Rate limiting (ограничение запросов)
- ✅ Генерация PDF полетной документации
- ✅ Климатические зоны (реалистичные температуры)
- ✅ Полная обработка ошибок

---

## Технологический стек

| Технология | Версия | Назначение |
|------------|--------|------------|
| Python | 3.13+ | Основной язык |
| Flask | 3.0.3 | Web-фреймворк |
| Flask-SQLAlchemy | 3.1.1 | ORM для БД |
| PostgreSQL | 15+ | База данных |
| psycopg | 3.2+ | Драйвер PostgreSQL |
| reportlab | 5.0.1 | Генерация PDF |
| pytest | 7.3.1 | Тестирование |
| python-dotenv | 1.0.0 | Переменные окружения |

---

## Установка и запуск

### Предварительные требования
- Python 3.13+
- PostgreSQL 15+
- Git (опционально)

### Шаг 1: Клонирование репозитория
```bash
git clone <repository-url>
cd Weather_Server
```

### Шаг 2: Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Шаг 3: Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка базы данных PostgreSQL
```sql
CREATE DATABASE weather_server;
CREATE USER meteo WITH PASSWORD 'meteo_password';
GRANT ALL PRIVILEGES ON DATABASE weather_server TO meteo;
```

### Шаг 5: Создание файла .env
Создайте файл `.env` в корне проекта:
```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=weather_server
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/weather_server

# Auth
ADMIN_KEY=eb1d7a52-d4a1-2312-9045-68ae7a493bd7
USER_TOKEN=cb1d3a52-d4a1-1234-8045-75ae7a493bd7

# Server
SECRET_KEY=dev-secret-key
FLASK_APP=app.main
FLASK_ENV=development
```

### Шаг 6: Запуск сервера
```bash
python -m app.main
```

Сервер запустится на `http://localhost:5000`

### Запуск через Docker
```bash
docker-compose up --build
```

---

## Структура проекта

```
Weather_Server/
├── app/                          # Основное приложение
│   ├── __init__.py              # Инициализация приложения, загрузка данных
│   ├── main.py                  # Точка входа
│   ├── config.py                # Конфигурация из .env
│   ├── database.py              # Инициализация SQLAlchemy
│   ├── models.py                # Модели БД (Aerodrome, Radar)
│   │
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   ├── routes.py            # Регистрация blueprint'ов
│   │   ├── meteo.py             # Основные метео-запросы
│   │   ├── catalog.py           # Справочники
│   │   └── registration.py      # Регистрация ключей
│   │
│   ├── core/                    # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── auth.py              # Авторизация
│   │   ├── rate_limiter.py      # Ограничение запросов
│   │   └── errors.py            # Обработка ошибок
│   │
│   ├── generators/              # Генераторы метеоданных
│   │   ├── __init__.py
│   │   ├── metar_gen.py         # Генератор METAR
│   │   ├── taf_gen.py           # Генератор TAF
│   │   ├── sigmet_gen.py        # Генератор SIGMET
│   │   ├── airmet_gen.py        # Генератор AIRMET
│   │   ├── gamet_gen.py         # Генератор GAMET
│   │   ├── rwindtmp_gen.py      # Ветер/температура по маршруту
│   │   ├── adwrng_gen.py        # Предупреждения по аэродрому
│   │   ├── wswrng_gen.py        # Предупреждения о сдвиге ветра
│   │   ├── dmrl_gen.py          # Данные радаров
│   │   ├── airep_gen.py         # Сообщения с бортов
│   │   ├── zond_gen.py          # Радиозонды
│   │   ├── vaac_gen.py          # Вулканический пепел
│   │   ├── tcac_gen.py          # Тропические циклоны
│   │   ├── swx_gen.py           # Космическая погода
│   │   ├── fpl_parser.py        # Парсер плана полета
│   │   ├── brief_gen.py         # Генератор PDF документации
│   │   └── climate_zones.py     # Климатические зоны
│   │
│   ├── data/                    # Данные
│   │   ├── aerodromes.json      # 26 аэродромов
│   │   └── radars.json          # 26 радаров
│   │
│   └── utils/                   # Утилиты
│       ├── __init__.py
│       └── time_utils.py        # Работа со временем
│
├── tests/                       # Тесты
│   ├── __init__.py
│   ├── test_auth.py             # Тесты авторизации (3 теста)
│   ├── test_meteo.py            # Тесты METAR/TAF/VFR (6 тестов)
│   ├── test_rate_limit.py       # Тесты rate limiting (3 теста)
│   ├── test_sigmet_airmet_gamet.py  # Тесты SIGMET/AIRMET/GAMET (16 тестов)
│   ├── test_new_features.py     # Тесты новых функций (17 тестов)
│   ├── test_special_data.py     # Тесты спецданных (11 тестов)
│   └── test_brief.py            # Тесты PDF (4 теста)
│
├── .env.example                 # Пример конфигурации
├── .gitignore                   # Игнорируемые файлы
├── Dockerfile                   # Docker образ
├── docker-compose.yml           # Docker compose
├── requirements.txt             # Зависимости
├── test_api.py                  # Интеграционные тесты API
├── test_parser.py               # Тест парсера FPL
├── check_tables.py              # Проверка таблиц БД
└── README.md                    # Документация
```

---

## API Endpoints

### Основной endpoint
```
GET/POST /meteo/
```

### Справочники
```
GET /cat/
```

### Регистрация
```
POST /reg/give
POST /reg/revoke
GET /reg/devices/
```

---

## Метеорологические данные

### 1. METAR — Регулярные сводки погоды
```bash
GET /meteo/?device=test&kind=metar&code=URSS
```
**Описание:** Текущая погода на аэродроме (ветер, видимость, облачность, температура, давление).

**Расшифровка METAR:**
```
METAR URSS 082209Z 33001MPS 5000 FEW300 07/M02 Q1010 NOSIG=
        │     │    │       │       │    │      │     │     │
        │     │    │       │       │    │      │     │     └─ Конец сообщения
        │     │    │       │       │    │      │     └─ Без значительных изменений
        │     │    │       │       │    │      └─ Давление 1010 гПа
        │     │    │       │       │    └─ Температура 7°C / точка росы -2°C
        │     │    │       │       └─ Облачность FEW на 300 футах
        │     │    │       └─ Видимость 5000 м
        │     │    └─ Ветер 330° 1 м/с
        │     └─ Время выпуска 08 число 22:09 UTC
        └─ Код аэродрома URSS (Сочи)
```

### 2. TAF — Прогноз погоды
```bash
GET /meteo/?device=test&kind=taf&code=UUDD
```
**Описание:** Прогноз погоды на 24 часа для аэродрома.

### 3. SIGMET — Опасные явления
```bash
GET /meteo/?device=test&kind=sigmet&code=ULLL
```
**Описание:** Опасные явления по маршруту полета (гроза, турбулентность, обледенение).

### 4. AIRMET — Опасные явления на малых высотах
```bash
GET /meteo/?device=test&kind=airmet&code=ULLL
```
**Описание:** Опасные явления ниже эшелона 100 (3000 м).

### 5. GAMET — Зональный прогноз
```bash
GET /meteo/?device=test&kind=gamet&area_name=TVER&area_number=5
```
**Описание:** Прогноз для полетов на малых высотах в определенном районе.

### 6. VFR — Категории полетов
```bash
GET /meteo/?device=test&kind=vfr&code=URSS.UUDD.UUEE
```
**Описание:** Категории полетов (визуальные/приборные) для аэродромов.

**Категории:**
- **VMC** — Visual Meteorological Conditions (визуальные условия)
- **IMC** — Instrument Meteorological Conditions (приборные условия)
- **LIFR** — Low Instrument Flight Rules (низкие приборные)
- **IFR** — Instrument Flight Rules (приборные)
- **MVFR** — Marginal VFR (пограничные)
- **VFR** — Visual Flight Rules (визуальные)

### 7. rwindtmp — Ветер/температура по маршруту
```bash
GET /meteo/?device=test&kind=rwindtmp&p[0]=x37.5y55.6z150t1685450553
```
**Описание:** Прогноз ветра и температуры на эшелонах полета.

**Формат точки:** `x[долгота]y[широта]z[эшелон]t[время]`

### 8. adwrng — Предупреждения по аэродрому
```bash
GET /meteo/?device=test&kind=adwrng&code=URSS
```
**Описание:** Опасные явления на аэродроме (гроза, туман, сильный ветер).

### 9. wswrng — Предупреждения о сдвиге ветра
```bash
GET /meteo/?device=test&kind=wswrng&code=URSS
```
**Описание:** Сдвиг ветра (опасен при посадке).

### 10-12. Данные ДМРЛ (радаров)
```bash
# Метеоявления
GET /meteo/?device=test&kind=wdmrl&code=rudn

# Интенсивность осадков
GET /meteo/?device=test&kind=pdmrl&code=rudn

# Верхняя граница облачности
GET /meteo/?device=test&kind=tdmrl&code=rudn
```
**Описание:** Данные с метеорологических радиолокаторов.

### 13. AIREP — Сообщения с бортов
```bash
GET /meteo/?device=test&kind=airep&code=ULLL
```
**Описание:** Сообщения от пилотов о фактической погоде.

### 14. ZOND — Радиозонды
```bash
GET /meteo/?device=test&kind=zond&code=ULLL
```
**Описание:** Траектории радиозондов (вертикальное зондирование атмосферы).

### 15. VAAC — Вулканический пепел
```bash
GET /meteo/?device=test&kind=vaac&code=RJTD
```
**Описание:** Консультативные сообщения о вулканическом пепле.

### 16. TCAC — Тропические циклоны
```bash
GET /meteo/?device=test&kind=tcac&code=KNHC
```
**Описание:** Консультативные сообщения о тропических циклонах.

### 17. SWX — Космическая погода
```bash
GET /meteo/?device=test&kind=swx
```
**Описание:** Космическая погода (солнечная активность, помехи GPS).

### 18. BRIEF — Полетная документация (PDF)
```bash
POST /meteo/?device=test&kind=brief
Content-Type: text/plain

(FPL-PPP1441-IS
-A319/M-SDFGHIRWY/B1L
-ULMM1735
-K0768F320 ASGO1K ASGOR T693 PILAN/K0779F330 M856 KUKUM/K0788F340
M856 GIKUR/K0801F350 T458 BEPOL BEPO1A
-ULLI0142 UUEE
-PBN/B1D1A1S2O1 DOF/230220 REG/PP00000 EET/ULLL0005 SEL/SSSS
CODE/000000 OPR/PPP RALT/ULMM ULLI RMK/ACASII EQUIPPED)
```
**Описание:** Генерирует PDF с полетной документацией.

---

## Справочники

### Список радаров
```bash
GET /cat/?code=dmrl-list
```

### Метеоявления
```bash
GET /cat/?code=dmrl-phenomena
```

### Интенсивность осадков
```bash
GET /cat/?code=dmrl-intensities
```

### Высота облачности
```bash
GET /cat/?code=dmrl-heights
```

---

## Авторизация и регистрация

### Авторизация
Все запросы требуют заголовок:
```
AUTHORIZATION: Bearer <token>
```

### Выдача ключей
```bash
POST /reg/give
AUTHORIZATION: Bearer <admin_key>

{
  "id": "request-123",
  "number": 3
}
```

### Отзыв ключей
```bash
POST /reg/revoke
AUTHORIZATION: Bearer <admin_key>

{
  "tokens": ["token1", "token2"]
}
```

### Список устройств
```bash
GET /reg/devices/
AUTHORIZATION: Bearer <user_token>
```

---

## База данных

### Таблицы:

#### 1. aerodromes
| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | Автоинкремент |
| icao_code | varchar(4) | ICAO код (URSS) |
| iata_code | varchar(3) | IATA код (AER) |
| name | varchar(100) | Название |
| latitude | float | Широта |
| longitude | float | Долгота |
| elevation | float | Высота (м) |

#### 2. radars
| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | Автоинкремент |
| code | varchar(10) | Код радара (rudn) |
| name_ru | varchar(100) | Название на русском |
| name_en | varchar(100) | Название на английском |
| latitude | float | Широта |
| longitude | float | Долгота |
| range_km | integer | Радиус действия (км) |
| status | integer | 0 - не работает, 1 - работает |

---

## Тестирование

### Все тесты
```bash
pytest tests/ -v
```

### Отдельные тесты
```bash
# Авторизация
pytest tests/test_auth.py -v

# Метеоданные
pytest tests/test_meteo.py -v

# Rate limiting
pytest tests/test_rate_limit.py -v

# SIGMET/AIRMET/GAMET
pytest tests/test_sigmet_airmet_gamet.py -v

# Новые функции
pytest tests/test_new_features.py -v

# Специальные данные
pytest tests/test_special_data.py -v

# PDF
pytest tests/test_brief.py -v
```

### Интеграционные тесты
```bash
python test_api.py
```

### Проверка парсера
```bash
python test_parser.py
```

### Проверка БД
```bash
python check_tables.py
```

---

## Сокращения и термины

### Авиационные коды
| Код | Значение |
|-----|----------|
| ICAO | International Civil Aviation Organization (4 буквы) |
| IATA | International Air Transport Association (3 буквы) |
| FPL | Flight Plan (план полета) |

### Метеорологические термины
| Термин | Расшифровка |
|--------|-------------|
| METAR | METeorological Aerodrome Report (сводка погоды) |
| TAF | Terminal Aerodrome Forecast (прогноз) |
| SIGMET | SIGnificant METeorological information |
| AIRMET | AIRmen's METeorological information |
| GAMET | General Aviation METeorological forecast |
| CAVOK | Ceiling And Visibility OK (хорошая погода) |
| NOSIG | No Significant change (без изменений) |
| QNH | Давление, приведенное к уровню моря |

### Категории полетов
| Код | Расшифровка | Условия |
|-----|-------------|---------|
| VMC | Visual Meteorological Conditions | Видимость ≥ 5 км, облака ≥ 1500 м |
| IMC | Instrument Meteorological Conditions | Видимость < 5 км или облака < 1500 м |
| LIFR | Low Instrument Flight Rules | Видимость < 1600 м или облака < 500 м |
| IFR | Instrument Flight Rules | Видимость < 5000 м или облака < 1000 м |
| MVFR | Marginal VFR | Видимость < 8000 м или облака < 3000 м |
| VFR | Visual Flight Rules | Видимость ≥ 8000 м и облака ≥ 3000 м |

### Аэродромы (примеры)
| ICAO | IATA | Город |
|------|------|-------|
| URSS | AER | Сочи |
| UUDD | DME | Москва (Домодедово) |
| UUEE | SVO | Москва (Шереметьево) |
| ULLI | LED | Санкт-Петербург |
| ULMM | MMK | Мурманск |

### Радары (примеры)
| Код | Название |
|-----|----------|
| rudn | Москва (Внуково) |
| rudm | Москва (Домодедово) |
| rusm | Москва (Шереметьево) |
| ruled | Санкт-Петербург (Пулково) |

---

## Примеры запросов

### Через curl
```bash
# METAR для Сочи
curl -H "AUTHORIZATION: Bearer cb1d3a52-d4a1-1234-8045-75ae7a493bd7" \
  "http://localhost:5000/meteo/?device=test&kind=metar&code=URSS"

# TAF для Домодедово
curl -H "AUTHORIZATION: Bearer cb1d3a52-d4a1-1234-8045-75ae7a493bd7" \
  "http://localhost:5000/meteo/?device=test&kind=taf&code=UUDD"

# Справочник радаров
curl -H "AUTHORIZATION: Bearer cb1d3a52-d4a1-1234-8045-75ae7a493bd7" \
  "http://localhost:5000/cat/?code=dmrl-list"

# PDF документация
curl -X POST \
  -H "AUTHORIZATION: Bearer cb1d3a52-d4a1-1234-8045-75ae7a493bd7" \
  -d "(FPL-SDM6346-IS...)" \
  "http://localhost:5000/meteo/?device=test&kind=brief" \
  -o briefing.pdf
```

### Через Python
```python
import requests

headers = {'AUTHORIZATION': 'Bearer cb1d3a52-d4a1-1234-8045-75ae7a493bd7'}

# METAR
response = requests.get(
    'http://localhost:5000/meteo/',
    params={'device': 'test', 'kind': 'metar', 'code': 'URSS'},
    headers=headers
)
print(response.json())
```

---

## Docker

### Сборка образа
```bash
docker build -t weather-server .
```

### Запуск через docker-compose
```bash
docker-compose up --build
```

### Остановка
```bash
docker-compose down
```

---

## Ограничения (Rate Limiting)

| Лимит | Значение |
|-------|----------|
| Запросов в минуту | 100 |
| Запросов в сутки | 10000 |

При превышении лимита возвращается HTTP 429 (Too Many Requests).

---

## Обработка ошибок

| Код | Описание |
|-----|----------|
| 200 | Успех |
| 400 | Неверный запрос (нет device, kind, points) |
| 401 | Не авторизован |
| 404 | Не найдено (аэродром, радар, данные) |
| 405 | Метод не разрешен |
| 429 | Превышен лимит запросов |
| 500 | Внутренняя ошибка сервера |
