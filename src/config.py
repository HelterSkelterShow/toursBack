from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

SECRET_AUTH = os.environ.get('SECRET')
RESET_AND_VERIFICATION = os.environ.get('RESET_AND_VERIFICATION_SECRET')

TIME_TO_UPDATE = 5
TIME_TO_CANCEL = 3
TOURIST_TIME_TO_CANCEL = 3

TOURISTS_PER_PAGE = 20

CLAIMS_PER_PAGE = 10

TOURS_PER_PAGE = 20

SESSION_LIFETIME = 43200

MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE'))
MAX_FILE_SUM_SIZE = int(os.environ.get('MAX_FILE_SUM_SIZE'))

SMTP_USER=os.environ.get('SMTP_USER')
SMTP_PASSWORD=os.environ.get('SMTP_PASSWORD')

AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION=os.environ.get('AWS_DEFAULT_REGION')

COMMISSION = 1.05
# RABBIT_HOST = os.environ.get('RABBIT_HOST')
# RABBIT_PORT = os.environ.get('RABBIT_PORT')
# RABBIT_USERNAME = os.environ.get('RABBIT_USERNAME')
# RABBIT_PASSWORD = os.environ.get('RABBIT_PASSWORD')

categories=[
    {
    "code":"camping",
    "name":"Кемпинг"
    },
    {
    "code":"tracking",
    "name":"Трекинг"
    },
    {
    "code":"sightseeing",
    "name":"Обзорные"
    },
    {
    "code":"thematic",
    "name":"Тематические"
    },
    {
    "code":"urbantirizm",
    "name":"Городской туризм"
    },
]

complexity = [
    {
    "code":"1",
    "name":"Легко"
    },
    {
    "code":"2",
    "name":"Ниже среднего"
    },
    {
    "code":"3",
    "name":"Средне"
    },
    {
    "code":"4",
    "name":"Выше среднего"
    },
    {
    "code":"5",
    "name":"Экстрим"
    },
]

regions = [
        { "code": "1", "name": "Республика Адыгея" },
        { "code": "2", "name": "Республика Башкортостан" },
        { "code": "3", "name": "Республика Бурятия" },
        { "code": "4", "name": "Республика Алтай" },
        { "code": "5", "name": "Республика Дагестан" },
        { "code": "6", "name": "Республика Ингушетия" },
        { "code": "7", "name": "Кабардино-Балкарская Республика" },
        { "code": "8", "name": "Республика Калмыкия" },
        { "code": "9", "name": "Карачаево-Черкесская Республика" },
        { "code": "10", "name": "Республика Карелия" },
        { "code": "11", "name": "Республика Коми" },
        { "code": "12", "name": "Республика Марий Эл" },
        { "code": "13", "name": "Республика Мордовия" },
        { "code": "14", "name": "Республика Саха (Якутия)" },
        { "code": "15", "name": "Республика Северная Осетия - Алания" },
        { "code": "16", "name": "Республика Татарстан" },
        { "code": "17", "name": "Республика Тыва" },
        { "code": "18", "name": "Удмуртская Республика" },
        { "code": "19", "name": "Республика Хакасия" },
        { "code": "20", "name": "Чеченская Республика"},
        { "code": "21", "name": "Чувашская Республика" },
        { "code": "22", "name": "Алтайский край" },
        { "code": "23", "name": "Краснодарский край" },
        { "code": "24", "name": "Красноярский край" },
        { "code": "25", "name": "Приморский край" },
        { "code": "26", "name": "Ставропольский край" },
        { "code": "27", "name": "Хабаровский край" },
        { "code": "28", "name": "Амурская область" },
        { "code": "29", "name": "Архангельская область" },
        { "code": "30", "name": "Астраханская область" },
        { "code": "31", "name": "Белгородская область" },
        { "code": "32", "name": "Брянская область" },
        { "code": "33", "name": "Владимирская область" },
        { "code": "34", "name": "Волгоградская область" },
        { "code": "35", "name": "Вологодская область" },
        { "code": "36", "name": "Воронежская область" },
        { "code": "37", "name": "Ивановская область" },
        { "code": "38", "name": "Иркутская область" },
        { "code": "39", "name": "Калининградская область" },
        { "code": "40", "name": "Калужская область" },
        { "code": "41", "name": "Камчатский край" },
        { "code": "42", "name": "Кемеровская область" },
        { "code": "43", "name": "Кировская область" },
        { "code": "44", "name": "Костромская область" },
        { "code": "45", "name": "Курганская область" },
        { "code": "46", "name": "Курская область" },
        { "code": "47", "name": "Ленинградская область" },
        { "code": "48", "name": "Липецкая область" },
        { "code": "49", "name": "Магаданская область" },
        { "code": "50", "name": "Московская область" },
        { "code": "51", "name": "Мурманская область" },
        { "code": "52", "name": "Нижегородская область" },
        { "code": "53", "name": "Новгородская область" },
        { "code": "54", "name": "Новосибирская область" },
        { "code": "55", "name": "Омская область" },
        { "code": "56", "name": "Оренбургская область" },
        { "code": "57", "name": "Орловская область" },
        { "code": "58", "name": "Пензенская область" },
        { "code": "59", "name": "Пермский край" },
        { "code": "60", "name": "Псковская область" },
        { "code": "61", "name": "Ростовская область" },
        { "code": "62", "name": "Рязанская область" },
        { "code": "63", "name": "Самарская область" },
        { "code": "64", "name": "Саратовская область" },
        { "code": "65", "name": "Сахалинская область" },
        { "code": "66", "name": "Свердловская область" },
        { "code": "67", "name": "Смоленская область" },
        { "code": "68", "name": "Тамбовская область" },
        { "code": "69", "name": "Тверская область" },
        { "code": "70", "name": "Томская область" },
        { "code": "71", "name": "Тульская область" },
        { "code": "72", "name": "Тюменская область" },
        { "code": "73", "name": "Ульяновская область" },
        { "code": "74", "name": "Челябинская область" },
        { "code": "75", "name": "Забайкальский край" },
        { "code": "76", "name": "Ярославская область" },
        { "code": "77", "name": "Москва" },
        { "code": "78", "name": "Санкт-Петербург" },
        { "code": "79", "name": "Еврейская автономная область" },
        { "code": "82", "name": "Ненецкий автономный округ" },
        { "code": "83", "name": "Ханты-Мансийский автономный округ - Югра" },
        { "code": "86", "name": "Чукотский автономный округ" },
        { "code": "87", "name": "Ямало-Ненецкий автономный округ" },
    ]