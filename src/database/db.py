import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from HW_Web_11.src.conf.config import config  # підключення до postgres


class DatabaseSessionManager:
    """Клас для управління сесіями бази даних"""

    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)  # наше посилання на postgres
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        """ Асинхронний менеджер контексту для взаємодії з об'єктами сесій бази даних. Для підключення"""
        if self._session_maker is None:
            raise Exception("Session is not created")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanamger = DatabaseSessionManager(config.DB_URL)  # Створення екземпляра менеджера сесій

"""Отже, коли вам потрібно взаємодіяти з базою даних у ваших асинхронних функціях, ви можете використовувати get_db() 
для отримання асинхронної сесії бази даних. Це дозволяє вам виконувати операції читання або запису в базу даних, 
забезпечуючи правильне відкриття та закриття сесії."""


async def get_db():  # Асинхронна функція для отримання сесії бази даних
    async with sessionmanamger.session() as session:
        yield session
