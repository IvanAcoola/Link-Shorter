from django.db import models


class Profiles(models.Model):
    nickname = models.CharField(max_length=50)
    sub_till = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Links(models.Model):
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=50)
    redirect = models.CharField(max_length=100, default='https://www.google.com/')
    screamer = models.BooleanField(default=False)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'


class Passes(models.Model):
    link = models.CharField(max_length=30)
    owner_link = models.CharField(max_length=50)
    ip = models.CharField(max_length=30)
    region = models.CharField(max_length=80)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Переход'
        verbose_name_plural = 'Переходы'
