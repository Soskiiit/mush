from huey import SqliteHuey
from mush.settings import BASE_DIR

# BASE_DIR = 'C:/Users/Oleg/PycharmProjects/mush/mush/'

db_dir = f"{BASE_DIR}/db2.sqlite3"

print(f"using database directory: {db_dir}")

huey = SqliteHuey(filename=db_dir)


@huey.task()
def add(a, b):
    return a + b


# В офф. доках предлагается в консоли сделать следующее
# >>> from photogrammetry.queue_test_huey import add
# >>> r = add(1, 2)
# >>> r()
# И получить вывод 3

# Можно запускать из shell, это также вынесено в файлик huey_test_runner,
# ниоткуда оно не работает
