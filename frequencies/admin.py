from django.contrib import admin
from csv import writer as csv_writer
from django.http import HttpResponse
from .models import Stimulus, Form, Reply

@admin.register(Stimulus)
class StimulusAdmin(admin.ModelAdmin):
    list_display = ('term', 'file_name', 'is_active')


class ReplyInline(admin.TabularInline):
    readonly_fields = ('stimulus', 'familiarity')
    model = Reply
    can_delete = False

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin.css', )
        }
    list_display = ('name', 'test_mode', 'created_at')
    ordering = ('-created_at',)
    inlines = (ReplyInline, )
    actions = ["export_as_csv"]

    def has_change_permission(self, request, obj=None):
        return False

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv_writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exportar Formularios seleccionado/s"

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('form', 'stimulus', 'familiarity')
    actions = ["export_as_csv"]

    def has_change_permission(self, request, obj=None):
        return False

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv_writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exportar Respuestas seleccionado/s"
