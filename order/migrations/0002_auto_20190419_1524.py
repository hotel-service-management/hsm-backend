# Generated by Django 2.2 on 2019-04-19 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
            ],
            options={
                'db_table': 'food',
            },
        ),
        migrations.RenameField(
            model_name='service',
            old_name='service_type',
            new_name='type',
        ),
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
        migrations.AlterModelTable(
            name='service',
            table='service',
        ),
        migrations.AlterModelTable(
            name='servicelist',
            table='service_list',
        ),
        migrations.CreateModel(
            name='FoodList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.ManyToManyField(to='order.Food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
            ],
            options={
                'db_table': 'food_list',
            },
        ),
    ]
