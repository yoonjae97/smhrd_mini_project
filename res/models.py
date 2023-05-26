# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Member(models.Model):
    mem_seq = models.FloatField(primary_key=True)
    mem_id = models.CharField(max_length=200)
    mem_password = models.CharField(max_length=200)
    mem_google_id = models.CharField(max_length=200, blank=True, null=True)
    mem_naver_id = models.CharField(max_length=200, blank=True, null=True)
    mem_type = models.CharField(max_length=200)
    mem_age = models.FloatField()
    mem_name = models.CharField(max_length=200)
    mem_wdate = models.DateField()
    mem_update = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'


class Restaurant(models.Model):
    res_seq = models.FloatField(primary_key=True)
    mem_seq = models.ForeignKey(Member, models.DO_NOTHING, db_column='mem_seq')
    res_name = models.CharField(max_length=200)
    res_locate = models.CharField(max_length=200)
    res_phone = models.CharField(max_length=200)
    res_content = models.CharField(max_length=200, blank=True, null=True)
    res_score = models.FloatField(blank=True, null=True)
    res_hit = models.FloatField()
    res_wdate = models.DateField()
    res_update = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurant'
