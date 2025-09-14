from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DeliveryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Delivery_type', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('Delivery_type',),
            },
        ),
        migrations.CreateModel(
            name='HUType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HU_type', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('HU_type',),
            },
        ),
        migrations.CreateModel(
            name='PreAdvice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('login', models.CharField(db_index=True, max_length=150)),
                ('driver_name', models.CharField(blank=True, max_length=255, null=True)),
                ('driver_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('driver_lang', models.CharField(blank=True, max_length=10, null=True)),
                ('vehicle_number', models.CharField(blank=True, max_length=50, null=True)),
                ('trailer_number', models.CharField(blank=True, max_length=50, null=True)),
                ('order_number', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='preadvices', to='dbcore.company')),
                ('delivery_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='preadvices', to='dbcore.deliverytype')),
            ],
            options={
                'ordering': ['-date', '-id'],
            },
        ),
        migrations.CreateModel(
            name='PreAdviceHU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('hu_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dbcore.hutype')),
                ('preadvice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hu_rows', to='dbcore.preadvice')),
            ],
            options={
                'unique_together': {('preadvice', 'hu_type')},
            },
        ),
    ]
