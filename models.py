from datetime import datetime
from typing import Optional, List
from exceptions import TransportException, InvalidDataException


class Person:
    """Базовый класс для всех людей"""

    def __init__(self, id: int, name: str, phone: str):
        if not name or len(name.strip()) == 0:
            raise InvalidDataException("Имя не может быть пустым")
        if not phone:
            raise InvalidDataException("Телефон не может быть пустым")

        self.id = id
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"{self.name} (тел: {self.phone})"


class Employee(Person):
    """Сотрудник транспортной компании"""

    def __init__(self, id: int, name: str, phone: str, position: str, salary: float):
        super().__init__(id, name, phone)

        if not position:
            raise InvalidDataException("Должность не может быть пустой")
        if salary <= 0:
            raise InvalidDataException("Зарплата должна быть положительной")

        self.position = position
        self.salary = salary

    def __str__(self):
        return f"{self.name} - {self.position} (з/п: {self.salary} руб.)"


class Passenger(Person):
    """Пассажир с учетом льготной категории"""

    def __init__(self, id: int, name: str, phone: str, email: str = "", discount: float = 0.0,
                 category: str = "взрослый"):
        super().__init__(id, name, phone)

        self.email = email
        if discount < 0 or discount > 100:
            raise InvalidDataException("Скидка должна быть от 0 до 100")
        self.discount = discount
        self.category = category

    def __str__(self):
        discount_str = ""
        if self.discount == 100:
            discount_str = " (бесплатно)"
        elif self.discount > 0:
            discount_str = f" (скидка {self.discount}%)"

        return f"{self.name} - {self.category}{discount_str}"


class Transport:
    """Базовый класс для транспорта"""
    STATUS_ACTIVE = "Активен"
    STATUS_REPAIR = "В ремонте"
    STATUS_RETIRED = "Списан"

    def __init__(self, id: int, brand: str, model: str, year: int, capacity: int):
        if not brand:
            raise InvalidDataException("Марка не может быть пустой")
        if not model:
            raise InvalidDataException("Модель не может быть пустой")
        if year < 1900 or year > datetime.now().year + 1:
            raise InvalidDataException("Некорректный год выпуска")
        if capacity <= 0:
            raise InvalidDataException("Вместимость должна быть положительной")

        self.id = id
        self.brand = brand
        self.model = model
        self.year = year
        self.capacity = capacity
        self.status = self.STATUS_ACTIVE

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year} г.), {self.capacity} мест"


class Bus(Transport):
    """Автобус (включая электробусы)"""

    def __init__(self, id: int, brand: str, model: str, year: int, capacity: int, route_number: str = ""):
        super().__init__(id, brand, model, year, capacity)
        self.route_number = route_number

    def __str__(self):
        base = super().__str__()
        bus_type = "Электробус" if "Электробус" in self.model else "Автобус"
        return f"{bus_type} {base}, маршрут {self.route_number if self.route_number else 'не назначен'}"


class Tram(Transport):
    """Трамвай"""

    def __init__(self, id: int, brand: str, model: str, year: int, capacity: int, line_number: str = ""):
        super().__init__(id, brand, model, year, capacity)
        self.line_number = line_number

    def __str__(self):
        base = super().__str__()
        return f"Трамвай {base}, маршрут {self.line_number if self.line_number else 'не назначен'}"


class Trolleybus(Transport):
    """Троллейбус"""

    def __init__(self, id: int, brand: str, model: str, year: int, capacity: int, route_number: str = ""):
        super().__init__(id, brand, model, year, capacity)
        self.route_number = route_number

    def __str__(self):
        base = super().__str__()
        return f"Троллейбус {base}, маршрут {self.route_number if self.route_number else 'не назначен'}"


class Route:
    """Маршрут"""

    def __init__(self, id: int, number: str, start_point: str, end_point: str, distance: float):
        if not number:
            raise InvalidDataException("Номер маршрута не может быть пустым")
        if not start_point or not end_point:
            raise InvalidDataException("Начальная и конечная точки должны быть указаны")
        if distance <= 0:
            raise InvalidDataException("Расстояние должно быть положительным")

        self.id = id
        self.number = number
        self.start_point = start_point
        self.end_point = end_point
        self.distance = distance

    def __str__(self):
        return f"Маршрут {self.number}: {self.start_point} - {self.end_point} ({self.distance} км)"


class Trip:
    """Поездка/рейс"""

    def __init__(self, id: int, route: Route, transport: Transport, driver: Employee,
                 departure_time: datetime, arrival_time: datetime, fare: float):
        if not route or not transport or not driver:
            raise InvalidDataException("Маршрут, транспорт и водитель должны быть указаны")
        if departure_time >= arrival_time:
            raise InvalidDataException("Время отправления должно быть раньше времени прибытия")
        if fare < 0:
            raise InvalidDataException("Стоимость проезда не может быть отрицательной")

        self.id = id
        self.route = route
        self.transport = transport
        self.driver = driver
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.fare = fare
        self.passengers: List[Passenger] = []

    def add_passenger(self, passenger: Passenger):
        """Добавление пассажира в рейс с учетом льгот"""
        if len(self.passengers) >= self.transport.capacity:
            raise TransportException("Транспорт заполнен, нельзя добавить больше пассажиров")
        self.passengers.append(passenger)

    def remove_passenger(self, passenger_id: int):
        """Удаление пассажира из рейса"""
        self.passengers = [p for p in self.passengers if p.id != passenger_id]

    def get_passenger_count(self) -> int:
        """Количество пассажиров"""
        return len(self.passengers)

    def get_free_seats(self) -> int:
        """Свободные места"""
        return self.transport.capacity - len(self.passengers)

    def get_total_revenue(self) -> float:
        """Общая выручка за рейс с учетом льгот"""
        total = 0
        for passenger in self.passengers:
            if passenger.discount == 100:
                ticket_price = 0  # Бесплатно
            else:
                ticket_price = self.fare * (1 - passenger.discount / 100)
            total += ticket_price
        return total

    def get_passengers_by_category(self, category: str) -> List[Passenger]:
        """Получение пассажиров по категории"""
        return [p for p in self.passengers if p.category == category]

    def __str__(self):
        """Красивое отображение информации о рейсе"""
        # Форматируем время
        dep_time = self.departure_time.strftime('%d.%m.%Y %H:%M')
        arr_time = self.arrival_time.strftime('%H:%M')

        # Рассчитываем продолжительность
        duration = self.arrival_time - self.departure_time
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        duration_str = f"{hours}ч {minutes}мин" if hours > 0 else f"{minutes}мин"

        # Информация о транспорте
        transport_type = "Электробус" if "Электробус" in self.transport.model else self.transport.__class__.__name__
        transport_info = f"{transport_type} {self.transport.brand} {self.transport.model}"

        # Информация о маршруте
        route_info = f"{self.route.start_point} → {self.route.end_point}"

        # Статистика по пассажирам с разбивкой по категориям
        passengers_count = self.get_passenger_count()
        free_seats = self.get_free_seats()

        # Подсчет по категориям
        categories = {}
        for p in self.passengers:
            categories[p.category] = categories.get(p.category, 0) + 1

        categories_str = ", ".join([f"{cat}: {count}" for cat, count in categories.items()])

        # Выручка с учетом льгот
        revenue = self.get_total_revenue()

        return (f"\n🚍 Рейс #{self.id} | Маршрут {self.route.number}\n"
                f"   {route_info} ({self.route.distance} км)\n"
                f"   ⏰ Отправление: {dep_time} | Прибытие: {arr_time} (в пути {duration_str})\n"
                f"   🚌 Транспорт: {transport_info} (вместимость: {self.transport.capacity} мест)\n"
                f"   👨‍✈️ Водитель: {self.driver.name}\n"
                f"   💰 Стоимость проезда: {self.fare} руб.\n"
                f"   👥 Пассажиры: {passengers_count}/{self.transport.capacity} ({free_seats} свободно)\n"
                f"   {f'   📊 Категории: {categories_str}' if categories_str else ''}\n"
                f"   💵 Выручка за рейс: {revenue:.2f} руб.")