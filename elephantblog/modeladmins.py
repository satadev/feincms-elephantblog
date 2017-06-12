from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from django.forms.models import ModelForm
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from feincms.admin import item_editor
from feincms.translations import admin_translationinline
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from elephantblog.models import CategoryTranslation, Entry


CategoryTranslationInline = admin_translationinline(
    CategoryTranslation,
    prepopulated_fields={
        'slug': ('title',)
    })


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTranslationInline]
    list_display = ['__str__', 'ordering', 'entries']
    list_editable = ['ordering']
    search_fields = ['translations__title']

    def entries(self, obj):
        return ', '.join(
            force_text(entry)
            for entry in Entry.objects.filter(categories=obj)
        ) or '-'
    entries.short_description = _('Blog entries in category')


class EntryAdminForm(ModelForm):
    tags = TagField(required=False, widget=LabelWidget)


class EntryAdmin(item_editor.ItemEditor):
    actions = []

    form = EntryAdminForm

    date_hierarchy = 'published_on'
    filter_horizontal = ['categories']
    list_display = [
        'title', 'is_active', 'is_featured', 'published_on', 'author']
    list_editable = ['is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'categories', 'author', 'tags']
    raw_id_fields = ['author']
    search_fields = ['title', 'slug']
    prepopulated_fields = {
        'slug': ('title',),
    }

    fieldset_insertion_index = 2
    fieldsets = [
        [None, {
            'fields': [
                ('title', 'slug'),
                'author',
                ('is_active', 'is_featured', ),
                'tags',
            ]
        }],
        [_('Other options'), {
            'fields': [
                'categories',
                'published_on',
            ],
            'classes': ('collapse',),
        }],
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
        return super(EntryAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
