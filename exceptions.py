
class TransportException(Exception):
    """Базовое исключение для транспортной системы"""
    pass


class InvalidDataException(TransportException):
    """Исключение при неверных данных"""
    pass


class NotFoundException(TransportException):
    """Исключение когда объект не найден"""
    pass


class FileOperationException(TransportException):
    """Исключение при работе с файлами"""
    pass