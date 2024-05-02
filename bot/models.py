from django.db import models


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(null=True)
    username = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.username}, {self.telegram_id}"

    class Meta:
        db_table = "userprofile"


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="Назва послуги", null=True)
    question = models.TextField(verbose_name="Опис", null=True)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.CharField(max_length=256, verbose_name="Час", null=True)
    location = models.CharField(max_length=256, verbose_name="Локація", null=True)
    contact = models.CharField(max_length=256, verbose_name="Контакти", null=True)

    def __str__(self):
        return f"{self.user}, {self.product}"


class Preference(models.Model):
    preference = models.TextField(verbose_name="Переваги", null=True)

    def __str__(self):
        return f"{self.preference}"

class Question(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.TextField(verbose_name="Питання Клієнта", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.question}"


class Contacts(models.Model):
    text = models.CharField(max_length=256, verbose_name="Текст", null=True)

    def __str__(self):
        return f"Text: {self.text}"

    class Meta:
        db_table = "contacts"


class ContactsLink(models.Model):
    contact = models.ForeignKey(Contacts, related_name='contact', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name="Текст", blank=True, null=True)
    links = models.CharField(max_length=256, verbose_name="Посилання")