from django.shortcuts import render
from django.http import HttpResponse
from .models import Conflict
from django import forms

def create_form(request):
    #template = 'conflict/test.html'
    template = 'conflict/create_form.html'
    conflicts = Conflict.objects.all().order_by('position')
    data = []
    parent = Conflict.objects.filter(related_id__isnull=False)
    for c in conflicts:
        for p in parent:
            if c.id == p.id:
                data.append(dict({'related_id': c.related_id, 'parent': p, 'related': c.related}))

    form = ConflictForm(conflicts=conflicts, data=data)
    if request.method == 'Post':
        form = ConflictForm(request.POST, conflicts=conflicts, data=data)

    context = {
        'conflicts': conflicts,
        'form': form
    }

    return render(request, template, context)

CONFIRM_CHOICE = (
    (0, 'Подтверждаю'),
    (1, 'Не подтверждаю'),
)
NONE_CHOICE = ((None, '---------'),)


class CustomChoiceField(forms.ChoiceField):
    def __init__(self, *, obj=None, choices=(), **kwargs):
        self.obj = obj
        super().__init__(choices=choices, **kwargs)


class CustomCharField(forms.CharField):

    def __init__(self, *, obj=None,
                 has_solution=None,
                 max_length=None,
                 min_length=None,
                 strip=True,
                 empty_value='',
                 **kwargs):
        self.obj = obj
        self.has_solution = has_solution
        super().__init__(max_length=max_length,
                         min_length=min_length,
                         strip=strip,
                         empty_value=empty_value,
                         **kwargs)


class ConflictForm(forms.Form):

    def __init__(self, **kwargs):
        self.conflicts = kwargs.pop('conflicts', [])
        self.data = kwargs.pop('data', [])
        super(ConflictForm, self).__init__(**kwargs)
        old_category = ''
        print('aaaaaaaa')
        for d in self.data:
            print(d['parent'])
        for conflict in self.conflicts:
            category = conflict.category.name
            print(conflict,conflict.related_id)
            changed = False
            if category != old_category:
                old_category = category
                changed = True
            self.fields['custom_confirm_%s' % conflict.id] = CustomChoiceField(
                obj=conflict,
                label=conflict.question,
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'style': 'display:inline;' if not conflict.only_comment else 'display:none;'
                }), choices=CONFIRM_CHOICE
            )
            self.fields['custom_comment_%s' % conflict.id] = forms.CharField(
                label=category if changed else '',
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 4,
                }),
                required=False
            )


    def clean(self):
        cleaned_data = super(ConflictForm, self).clean()
        if self.draft:
            return cleaned_data

        for field in self.conflicts_answers():
            if field['confirm']['value'] == '0' and not field['comment']['value']:
                # if not field['confirm']['field'].obj.only_comment:
                self.add_error('custom_comment_{}'.format(field['id']), 'Заполните поле')

            print(field['confirm']['field'].obj.category.name)
            print(field['confirm']['field'].obj.only_comment)
            # elif not field['comment']['value'] and field['confirm']['field'].obj.only_comment:
            #     self.add_error('custom_comment_{}'.format(field['id']), 'Заполните поле')

        parent = self.conflicts.filter(related_isnull = False)
        print(parent)

        return cleaned_data

    def conflict_fields(self):
        for field in self.fields:
            name = field
            if name.startswith('custom_confirm_'):
                if len(name.split('_')) == 3:
                    cid = name.split('_')[-1]
                    yield {
                        'id': cid,
                        'confirm': {'value': '', 'field': self[name]},
                        'comment': {'value': '', 'field': self['custom_comment_{}'.format(cid)], }
                    }

    def conflicts_answers(self):
        cleaned = self.cleaned_data.copy()
        for name, value in cleaned.items():
            if name.startswith('custom_comment_'):
                if len(name.split('_')) == 3:
                    cid = name.split('_')[-1]
                    confirm = self.cleaned_data.get('custom_confirm_{}'.format(cid), False)
                    yield {
                        'id': cid,
                        'obj': self.fields['custom_confirm_{}'.format(cid)].obj,
                        'comment': {'value': value, 'field': self.fields[name]},
                        'confirm': {'value': confirm, 'field': self.fields['custom_confirm_{}'.format(cid)], }
                    }


