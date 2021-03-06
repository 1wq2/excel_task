# Generated by Django 2.1.5 on 2019-02-04 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceAccounts',
            fields=[
                ('Id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('Number', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('Id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('ClassNumber', models.IntegerField(unique=True)),
                ('Description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('Id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('Name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('Id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('IncomingBalanceAssets', models.FloatField()),
                ('IncomingBalanceLiabilities', models.FloatField()),
                ('CirculationDebit', models.FloatField()),
                ('CirculationCredit', models.FloatField()),
                ('OutgoingBalanceAssets', models.FloatField()),
                ('OutgoingBalanceLiabilities', models.FloatField()),
                ('BalanceAccountsId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ExcelManager.BalanceAccounts')),
                ('FileId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ExcelManager.Files')),
            ],
        ),
        migrations.AddField(
            model_name='balanceaccounts',
            name='ClassId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ExcelManager.Classes'),
        ),
    ]
