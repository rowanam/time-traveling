# Generated by Django 3.2.23 on 2023-12-05 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_auto_20231203_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customtrip',
            name='locations',
        ),
        migrations.CreateModel(
            name='CustomLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lat', models.DecimalField(decimal_places=2, max_digits=8)),
                ('long', models.DecimalField(decimal_places=2, max_digits=8)),
                ('order', models.IntegerField()),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='trips.customtrip')),
            ],
        ),
    ]
