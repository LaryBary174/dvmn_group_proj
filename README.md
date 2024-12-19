# API для управления услугами салона красоты

Эндпоинты сформированы на Django для получения данных по услугам салонов красоты и возможностью записываться онлайн


## Описание моделей
`Specialist` модель специалиста. Специалист связа со следующими моделями:

- `Salon` салоны где работает специалист 
- `Service` услуги, которые оказывает специалист

За расписание отвечает модель `Schedule`, у расписания есть поля specialist, salon, date, time (какой специалист в каком салоне в эту дату работает) и поле `is_available` отвечает свободен ли слот или нет. Необходимое поле для записи клиента в будущем

`Appointment` модель записи клиента к выбранному специалисту

## Установка
- Скачать код
- Установить все зависимости:
```
pip install -r requirements.txt
```
- Создайте БД командой
``` 
py manage.py migrate
```
- Запуск
```
py manage.py runserver
```

## API
GET /api/salons  получение списка всех салонов

Пример ответа:
```
    {
        "id": 1,
        "address": "Салон 1 Адрес 1",
        "phone": "1234"
    }
```

GET /api/services получение списка всех услуг

Пример ответа:
```
    {
        "id": 1,
        "title": "окрашивание волос",
        "description": "окрашивание волос",
        "price": "1000.00"
    }
```

GET /api/specialists получение списка всех специалистов, возможен запрос с параметрами для сортировки

Параметры запроса:
- service_id - ID услуги
- salon_id - ID салона

Пример ответа:
``` 
api/specialists/?salon_id=1&service_id=1
[    
    {
        "id": 1,
        "name": "Ольга",
        "salon": [
            {
                "id": 1,
                "address": "Салон 1 Адрес 1",
                "phone": "1234"
            },
            {
                "id": 3,
                "address": "Салон 3 Адрес 3",
                "phone": "12345"
            }
        ],
        "service": [
            {
                "id": 1,
                "title": "окрашивание волос",
                "description": "окрашивание волос",
                "price": "1000.00"
            },
            {
                "id": 2,
                "title": "укладка волос",
                "description": "укладка волос",
                "price": "1000.00"
            }
        ]
    }
]
```

GET /api/schedules получение расписание всех специалистов, для сортировки запрос с параметрами

Параметры запроса:
- specialist_id - ID специалиста
- salon_id - ID салона
- date - дата в формате `ГГГГ-ММ-ДД`

Пример ответа:
```
/api/schedules/?salon_id=1&specialist_id=1&date=2024-12-19

[
    {
        "id": 1,
        "specialist": "Ольга",
        "date": "2024-12-19",
        "time": "11:00:00",
        "is_available": true,
        "salon": "Салон 1 Адрес 1"
    }
]
```

POST /api/appointments-new/create/ создание записи на услугу

Тело запроса:
- customer - Имя клиента(str)
- customer_phone - номер телефона(str)
- schedule - ID расписания свободного с датой и временем

Пример ответа:
```
{
    "message": "Успешно записаны!",
    "Адрес салона": "Салон 3 Адрес 3",
    "Мастер": "Ольга",
    "Дата": "2024-12-19",
    "Время": "21:00:00"
}
или 
{
    "error": "Выбранного времени не существует или занято."
}
```

