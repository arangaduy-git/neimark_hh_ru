from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main():
    main_kb_list = [
        [InlineKeyboardButton(text="Неполный день", callback_data='part_time')],
        [InlineKeyboardButton(text="От 4 часов в день", callback_data='from_4_hours')],
        [InlineKeyboardButton(text="По вечерам", callback_data='in_evening')],
        [InlineKeyboardButton(text="По выходным", callback_data='on_weekends')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=main_kb_list)


def specialization():
    specialization_kb_list = [
        [InlineKeyboardButton(text="🛡️ Безопасность (cпециалист по ИБ)", callback_data='security')],
        [InlineKeyboardButton(text="🏡 Обслуживающий персонал (курьер, дворник)", callback_data='service_personnel')],
        [InlineKeyboardButton(text="💻 Информационные технологии", callback_data='information_technology')],
        [InlineKeyboardButton(text="🎨 Массмедиа (фотограф, дизайнер)", callback_data='mass_media')],
        [InlineKeyboardButton(text="💊 Медицина (аптекарь, лаборант)", callback_data='medicine')],
        [InlineKeyboardButton(text="👷 Рабочий персонал(сварщик, слесарь,механик)", callback_data='workers')],
        [InlineKeyboardButton(text="🛍️ Розничная торговля(продавец, промоутер)", callback_data='retail')],
        [InlineKeyboardButton(text="🏋️ Спортивные клубы, фитнес, салоны красоты", callback_data='fitness')],
        [InlineKeyboardButton(text="❓ Не определился", callback_data='not_decided')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=specialization_kb_list)


def industry():
    industry_kb_list = [
        [InlineKeyboardButton(text="🚗 Автомобильный бизнес", callback_data='car')],
        [InlineKeyboardButton(text="🏨 Гостиницы, рестораны, общепит, кейтеринг", callback_data='hotels')],
        [InlineKeyboardButton(text="🏢 ЖКХ", callback_data='JKH')],
        [InlineKeyboardButton(text="💻 Информационные технологии, интернет", callback_data='internet')],
        [InlineKeyboardButton(text="💊 Медицина, фармацевтика, аптеки", callback_data='medicine1')],
        [InlineKeyboardButton(text="🌍 Общественная деятельность, благотворительность", callback_data='social')],
        [InlineKeyboardButton(text="🥫 Продукты питания", callback_data='food')],
        [InlineKeyboardButton(text="⚙️ Промышленное оборудование, техника, станки", callback_data='components')],
        [InlineKeyboardButton(text="🛍️ Розничная торговля", callback_data='retail1')],
        [InlineKeyboardButton(text="🏗️ Строительство, недвижимость, проектирование", callback_data='building')],
        [InlineKeyboardButton(text="🎁 Товары народного потребления (непищевые)", callback_data='non-food')],
        [InlineKeyboardButton(text="📱 Электроника, бытовая техника", callback_data='computers')],
        [InlineKeyboardButton(text="❓ Не определился", callback_data='non_decided')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=industry_kb_list)


def experience():
    experience_kb_list = [
        [InlineKeyboardButton(text="🌱 Не имеет значения", callback_data='doesnt_matter')],
        [InlineKeyboardButton(text="🌱 Нет опыта", callback_data='0')],
        [InlineKeyboardButton(text="📅 От 1 года до 3 лет", callback_data='1-3')],
        [InlineKeyboardButton(text="📅 От 3 до 6 лет", callback_data='3-6')],
        [InlineKeyboardButton(text="📅 Более 6 лет", callback_data='6+')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=experience_kb_list)


def disability():
    disability_kb_list = [
        [InlineKeyboardButton(text="💚 Да", callback_data='yes')],
        [InlineKeyboardButton(text="💚 Нет", callback_data='no')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=disability_kb_list)


def region():
    region_kb_list = [
        [InlineKeyboardButton(text="Москва", callback_data='moscow')],
        [InlineKeyboardButton(text="Московская область", callback_data='moscow_region')],
        [InlineKeyboardButton(text="Санкт-Петербург", callback_data='petersburg')],
        [InlineKeyboardButton(text="Ленинградская область", callback_data='leningrad')],
        [InlineKeyboardButton(text="Севастополь", callback_data='sevastopol')],
        [InlineKeyboardButton(text="Краснодарский край", callback_data='krasnodar')],
        [InlineKeyboardButton(text="Республика Татарстан", callback_data='tatarstan')],
        [InlineKeyboardButton(text="Нижегородская область", callback_data='nizhny_novgorod')],
        [InlineKeyboardButton(text="Ярославская область", callback_data='yaroslavl')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=region_kb_list)
