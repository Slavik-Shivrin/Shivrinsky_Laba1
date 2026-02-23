from transport_company import TransportCompany
from models import Bus, Tram, Trolleybus, Employee, Passenger, Route, Trip
from exceptions import TransportException, NotFoundException, InvalidDataException
from datetime import datetime, timedelta
from typing import Optional

class TransportManager:
    """Менеджер для интерактивной работы с транспортной компанией"""

    def __init__(self, company: TransportCompany):
        self.company = company

    def interactive_mode(self):
        """Интерактивный режим работы"""
        while True:
            try:
                self._show_menu()
                choice = input("\nВыберите действие: ").strip()

                if choice == '0':
                    print("До свидания!")
                    break
                elif choice == '1':
                    self._show_all_transports()
                elif choice == '2':
                    self._add_transport()
                elif choice == '3':
                    self._show_all_employees()
                elif choice == '4':
                    self._add_employee()
                elif choice == '5':
                    self._show_all_passengers()
                elif choice == '6':
                    self._add_passenger()
                elif choice == '7':
                    self._show_all_routes()
                elif choice == '8':
                    self._add_route()
                elif choice == '9':
                    self._show_all_trips()
                elif choice == '10':
                    self._add_trip()
                elif choice == '11':
                    self._book_ticket()
                elif choice == '12':
                    self._save_data()
                elif choice == '13':
                    self._load_data()
                else:
                    print("Неверный выбор. Пожалуйста, выберите пункт из меню.")

            except TransportException as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Непредвиденная ошибка: {e}")
                print("Попробуйте снова.")

    def _show_menu(self):
        """Отображение меню"""
        print("\n" + "=" * 50)
        print("     СИСТЕМА УПРАВЛЕНИЯ ПАССАЖИРСКИМ ТРАНСПОРТОМ")
        print("=" * 50)
        print("1. Показать весь транспорт")
        print("2. Добавить транспорт")
        print("3. Показать всех сотрудников")
        print("4. Добавить сотрудника")
        print("5. Показать всех пассажиров")
        print("6. Добавить пассажира")
        print("7. Показать все маршруты")
        print("8. Добавить маршрут")
        print("9. Показать все рейсы")
        print("10. Создать новый рейс")
        print("11. Купить билет")
        print("12. Сохранить данные в файл")
        print("13. Загрузить данные из файла")
        print("0. Выход")

    def _show_all_transports(self):
        """Показать весь транспорт"""
        if not self.company.transports:
            print("\nТранспорт не найден.")
            return

        print("\n--- ТРАНСПОРТНЫЕ СРЕДСТВА ---")
        for t in self.company.transports:
            print(f"[{t.id}] {t}")

    def _add_transport(self):
        """Добавить новое транспортное средство"""
        print("\n--- ДОБАВЛЕНИЕ ТРАНСПОРТА ---")
        print("1. Автобус")
        print("2. Трамвай")

        choice = input("Выберите тип транспорта: ").strip()

        try:
            brand = input("Марка: ").strip()
            model = input("Модель: ").strip()
            year = int(input("Год выпуска: ").strip())
            capacity = int(input("Вместимость: ").strip())

            if choice == '1':
                route_num = input("Номер маршрута (если есть): ").strip()
                transport = Bus(0, brand, model, year, capacity, route_num)
            elif choice == '2':
                line_num = input("Номер линии (если есть): ").strip()
                transport = Tram(0, brand, model, year, capacity, line_num)
            else:
                print("Неверный выбор")
                return

            self.company.add_transport(transport)
            print(f"Транспорт успешно добавлен с ID {transport.id}")

        except ValueError as e:
            raise InvalidDataException("Ошибка ввода числовых данных")

    def _show_all_employees(self):
        """Показать всех сотрудников"""
        if not self.company.employees:
            print("\nСотрудники не найдены.")
            return

        print("\n--- СОТРУДНИКИ ---")
        for e in self.company.employees:
            print(f"[{e.id}] {e}")

    def _add_employee(self):
        """Добавить нового сотрудника"""
        print("\n--- ДОБАВЛЕНИЕ СОТРУДНИКА ---")

        try:
            name = input("ФИО: ").strip()
            phone = input("Телефон: ").strip()
            position = input("Должность: ").strip()
            salary = float(input("Зарплата: ").strip())

            employee = Employee(0, name, phone, position, salary)
            self.company.add_employee(employee)
            print(f"Сотрудник успешно добавлен с ID {employee.id}")

        except ValueError as e:
            raise InvalidDataException("Ошибка ввода числовых данных")

    def _show_all_passengers(self):
        """Показать всех пассажиров"""
        if not self.company.passengers:
            print("\nПассажиры не найдены.")
            return

        print("\n--- ПАССАЖИРЫ ---")
        for p in self.company.passengers:
            print(f"[{p.id}] {p}")

    def _add_passenger(self):
        """Добавить нового пассажира"""
        print("\n--- ДОБАВЛЕНИЕ ПАССАЖИРА ---")

        try:
            name = input("ФИО: ").strip()
            phone = input("Телефон: ").strip()
            email = input("Email (необязательно): ").strip()
            discount = float(input("Скидка (0-100, по умолчанию 0): ").strip() or "0")

            passenger = Passenger(0, name, phone, email, discount)
            self.company.add_passenger(passenger)
            print(f"Пассажир успешно добавлен с ID {passenger.id}")

        except ValueError as e:
            raise InvalidDataException("Ошибка ввода числовых данных")

    def _show_all_routes(self):
        """Показать все маршруты"""
        if not self.company.routes:
            print("\nМаршруты не найдены.")
            return

        print("\n--- МАРШРУТЫ ---")
        for r in self.company.routes:
            print(f"[{r.id}] {r}")

    def _add_route(self):
        """Добавить новый маршрут"""
        print("\n--- ДОБАВЛЕНИЕ МАРШРУТА ---")

        try:
            number = input("Номер маршрута: ").strip()
            start = input("Начальная точка: ").strip()
            end = input("Конечная точка: ").strip()
            distance = float(input("Расстояние (км): ").strip())

            route = Route(0, number, start, end, distance)
            self.company.add_route(route)
            print(f"Маршрут успешно добавлен с ID {route.id}")

        except ValueError as e:
            raise InvalidDataException("Ошибка ввода числовых данных")

    def _show_all_trips(self):
        """Показать все рейсы с детальной информацией"""
        if not self.company.trips:
            print("\n❌ Рейсы не найдены.")
            return

        print("\n" + "=" * 80)
        print("📋 СПИСОК ВСЕХ РЕЙСОВ")
        print("=" * 80)

        # Группируем рейсы по датам
        trips_by_date = {}
        for trip in self.company.trips:
            date_key = trip.departure_time.strftime('%d.%m.%Y')
            if date_key not in trips_by_date:
                trips_by_date[date_key] = []
            trips_by_date[date_key].append(trip)

        # Сортируем даты
        for date in sorted(trips_by_date.keys()):
            print(f"\n📅 {date}:")
            print("-" * 80)

            # Сортируем рейсы по времени отправления
            for trip in sorted(trips_by_date[date], key=lambda x: x.departure_time):
                try:
                    # Базовая информация в одну строку
                    dep_time = trip.departure_time.strftime('%H:%M')
                    arr_time = trip.arrival_time.strftime('%H:%M')

                    # Иконка транспорта
                    if "Электробус" in trip.transport.model:
                        transport_icon = "⚡"
                    elif isinstance(trip.transport, Bus):
                        transport_icon = "🚌"
                    elif isinstance(trip.transport, Tram):
                        transport_icon = "🚊"
                    elif isinstance(trip.transport, Trolleybus):
                        transport_icon = "🔌"
                    else:
                        transport_icon = "🚍"

                    # Получаем имя водителя (фамилия и инициалы)
                    driver_name_parts = trip.driver.name.split()
                    if len(driver_name_parts) >= 2:
                        driver_short = f"{driver_name_parts[0]} {driver_name_parts[1][0]}."
                    else:
                        driver_short = trip.driver.name

                    # Строка с основной информацией
                    print(f"\n{transport_icon} РЕЙС #{trip.id} | Маршрут {trip.route.number}")
                    print(f"   📍 {trip.route.start_point} → {trip.route.end_point} ({trip.route.distance} км)")
                    print(
                        f"   ⏰ {dep_time} - {arr_time} | В пути: {self._format_duration(trip.arrival_time - trip.departure_time)}")
                    print(f"   🚌 Транспорт: {trip.transport.brand} {trip.transport.model} ({trip.transport.year} г.)")
                    print(f"   👨‍✈️ Водитель: {trip.driver.name} ({trip.driver.position})")
                    print(f"   💰 Стоимость проезда: {trip.fare} руб.")
                    print(
                        f"   👥 Места: {trip.get_passenger_count()}/{trip.transport.capacity} занято | Свободно: {trip.get_free_seats()}")

                    # Выручка с учетом льгот
                    revenue = trip.get_total_revenue()
                    print(f"   💵 Выручка за рейс: {revenue:.2f} руб.")

                    # Показываем пассажиров
                    if trip.passengers:
                        print("   📋 ПАССАЖИРЫ:")
                        # Группируем по категориям
                        passengers_by_cat = {}
                        for p in trip.passengers:
                            if p.category not in passengers_by_cat:
                                passengers_by_cat[p.category] = []
                            passengers_by_cat[p.category].append(p)

                        for category, cat_passengers in passengers_by_cat.items():
                            # Эмодзи для разных категорий
                            cat_emoji = {
                                "пенсионер": "👴",
                                "студент": "🎓",
                                "ребенок": "🧒",
                                "взрослый": "👤"
                            }.get(category, "👤")

                            print(f"      {cat_emoji} {category.capitalize()} ({len(cat_passengers)}):")
                            for p in cat_passengers:
                                льгота = f"(скидка {p.discount}%)" if p.discount > 0 else ""
                                print(f"         • {p.name} {льгота}")
                    else:
                        print("   📋 Пассажиров нет")

                except Exception as e:
                    print(f"   ⚠️ Ошибка при отображении рейса {trip.id}: {e}")

                print("-" * 60)

    def _format_duration(self, duration):
        """Форматирование продолжительности"""
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        if hours > 0:
            return f"{hours}ч {minutes}мин"
        else:
            return f"{minutes}мин"

    def _add_trip(self):
        """Создать новый рейс"""
        print("\n--- СОЗДАНИЕ РЕЙСА ---")

        # Показываем доступные маршруты
        if not self.company.routes:
            print("Сначала добавьте маршруты!")
            return

        print("\nДоступные маршруты:")
        for r in self.company.routes:
            print(f"[{r.id}] {r}")

        try:
            route_id = int(input("ID маршрута: ").strip())
            route = self.company.get_route(route_id)
            if not route:
                raise NotFoundException("Маршрут не найден")

            # Показываем доступный транспорт
            active_transports = self.company.get_active_transports()
            if not active_transports:
                print("Нет доступного транспорта!")
                return

            print("\nДоступный транспорт:")
            for t in active_transports:
                print(f"[{t.id}] {t}")

            transport_id = int(input("ID транспорта: ").strip())
            transport = self.company.get_transport(transport_id)
            if not transport or transport.status != transport.STATUS_ACTIVE:
                raise NotFoundException("Транспорт не найден или не активен")

            # Показываем доступных водителей
            drivers = self.company.get_drivers()
            if not drivers:
                print("Нет доступных водителей!")
                return

            print("\nДоступные водители:")
            for d in drivers:
                print(f"[{d.id}] {d}")

            driver_id = int(input("ID водителя: ").strip())
            driver = self.company.get_employee(driver_id)
            if not driver:
                raise NotFoundException("Водитель не найден")

            # Время рейса
            date_str = input("Дата отправления (ГГГГ-ММ-ДД): ").strip()
            time_str = input("Время отправления (ЧЧ:ММ): ").strip()
            departure = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

            # Рассчет времени прибытия (примерно)
            travel_hours = route.distance / 40  # средняя скорость 40 км/ч
            arrival = departure + timedelta(hours=travel_hours)

            fare = float(input("Стоимость проезда (руб): ").strip())

            trip = Trip(0, route, transport, driver, departure, arrival, fare)
            self.company.add_trip(trip)
            print(f"Рейс успешно создан с ID {trip.id}")

        except ValueError as e:
            raise InvalidDataException("Ошибка ввода данных")

    def _book_ticket(self):
        """Купить билет на рейс"""
        print("\n--- ПОКУПКА БИЛЕТА ---")

        if not self.company.trips:
            print("Нет доступных рейсов!")
            return

        # Показываем доступные рейсы
        print("\nДоступные рейсы:")
        for t in self.company.trips:
            if t.get_free_seats() > 0 and t.departure_time > datetime.now():
                print(f"[{t.id}] {t} (свободно {t.get_free_seats()} мест)")

        try:
            trip_id = int(input("ID рейса: ").strip())
            trip = None
            for t in self.company.trips:
                if t.id == trip_id:
                    trip = t
                    break

            if not trip:
                raise NotFoundException("Рейс не найден")

            if trip.get_free_seats() <= 0:
                raise TransportException("В этом рейсе нет свободных мест")

            # Показываем пассажиров
            if not self.company.passengers:
                print("Сначала зарегистрируйте пассажира!")
                return

            print("\nЗарегистрированные пассажиры:")
            for p in self.company.passengers:
                print(f"[{p.id}] {p}")

            passenger_id = int(input("ID пассажира: ").strip())
            passenger = self.company.get_passenger(passenger_id)
            if not passenger:
                raise NotFoundException("Пассажир не найден")

            trip.add_passenger(passenger)
            price = trip.fare * (1 - passenger.discount / 100)
            print(f"Билет успешно куплен! Стоимость: {price:.2f} руб.")

        except ValueError as e:
            raise InvalidDataException("Ошибка ввода данных")

    def _save_data(self):
        """Сохранение данных в файл"""
        print("\n--- СОХРАНЕНИЕ ДАННЫХ ---")
        print("1. Сохранить в JSON")
        print("2. Сохранить в XML")

        choice = input("Выберите формат: ").strip()

        try:
            filename = input("Имя файла (без расширения): ").strip()

            if choice == '1':
                self.company.save_to_json(f"{filename}.json")
                print(f"Данные сохранены в {filename}.json")
            elif choice == '2':
                self.company.save_to_xml(f"{filename}.xml")
                print(f"Данные сохранены в {filename}.xml")
            else:
                print("Неверный выбор")

        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def _load_data(self):
        """Загрузка данных из файла"""
        print("\n--- ЗАГРУЗКА ДАННЫХ ---")
        print("1. Загрузить из JSON")
        print("2. Загрузить из XML")

        choice = input("Выберите формат: ").strip()

        try:
            filename = input("Имя файла (без расширения): ").strip()

            if choice == '1':
                self.company.load_from_json(f"{filename}.json")
                print(f"Данные загружены из {filename}.json")
            elif choice == '2':
                self.company.load_from_xml(f"{filename}.xml")
                print(f"Данные загружены из {filename}.xml")
            else:
                print("Неверный выбор")

        except FileNotFoundError:
            print("Файл не найден")
        except Exception as e:
            print(f"Ошибка загрузки: {e}")