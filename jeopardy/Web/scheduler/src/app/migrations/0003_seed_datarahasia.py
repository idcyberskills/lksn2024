# Generated by Django 4.0.5 on 2023-04-01 14:14

from django.db import migrations

def forwards_func(apps, schema_editor):
    DATA = [
        ('diary', 'Semoga kalian sukses di LKSN 2024.'),
        ('config', 'LKSN{\w+} adalah format flag'),
        ('s3crEt', 'LKSN{sus4H_c4R1_iD3eE3}'),
        ('not flag', 'Sudah dibilang ini bukan flag'),
        ('bukan flag', 'Sudah dibilang ini bukan flag'),
        ('init', 'Sudah dibilang ini bukan flag'),
        ('oh flag', 'Sudah dibilang ini bukan flag'),
    ]
    DataRahasia = apps.get_model("app", "DataRahasia")
    db_alias = schema_editor.connection.alias
    DataRahasia.objects.using(db_alias).bulk_create([DataRahasia(title=e[0], data=e[1]) for e in DATA])

def reverse_func(apps, schema_editor):
    DataRahasia = apps.get_model("app", "DataRahasia")
    db_alias = schema_editor.connection.alias
    DataRahasia.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_datarahasia'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]