from django.contrib import admin

from .models import Categoria, Curso, Inscricao, Instrutor


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Instrutor)
class InstrutorAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


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
        "categoria",
        "instrutor",
        "carga_horaria",
        "avaliacao",
        "total_alunos",
        "preco",
        "destaque",
        "ativo",
        "data_criacao",
    )
    list_filter = ("ativo", "nivel", "destaque", "categoria")
    search_fields = ("titulo", "slug", "descricao")
    prepopulated_fields = {"slug": ("titulo",)}
    ordering = ("-destaque", "titulo")
    list_editable = ("ativo", "destaque")
    inlines = [InscricaoInline]


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "curso", "criado_em")
    list_filter = ("curso",)
    search_fields = ("nome", "email", "curso__titulo")
    readonly_fields = ("criado_em",)
    ordering = ("-criado_em",)
