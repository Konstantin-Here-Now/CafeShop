from django.db import models
from django.urls import reverse


class Coffee(models.Model):
    name = models.CharField(max_length=120, default='Кофе', verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(default=10, verbose_name='Цена')
    date_created = models.DateField(auto_now_add=True, verbose_name='Дата создания записи')
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления записи')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Фото')
    exist = models.BooleanField(default=True, null=False, verbose_name='В каталоге?')

    def get_absolute_url(self):
        return reverse('coffee_info', kwargs={'coffee_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кофе'
        verbose_name_plural = 'Кофе'
        ordering = ['name', 'price']


class Cheque(models.Model):
    number = models.IntegerField(verbose_name='Номер заказа')
    total_price = models.FloatField(verbose_name='Общая сумма чека')
    date_printed = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    desc = models.TextField(verbose_name='Заказ')

    def __str__(self):
        return f'{self.date_printed} {self.total_price}'

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        ordering = ['date_printed', 'total_price']
