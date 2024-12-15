from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Scope, Tag

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        result = super(ScopeInlineFormset, self).clean()
        is_main_checked = False
        for form in self.forms:
            if form.is_valid():
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    if is_main_checked and form.cleaned_data['is_main']:
                        raise ValidationError('Основной раздел может быть только один')
                    if form.cleaned_data['is_main']:
                        is_main_checked = True
        if not is_main_checked:
            raise ValidationError('Не выбран основной раздел')
        return result

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
