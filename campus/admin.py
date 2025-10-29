from django.contrib import admin
from .models import Zone, Building, Division, Task, Subtask

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'floors')
    list_filter = ('zone',)
    search_fields = ('name',)

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'division', 'created_at')
    list_filter = ('division__building__zone', 'division__building')
    inlines = [SubtaskInline]

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'assistant')
    list_filter = ('building__zone', 'building')
    search_fields = ('name',)
