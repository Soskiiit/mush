from litequeue import LiteQueue
from mush.mush.settings import BASE_DIR

# BASE_DIR = 'C:/Users/Oleg/PycharmProjects/mush/mush/'

db_dir = f'{BASE_DIR}/db2.sqlite3'
# db_dir=':memory:'

print(f'using database directory: {db_dir}')
q = LiteQueue(db_dir)

q.put('hello')
print(q)

# Если запускать этот файл из проекта, выводится
# sqlite3.OperationalError: no such column: MessageStatus.READY
# Если запускать извне - всё работает, выводит в духе
# LiteQueue(Connection=<sqlite3.Connection object at 0x000001DC4269D4E0>,
# items=[Message(data='hello',...
# В db_dir по можно ставить и ':memory:', но это также безрезультатно
