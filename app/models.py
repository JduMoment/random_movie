from dependencies import ENV

class Movie:

    def __init__(self, title, d_release, rate):
        self.title = title
        self.d_release = d_release
        self.rate = rate

    def __new__(cls, *args, **kwargs):
        """Запрещаем создавать класс стандартным способом (прим. Film())"""
        if cls is Movie:
            raise TypeError("Используйте Film.create() вместо Film()")
        return super().__new__(cls)

    @classmethod
    def create(cls, title, d_release, rate):
        """
        Единственный способ создать экземпляр.
        Сделано, чтобы валидировать можно было уже на этапе создания.
        """
        return cls(title, d_release, rate)

class TMDB:

    def get_movies(self, **kwargs):
        url = f"{ENV.TMDB_BASE_URL}"
        pass

    def get_request_dict(self, **kwargs):
        pass
