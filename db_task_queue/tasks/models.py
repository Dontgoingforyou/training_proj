from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]

    task_name = models.CharField(max_length=255, verbose_name='Имя задачи')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    worked_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at =models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.task_name