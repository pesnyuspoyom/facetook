from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# это наша первая таблица "News"
class News(models.Model):                                       # unique СНИЗУ, добавляет уникальность, статьи с таким же именем не будет
    title = models.CharField('Название статьи', max_length=200, unique=True) # класс CharField позволяет создать поле, в котором мы можем написать текст с ограничением 100 символов
    text = models.TextField('Основной текст статьи') # класс TextField позволяет создать поле, в котором мы можем написать текст ограничением 
    date = models.DateTimeField('Дата', default=timezone.now) # класс DateTimeField время создания статьи
    avtor = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)  # это поле привязанное к определенному пользователю + управлние удалением этого пользователя
    

    # sizes = (           #благодаря этому классу мы можем выбирать значения которые сами задали ЭТО НАЧАЛО
    #     ('S', 'Small'),
    #     ('M', 'Medium'),
    #     ('L', 'Large'),
    #     ('XL', 'X large'),
    # )

    # shop_sizes = models.CharField(max_length=2, choices=sizes, default='S') #ЭТО КОНЕЦ

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Tasks(models.Model):
    title = models.CharField('Заголовок',max_length = 50)
    task = models.TextField("Задание")
    otvet = models.IntegerField("Ответ", default=1)
    date = models.DateTimeField('Дата', default=timezone.now)
    hardness = models.FloatField("Уровень сложности", default=1.0)

