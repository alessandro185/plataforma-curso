from django.contrib import admin

from .models import Curso, Inscricao


class InscricaoInline(admin.TabularInline):
    model = Inscricao
    extra = 0
    readonly_fields = ("nome", "email", "telefone", "observacoes", "criado_em")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "slug",
        "nivel",
        "carga_horaria",
        "data_criacao",
        "ativo",
    )
    list_filter = ("ativo", "nivel")
    search_fields = ("titulo", "slug", "descricao")
    prepopulated_fields = {"slug": ("titulo",)}
    ordering = ("titulo",)
    inlines = [InscricaoInline]


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "curso", "criado_em")
    list_filter = ("curso",)
    search_fields = ("nome", "email", "curso__titulo")
    readonly_fields = ("criado_em",)
    ordering = ("-criado_em",)
