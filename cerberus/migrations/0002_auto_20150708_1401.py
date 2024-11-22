from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cerberus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lockout',
            name='ip_address',
            field=models.GenericIPAddressField(default=None, null=True, verbose_name='IP address', blank=True),
        ),
    ]
