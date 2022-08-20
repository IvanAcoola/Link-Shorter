from django.db import models


class Profiles(models.Model):
    SUBS = (
        ("pro", "pro"),
        ("vip", "vip"),
        ("max", "max"),
    )
    nickname = models.CharField(max_length=50)
    sub_type = models.CharField(choices=SUBS, max_length=10, default='pro')
    sub_till = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Подписки'


class Links(models.Model):
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=50)
    redirect = models.CharField(max_length=100, default='https://www.google.com/')
    type = models.CharField(max_length=12, default='redirect')
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
    fish = models.CharField(max_length=100, default='-')
    agent = models.CharField(max_length=150, default='not_loged')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Переход'
        verbose_name_plural = 'Переходы'
