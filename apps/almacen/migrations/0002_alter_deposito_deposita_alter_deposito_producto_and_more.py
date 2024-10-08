# Generated by Django 5.1 on 2024-08-21 00:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0001_initial'),
        ('producto', '0004_alter_producto_imagen_qr'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposito',
            name='deposita',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiendeposita', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='deposito',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depoproducto', to='producto.producto'),
        ),
        migrations.AlterField(
            model_name='retiro',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retiroproducto', to='producto.producto'),
        ),
        migrations.AlterField(
            model_name='retiro',
            name='retira',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quienretiro', to=settings.AUTH_USER_MODEL),
        ),
    ]
