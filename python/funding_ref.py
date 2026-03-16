import csv

class RecordNotFound(Exception):
    """Исключение, выбрасываемое, когда запись не найдена."""
    pass

class FundingRaised:
    # Кэшируем данные CSV, чтобы не читать файл каждый раз
    _cached_data = None

    @classmethod
    def _load_data(cls):
        """Загружает данные из CSV один раз и кэширует их."""
        if cls._cached_data is None:
            with open("../startup_funding.csv", "rt", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                next(reader)  # Пропускаем заголовок
                cls._cached_data = [row for row in reader]
        return cls._cached_data

    @staticmethod
    def _map_row(row):
        """Преобразует строку CSV в словарь с нужными ключами."""
        keys = [
            'permalink', 'company_name', 'number_employees', 'category',
            'city', 'state', 'funded_date', 'raised_amount',
            'raised_currency', 'round'
        ]
        return dict(zip(keys, row))

    @classmethod
    def where(cls, options=None):
        """
        Возвращает список всех записей, соответствующих условиям.
        Поддерживает фильтрацию по: company_name, city, state, round.
        """
        if options is None:
            options = {}

        data = cls._load_data()
        filtered_data = data

        # Фильтрация по каждому полю
        filters = {
            'company_name': 1,
            'city': 4,
            'state': 5,
            'round': 9
        }

        for key, index in filters.items():
            if key in options:
                filtered_data = [row for row in filtered_data if row[index] == options[key]]

        return [cls._map_row(row) for row in filtered_data]

    @classmethod
    def find_by(cls, options):
        """
        Возвращает первую запись, соответствующую условиям.
        Выбрасывает RecordNotFound, если ничего не найдено.
        """
        result = cls.where(options)
        if not result:
            raise RecordNotFound(f"Запись с параметрами {options} не найдена.")
        return result[0]