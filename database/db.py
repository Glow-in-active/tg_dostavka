import sqlite3

class DatabaseConnection:
    '''
    Класс для управления соединением с бд, гарантирует, что соединение с бд будет создано только один раз
    и будет использоваться повторно

    Attributes:
        _instance (DatabaseConnection): Единственный экземпляр класса
        _conn (sqlite3.Connection): Объект соединения с бд
        _cursor (sqlite3.Cursor): Объект курсора для выполнения SQL-запросов
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        '''
        Создает новый экземпляр класса, если он еще не был создан

        Returns:
            DatabaseConnection: Единственный экземпляр класса
        '''
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._conn = sqlite3.connect('../../database/users', check_same_thread=False)
            cls._instance._cursor = cls._instance._conn.cursor()
        return cls._instance

    @property
    def conn(self):
        '''
        Returns:
            sqlite3.Connection: Объект соединения с бд
        '''
        return self._conn

    @property
    def cursor(self):
        '''
        Returns:
            sqlite3.Cursor: Объект курсора для выполнения SQL-запросов
        '''
        return self._cursor

def get_db_connection():
    '''
    Returns:
        sqlite3.Connection: Объект соединения с бд
    '''
    return DatabaseConnection().conn

def get_db_cursor():
    '''
    Returns:
        sqlite3.Cursor: Объект курсора для выполнения SQL-запросов
    '''
    return DatabaseConnection().cursor

