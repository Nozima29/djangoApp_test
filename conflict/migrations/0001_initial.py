# Generated by Django 3.0.8 on 2020-07-17 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('position', models.IntegerField(verbose_name='Позиция/очередность')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Категория конфликтов',
                'verbose_name_plural': 'Категории конфликтов',
            },
        ),
        migrations.CreateModel(
            name='Conflict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Вопрос конфликта')),
                ('color', models.BooleanField(default=False, verbose_name='Подсвечивать')),
                ('position', models.IntegerField(verbose_name='Позиция/очередность')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('only_comment', models.BooleanField(default=False, verbose_name='Только комментарий')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conflicts', to='conflict.Category', verbose_name='Категория')),
                ('related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_question', to='conflict.Conflict', verbose_name='Зависит от')),
            ],
            options={
                'verbose_name': 'Конфликт',
                'verbose_name_plural': 'Конфликты',
            },
        ),
    ]