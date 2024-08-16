from django.db import models


class Region(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subregions',
                               db_column='parent_slug')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'regions'


class Port(models.Model):
    code = models.CharField(max_length=5, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, to_field='slug', on_delete=models.CASCADE, related_name='ports',
                               db_column='parent_slug')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ports'


class Price(models.Model):
    origin = models.ForeignKey(Port, related_name='origin_prices', on_delete=models.CASCADE, to_field='code',
                               db_column='orig_code')
    destination = models.ForeignKey(Port, related_name='destination_prices', on_delete=models.CASCADE, to_field='code',
                                    db_column='dest_code')
    day = models.DateField()
    price = models.IntegerField()

    class Meta:
        db_table = 'prices'
        unique_together = ('origin', 'destination', 'day')
