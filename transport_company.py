from typing import List, Optional, Dict
from datetime import datetime
from models import Transport, Bus, Tram, Employee, Passenger, Route, Trip
from exceptions import NotFoundException, InvalidDataException
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom


class TransportCompany:
    """Класс транспортной компании"""

    def __init__(self, name: str):
        self.name = name
        self.transports: List[Transport] = []
        self.employees: List[Employee] = []
        self.passengers: List[Passenger] = []
        self.routes: List[Route] = []
        self.trips: List[Trip] = []

        self._next_id = {
            'transport': 1,
            'employee': 1,
            'passenger': 1,
            'route': 1,
            'trip': 1
        }

    def _get_next_id(self, entity_type: str) -> int:
        """Получение следующего ID для сущности"""
        current = self._next_id.get(entity_type, 1)
        self._next_id[entity_type] = current + 1
        return current

    # Транспорт
    def add_transport(self, transport: Transport):
        """Добавление транспорта"""
        if transport.id == 0:
            transport.id = self._get_next_id('transport')
        self.transports.append(transport)

    def get_transport(self, transport_id: int) -> Optional[Transport]:
        """Получение транспорта по ID"""
        for t in self.transports:
            if t.id == transport_id:
                return t
        return None

    def remove_transport(self, transport_id: int):
        """Удаление транспорта"""
        transport = self.get_transport(transport_id)
        if not transport:
            raise NotFoundException(f"Транспорт с ID {transport_id} не найден")
        self.transports.remove(transport)

    def get_active_transports(self) -> List[Transport]:
        """Получение активного транспорта"""
        return [t for t in self.transports if t.status == Transport.STATUS_ACTIVE]

    # Сотрудники
    def add_employee(self, employee: Employee):
        """Добавление сотрудника"""
        if employee.id == 0:
            employee.id = self._get_next_id('employee')
        self.employees.append(employee)

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        """Получение сотрудника по ID"""
        for e in self.employees:
            if e.id == employee_id:
                return e
        return None

    def get_drivers(self) -> List[Employee]:
        """Получение водителей"""
        return [e for e in self.employees if 'водитель' in e.position.lower()]

    # Пассажиры
    def add_passenger(self, passenger: Passenger):
        """Добавление пассажира"""
        if passenger.id == 0:
            passenger.id = self._get_next_id('passenger')
        self.passengers.append(passenger)

    def get_passenger(self, passenger_id: int) -> Optional[Passenger]:
        """Получение пассажира по ID"""
        for p in self.passengers:
            if p.id == passenger_id:
                return p
        return None

    # Маршруты
    def add_route(self, route: Route):
        """Добавление маршрута"""
        if route.id == 0:
            route.id = self._get_next_id('route')
        self.routes.append(route)

    def get_route(self, route_id: int) -> Optional[Route]:
        """Получение маршрута по ID"""
        for r in self.routes:
            if r.id == route_id:
                return r
        return None

    def get_route_by_number(self, number: str) -> Optional[Route]:
        """Получение маршрута по номеру"""
        for r in self.routes:
            if r.number == number:
                return r
        return None

    # Рейсы
    def add_trip(self, trip: Trip):
        """Добавление рейса"""
        if trip.id == 0:
            trip.id = self._get_next_id('trip')
        self.trips.append(trip)

    def get_trips_by_date(self, date: datetime.date) -> List[Trip]:
        """Получение рейсов по дате"""
        return [t for t in self.trips if t.departure_time.date() == date]

    def get_trips_by_route(self, route_id: int) -> List[Trip]:
        """Получение рейсов по маршруту"""
        return [t for t in self.trips if t.route.id == route_id]

    # Сохранение/загрузка данных
    def save_to_json(self, filename: str):
        """Сохранение данных в JSON"""
        data = {
            'company_name': self.name,
            'transports': [
                {
                    'id': t.id,
                    'type': 'bus' if isinstance(t, Bus) else 'tram',
                    'brand': t.brand,
                    'model': t.model,
                    'year': t.year,
                    'capacity': t.capacity,
                    'status': t.status,
                    'route_number': getattr(t, 'route_number', ''),
                    'line_number': getattr(t, 'line_number', '')
                } for t in self.transports
            ],
            'employees': [
                {
                    'id': e.id,
                    'name': e.name,
                    'phone': e.phone,
                    'position': e.position,
                    'salary': e.salary
                } for e in self.employees
            ],
            'passengers': [
                {
                    'id': p.id,
                    'name': p.name,
                    'phone': p.phone,
                    'email': p.email,
                    'discount': p.discount
                } for p in self.passengers
            ],
            'routes': [
                {
                    'id': r.id,
                    'number': r.number,
                    'start_point': r.start_point,
                    'end_point': r.end_point,
                    'distance': r.distance
                } for r in self.routes
            ],
            'trips': [
                {
                    'id': t.id,
                    'route_id': t.route.id,
                    'transport_id': t.transport.id,
                    'driver_id': t.driver.id,
                    'departure_time': t.departure_time.isoformat(),
                    'arrival_time': t.arrival_time.isoformat(),
                    'fare': t.fare,
                    'passengers': [p.id for p in t.passengers]
                } for t in self.trips
            ],
            'next_id': self._next_id
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise FileOperationException(f"Ошибка сохранения в JSON: {e}")

    def load_from_json(self, filename: str):
        """Загрузка данных из JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise FileOperationException(f"Ошибка загрузки из JSON: {e}")

        self.name = data['company_name']

        # Очистка текущих данных
        self.transports.clear()
        self.employees.clear()
        self.passengers.clear()
        self.routes.clear()
        self.trips.clear()

        # Загрузка транспорта
        transport_map = {}
        for t_data in data['transports']:
            if t_data['type'] == 'bus':
                transport = Bus(
                    t_data['id'], t_data['brand'], t_data['model'],
                    t_data['year'], t_data['capacity'], t_data['route_number']
                )
            else:
                transport = Tram(
                    t_data['id'], t_data['brand'], t_data['model'],
                    t_data['year'], t_data['capacity'], t_data['line_number']
                )
            transport.status = t_data['status']
            self.transports.append(transport)
            transport_map[t_data['id']] = transport

        # Загрузка сотрудников
        employee_map = {}
        for e_data in data['employees']:
            employee = Employee(
                e_data['id'], e_data['name'], e_data['phone'],
                e_data['position'], e_data['salary']
            )
            self.employees.append(employee)
            employee_map[e_data['id']] = employee

        # Загрузка пассажиров
        passenger_map = {}
        for p_data in data['passengers']:
            passenger = Passenger(
                p_data['id'], p_data['name'], p_data['phone'],
                p_data['email'], p_data['discount']
            )
            self.passengers.append(passenger)
            passenger_map[p_data['id']] = passenger

        # Загрузка маршрутов
        route_map = {}
        for r_data in data['routes']:
            route = Route(
                r_data['id'], r_data['number'],
                r_data['start_point'], r_data['end_point'],
                r_data['distance']
            )
            self.routes.append(route)
            route_map[r_data['id']] = route

        # Загрузка рейсов
        for t_data in data['trips']:
            trip = Trip(
                t_data['id'],
                route_map[t_data['route_id']],
                transport_map[t_data['transport_id']],
                employee_map[t_data['driver_id']],
                datetime.fromisoformat(t_data['departure_time']),
                datetime.fromisoformat(t_data['arrival_time']),
                t_data['fare']
            )
            # Добавление пассажиров
            for p_id in t_data['passengers']:
                if p_id in passenger_map:
                    trip.add_passenger(passenger_map[p_id])
            self.trips.append(trip)

        self._next_id = data['next_id']

    def save_to_xml(self, filename: str):
        """Сохранение данных в XML"""
        root = ET.Element("TransportCompany")
        root.set("name", self.name)

        # Транспорт
        transports_elem = ET.SubElement(root, "Transports")
        for t in self.transports:
            t_elem = ET.SubElement(transports_elem, "Transport")
            t_elem.set("id", str(t.id))
            t_elem.set("type", "bus" if isinstance(t, Bus) else "tram")
            ET.SubElement(t_elem, "Brand").text = t.brand
            ET.SubElement(t_elem, "Model").text = t.model
            ET.SubElement(t_elem, "Year").text = str(t.year)
            ET.SubElement(t_elem, "Capacity").text = str(t.capacity)
            ET.SubElement(t_elem, "Status").text = t.status
            if isinstance(t, Bus):
                ET.SubElement(t_elem, "RouteNumber").text = t.route_number
            elif isinstance(t, Tram):
                ET.SubElement(t_elem, "LineNumber").text = t.line_number

        # Сотрудники
        employees_elem = ET.SubElement(root, "Employees")
        for e in self.employees:
            e_elem = ET.SubElement(employees_elem, "Employee")
            e_elem.set("id", str(e.id))
            ET.SubElement(e_elem, "Name").text = e.name
            ET.SubElement(e_elem, "Phone").text = e.phone
            ET.SubElement(e_elem, "Position").text = e.position
            ET.SubElement(e_elem, "Salary").text = str(e.salary)

        # Пассажиры
        passengers_elem = ET.SubElement(root, "Passengers")
        for p in self.passengers:
            p_elem = ET.SubElement(passengers_elem, "Passenger")
            p_elem.set("id", str(p.id))
            ET.SubElement(p_elem, "Name").text = p.name
            ET.SubElement(p_elem, "Phone").text = p.phone
            ET.SubElement(p_elem, "Email").text = p.email
            ET.SubElement(p_elem, "Discount").text = str(p.discount)

        # Маршруты
        routes_elem = ET.SubElement(root, "Routes")
        for r in self.routes:
            r_elem = ET.SubElement(routes_elem, "Route")
            r_elem.set("id", str(r.id))
            ET.SubElement(r_elem, "Number").text = r.number
            ET.SubElement(r_elem, "StartPoint").text = r.start_point
            ET.SubElement(r_elem, "EndPoint").text = r.end_point
            ET.SubElement(r_elem, "Distance").text = str(r.distance)

        # Рейсы
        trips_elem = ET.SubElement(root, "Trips")
        for t in self.trips:
            t_elem = ET.SubElement(trips_elem, "Trip")
            t_elem.set("id", str(t.id))
            ET.SubElement(t_elem, "RouteId").text = str(t.route.id)
            ET.SubElement(t_elem, "TransportId").text = str(t.transport.id)
            ET.SubElement(t_elem, "DriverId").text = str(t.driver.id)
            ET.SubElement(t_elem, "DepartureTime").text = t.departure_time.isoformat()
            ET.SubElement(t_elem, "ArrivalTime").text = t.arrival_time.isoformat()
            ET.SubElement(t_elem, "Fare").text = str(t.fare)

            passengers_refs = ET.SubElement(t_elem, "PassengerIds")
            for p in t.passengers:
                ET.SubElement(passengers_refs, "PassengerId").text = str(p.id)

        # Next ID
        next_id_elem = ET.SubElement(root, "NextId")
        for key, value in self._next_id.items():
            ET.SubElement(next_id_elem, key).text = str(value)

        # Запись в файл с форматированием
        try:
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(xml_str)
        except Exception as e:
            raise FileOperationException(f"Ошибка сохранения в XML: {e}")

    def display_info(self):
        """Вывод информации о компании"""
        print(f"\nТранспортная компания: {self.name}")
        print(f"Транспортных средств: {len(self.transports)}")
        print(f"Сотрудников: {len(self.employees)}")
        print(f"Пассажиров: {len(self.passengers)}")
        print(f"Маршрутов: {len(self.routes)}")
        print(f"Рейсов: {len(self.trips)}")