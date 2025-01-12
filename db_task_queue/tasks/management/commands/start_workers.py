from django.core.management.base import BaseCommand
from tasks.tasks import main

class Command(BaseCommand):
    help = 'Запуск воркеров для обработки задач'

    def handle(self, *args, **kwargs):
        main()