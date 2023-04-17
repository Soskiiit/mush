from queue_test_huey import add
r = add(1, 2)
# Запускаем задачу через r(), ждём её окончания (blocking=True), а если она не успеет за 3 секунды - грустим
r(blocking=True, timeout=3)
# Получаем timed out waiting for result - за 3 секунды мы не смогли сложить 1 и 2 );

# run:
# python .\mush\photogrammetry\huey_test_runner.py