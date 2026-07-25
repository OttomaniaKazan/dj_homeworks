from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    # id, name, price, image, release_date, lte_exists и slug. Поле id — должно быть основным ключом модели.

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField(blank=True, null=True)
    lte_exists = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name