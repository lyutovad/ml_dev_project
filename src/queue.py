from redis import Redis
from rq import Queue

# Подключение к Redis серверу
redis_conn = Redis()

# Создание объекта очереди
queue = Queue(connection=redis_conn)


# Функция, которая будет выполняться в фоновом режиме
def my_task(x, y):
    return x + y


# Добавление задачи в очередь
job = queue.enqueue(my_task, args=(3, 4))

# Получение результатов выполнения задачи
result = job.result
print(f"Результат выполнения задачи: {result}")


from rq import Worker, Queue, Connection
from redis import Redis

# Подключение к Redis серверу
redis_conn = Redis()

# Создание объекта очереди
queue = Queue(connection=redis_conn)

# Создание объекта рабочего процесса
worker = Worker([queue], connection=redis_conn)

# Запуск рабочего процесса для обработки задач
if __name__ == "__main__":
    worker.work()
