import time

from django.db import transaction
from .models import Task

def fetch_task(worker_id: int) -> Task | None:
    """ Извлекает задачу со статусом 'pending', блокирует её и назначает воркеру """

    with transaction.atomic():
        task = (Task.objects.select_for_update(skip_locked=True).filter(status='pending').first())
        if task:
            task.status = 'processing'
            task.worked_id = worker_id
            task.save()
        return task


def process_task(task: Task):
    """ Выполняет обработку задачи и завершает её """

    try:
        print(f'Воркер {task.worked_id} обрабатывает задачу {task.id}: {task.task_name}')
        time.sleep(2)
        task.status = 'completed'
        task.save()
        print(f'Задача {task.id} выполнена воркером {task.worked_id}')
    except Exception as e:
        print(f'Ошибка при обработке задачи {task.id}: {e}')