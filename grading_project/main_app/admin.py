from django.contrib import admin

from main_app.models import Profile, Criteria, Grading, Table


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'ratings']

    def full_name(self, obj):
        return obj.user.get_full_name()

    full_name.short_description = 'Юзер'


class CriteriaAdmin(admin.ModelAdmin):
    list_display = ['title', 'standard_in_points', 'table_name']

    def table_name(self, obj):
        return obj.table_title.table

    table_name.short_description = 'Название таблицы'


class GradingAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'criteria_title', 'work_done', 'rating']

    def criteria_title(self, obj):
        return obj.used_standard.title

    def full_name(self, obj):
        return obj.user.get_full_name()

    full_name.short_description = 'Юзер'

    criteria_title.short_description = 'Наименование работ'


class TableAdmin(admin.ModelAdmin):
    list_display = ['table']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Grading, GradingAdmin)
admin.site.register(Table, TableAdmin)
