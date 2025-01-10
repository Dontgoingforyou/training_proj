from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE, verbose_name='Автор')
    count = models.PositiveIntegerField(default=0, verbose_name='Количество книг на складе')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'{self.title} - {self.author}, на складе {self.count} книг'
