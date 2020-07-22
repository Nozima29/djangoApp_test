from django.contrib import admin
from .models import Category, Conflict

@admin.register(Conflict)
class ShowConflicts(admin.ModelAdmin):
    model = Conflict
    list_display = ['id', 'question', 'category', 'related']

class ConflictAdmin(admin.TabularInline):
    model = Conflict
    ordering = ['position']


class AddConflictAdmin(admin.TabularInline):
    model = Conflict
    classes = ['collapse']
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    extra = 0
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(AddConflictAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'related':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(category=request._obj_)
                print(field.queryset)
            else:
                field.queryset = field.queryset.none()

        return field

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #list_display = ['id', 'name', 'position','created_at']
    fieldsets = [
        (None, {'fields': ['name', 'position']})
    ]
    inlines = [ConflictAdmin, AddConflictAdmin]
    oredering = ['position']
    search_fields = ['name', 'id']
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        request._obj_ = obj
        return super(CategoryAdmin, self).get_form(request, obj, **kwargs)


#admin.site.register(Category, CategoryAdmin)
