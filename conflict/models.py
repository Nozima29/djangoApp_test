from django.db import models

class Category(models.Model):
    name = models.CharField('Название', max_length=255)
    position = models.IntegerField('Позиция/очередность')
    created_at = models.DateTimeField('Время создания', auto_now_add=True)

    def __str__(self):
        return self.name
    def __int__(self):
        return self.position

    class Meta:
        verbose_name = "Категория конфликтов"
        verbose_name_plural = "Категории конфликтов"


class Conflict(models.Model):
    question = models.TextField('Вопрос конфликта')
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 related_name='conflicts', verbose_name='Категория')
    color = models.BooleanField('Подсвечивать', default=False)
    position = models.IntegerField('Позиция/очередность')

    related = models.ForeignKey('self', verbose_name='Зависит от', on_delete=models.CASCADE,
                                null=True, blank=True, related_name='related_question'
                                #limit_choices_to={'category': 3}
                            )
    created_at = models.DateTimeField('Время создания', auto_now_add=True)

    only_comment = models.BooleanField('Только комментарий', default=False)

    def __str__(self):
        return str(self.question[:100])

    class Meta:
        verbose_name = "Конфликт"
        verbose_name_plural = "Конфликты"




