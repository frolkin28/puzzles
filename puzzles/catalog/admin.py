
from django.contrib import admin

from puzzles.catalog.models.puzzle import Puzzle


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'pieces', 'price', 'status', 'condition', 'created_at'
    )
    readonly_fields = (
        'search_vector',
    )
