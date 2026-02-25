"""
Главный модуль для запуска системы управления пассажирским транспортом
"""

from transport_company import TransportCompany
from manager import TransportManager
from models import Bus, Tram, Trolleybus, Employee, Passenger, Route
from datetime import datetime, timedelta
from exceptions import TransportException


def create_initial_company():
    """Создание начальной транспортной компании с демонстрационными данными"""
    company = TransportCompany("ГУП 'Мосгортранс' Филиал Восточный")

    # Транспорт
    transports_data = [
        # Автобусы
        ("bus", "ЛиАЗ", "5292.65 (Гармония)", 2022, 45, "т36"),        # Самый массовый автобус Москвы
        ("bus", "МАЗ", "203.085", 2021, 40, "32"),                      # МАЗы тоже часто встречаются
        ("bus", "НефАЗ", "5299-40-57", 2023, 35, "817"),                # НефАЗы работают на маршрутах
        ("bus", "ПАЗ", "320435-04 (Vector Next)", 2022, 25, "1064"),    # ПАЗики на областных маршрутах
        ("bus", "ЛиАЗ", "4292.60", 2023, 30, "723"),                     # Средние автобусы
        # Электробусы
        ("bus", "КамАЗ", "6282 (Электробус)", 2023, 35, "107"),         # Электробусы КамАЗ
        ("bus", "ЛиАЗ", "6274 (Электробус)", 2023, 35, "с916"),         # Электробусы ЛиАЗ
        # Трамваи
        ("tram", "ПК ТС", "71-931М 'Витязь-М'", 2021, 45, "17"),        # Современные трамваи
        ("tram", "УКВЗ", "71-623-04", 2019, 38, "36"),                  # Усть-Катавские трамваи
        ("tram", "Татра", "T3R.PV", 2018, 32, "27"),                     # Чешские трамваи (ещё есть)
        # Троллейбусы
        ("trolley", "СВАРЗ", "6238.00 'Синара'", 2022, 40, "23"),       # Современные троллейбусы
        ("trolley", "Тролза", "5275.05 'Оптима'", 2020, 38, "35"),       # Тролза (Химки, Видное)
    ]

    for trans_type, brand, model, year, capacity, route_line in transports_data:
        try:
            if trans_type == "bus":
                transport = Bus(0, brand, model, year, capacity, route_line)
            elif trans_type == "tram":
                transport = Tram(0, brand, model, year, capacity, route_line)
            elif trans_type == "trolley":
                transport = Trolleybus(0, brand, model, year, capacity, route_line)
            company.add_transport(transport)
        except Exception as e:
            print(f"Ошибка при создании транспорта: {e}")

    # Сотрудники
    employees_data = [
        # Водители
        ("Корнеев Валентин Петрович", "+7-916-432-15-67", "Водитель автобуса 1 класса", 65000.0),
        ("Мухин Александр Борисович", "+7-925-876-34-21", "Водитель электробуса", 70000.0),
        ("Цветков Виктор Иванович", "+7-903-543-87-09", "Водитель трамвая", 62000.0),
        ("Жуков Дмитрий Сергеевич", "+7-910-234-76-54", "Водитель троллейбуса", 58000.0),
        # Диспетчеры
        ("Панкратова Нина Васильевна", "+7-499-234-56-78", "Старший диспетчер", 55000.0),
        ("Сорокина Людмила Георгиевна", "+7-498-765-43-21", "Диспетчер", 48000.0),
        # Механики
        ("Тихомиров Геннадий Аркадьевич", "+7-916-555-34-12", "Механик автоколонны", 60000.0),
        ("Ершов Константин Николаевич", "+7-925-777-89-23", "Слесарь по ремонту", 52000.0),
        # Контроллеры
        ("Мельникова Тамара Ильинична", "+7-903-444-56-78", "Контролер", 45000.0),
        # Медицинский работник
        ("Воронцова Ангелина Дмитриевна", "+7-910-888-45-67", "Фельдшер предрейсового осмотра", 54000.0)
    ]

    for name, phone, position, salary in employees_data:
        try:
            employee = Employee(0, name, phone, position, salary)
            company.add_employee(employee)
        except Exception as e:
            print(f"Ошибка при создании сотрудника: {e}")

    passengers_data = [
        # Я - Шивринский Вячеслав Владимирович (студент, 50%)
        ("Шивринский Вячеслав Владимирович", "+7-977-123-45-67", "slava.shivrinsky@student.ru", 50.0, "студент"),

        # Петровна Мария Ивановна - пенсионерка (бесплатно)
        ("Петрова Мария Ивановна", "+7-495-234-56-78", "", 100.0, "пенсионер"),

        # Соколов Андрей Дмитриевич - еще один студент (50%)
        ("Соколов Андрей Дмитриевич", "+7-925-876-54-32", "andrey.sokolov@student.ru", 50.0, "студент"),

        # Морозова Елизавета Алексеевна - ребенок (бесплатно)
        ("Морозова Елизавета Алексеевна", "+7-903-987-65-43", "", 100.0, "ребенок"),

        # Ковалёв Сергей Николаевич - взрослый (без льгот)
        ("Ковалёв Сергей Николаевич", "+7-910-555-77-88", "sergey.kovalev@work.ru", 0.0, "взрослый")
    ]

    for name, phone, email, discount, category in passengers_data:
        try:
            passenger = Passenger(0, name, phone, email, discount, category)
            company.add_passenger(passenger)
        except Exception as e:
            print(f"Ошибка при создании пассажира: {e}")

    # Маршруты
    routes_data = [
        ("т36", "ВДНХ (южная)", "Останкино", 8.5),           # Троллейбус 36
        ("32", "Парк Победы", "Фили", 12.0),                  # Автобус 32
        ("817", "Метро Домодедовская", "Зябликово", 6.3),     # Автобус 817
        ("1064", "Люберцы", "Метро Выхино", 15.7),            # Областной маршрут
        ("723", "Метро Бабушкинская", "Осташковская", 9.2),   # Автобус 723
        ("107", "Метро Партизанская", "Авиамоторная", 7.8),   # Электробус 107
        ("с916", "Метро Каховская", "Черёмушки", 11.4),       # Электробус с916
        ("17", "Медведково", "ВДНХ", 14.5),                    # Трамвай 17
        ("36", "Детский санаторий", "Метро Сокольники", 16.2), # Трамвай 36
        ("27", "Метро Дмитровская", "Михалково", 10.8),        # Трамвай 27
        ("23", "Химки", "Метро Сходненская", 22.5),            # Троллейбус 23
        ("35", "Видное", "Метро Кантемировская", 28.3)         # Троллейбус 35
    ]

    for number, start, end, distance in routes_data:
        try:
            route = Route(0, number, start, end, distance)
            company.add_route(route)
        except Exception as e:
            print(f"Ошибка при создании маршрута: {e}")

    # Демонстрационные рейсы с учетом льгот пассажиров
    try:
        drivers = company.get_drivers()
        active_transports = company.get_active_transports()

        # Рейс на электробусе 107 (самый современный)
        if drivers and active_transports and company.routes:
            route107 = company.get_route_by_number("107")
            # Ищем электробус
            electrobus = next((t for t in active_transports if "Электробус" in t.model), active_transports[0])
            # Ищем водителя
            driver = next((d for d in drivers if "электробус" in d.position.lower()), drivers[0])

            if route107:
                trip1 = Trip(
                    0, route107, electrobus, driver,
                    datetime.now().replace(hour=8, minute=15, second=0),
                    datetime.now().replace(hour=8, minute=50, second=0),
                    45.0  # стоимость проезда 45 рублей
                )
                # Добавим всех пассажиров в этот рейс
                for passenger in company.passengers:
                    try:
                        trip1.add_passenger(passenger)
                    except Exception as e:
                        print(f"Не удалось добавить пассажира {passenger.name}: {e}")
                company.add_trip(trip1)

            # Рейс на трамвае 17
            route17 = company.get_route_by_number("17")
            if route17:
                trip2 = Trip(
                    0, route17, active_transports[7], drivers[2],
                    datetime.now().replace(hour=17, minute=30, second=0),
                    datetime.now().replace(hour=18, minute=10, second=0),
                    45.0
                )
                # Добавим только студентов и взрослого
                for passenger in company.passengers:
                    if passenger.category in ["студент", "взрослый"]:
                        trip2.add_passenger(passenger)
                company.add_trip(trip2)

    except Exception as e:
        print(f"Ошибка при создании рейсов: {e}")

    return company


def main():
    """Главная функция"""
    print("=" * 70)
    print("     СИСТЕМА УПРАВЛЕНИЯ ПАССАЖИРСКИМ ТРАНСПОРТОМ Г. МОСКВЫ")
    print("=" * 70)

    try:
        company = create_initial_company()
        manager = TransportManager(company)

        company.display_info()

        # Вывод информации о льготах
        print("\n" + "=" * 50)
        print("ЛЬГОТНЫЕ КАТЕГОРИИ ПАССАЖИРОВ:")
        print("=" * 50)
        for passenger in company.passengers:
            discount_text = f"Скидка {passenger.discount}%" if passenger.discount > 0 else "Полная стоимость"
            if passenger.discount == 100:
                discount_text = "Бесплатный проезд"
            print(f"  {passenger.name}: {passenger.category} - {discount_text}")

        print("\nДля навигации используйте меню.")
        manager.interactive_mode()

    except TransportException as e:
        print(f"Ошибка в работе системы: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nРабота программы завершена.")


if __name__ == "__main__":
    main()