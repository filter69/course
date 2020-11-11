# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    titles = models.CharField(max_length=20, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    parnt_elevel = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_category'


class Title(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    publish_time = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    cate = models.ForeignKey(TCategory, models.DO_NOTHING, blank=True, null=True)
    class Meta:
        db_table = 'title'
