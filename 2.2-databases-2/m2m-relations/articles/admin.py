from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        main_count = 0
        for form in self.forms:
            # Проверяем, что форма прошла валидацию и не помечена на удаление (чекбокс DELETE)
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_main'):
                    main_count += 1
        
        # Если основных разделов не ровно 1, выбрасываем ошибку
        if main_count != 1:
            raise ValidationError('У статьи должен быть указан ровно один основной раздел.')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1  # Количество пустых форм для добавления новых связей


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass