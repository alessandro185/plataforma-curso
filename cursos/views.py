from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InscricaoForm
from .models import Categoria, Curso


def lista_cursos(request):
    qs = Curso.objects.filter(ativo=True).select_related("categoria", "instrutor")

    # Busca textual
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(titulo__icontains=q) | Q(descricao__icontains=q)
        )

    # Filtro por nível
    nivel = request.GET.get("nivel", "").strip()
    if nivel in [c[0] for c in Curso.Nivel.choices]:
        qs = qs.filter(nivel=nivel)

    # Filtro por categoria
    categoria_slug = request.GET.get("categoria", "").strip()
    if categoria_slug:
        qs = qs.filter(categoria__slug=categoria_slug)

    # Ordenação
    ordem = request.GET.get("ordem", "destaque")
    ordem_opcoes = {
        "destaque": ["-destaque", "-avaliacao", "titulo"],
        "titulo": ["titulo"],
        "horas": ["-carga_horaria"],
        "avaliacao": ["-avaliacao"],
        "recente": ["-data_criacao"],
    }
    qs = qs.order_by(*ordem_opcoes.get(ordem, ["-destaque", "titulo"]))

    # Paginação
    paginator = Paginator(qs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    return render(
        request,
        "cursos/lista.html",
        {
            "page_obj": page_obj,
            "cursos": page_obj.object_list,
            "categorias": categorias,
            "q": q,
            "nivel_sel": nivel,
            "categoria_sel": categoria_slug,
            "ordem_sel": ordem,
            "total_cursos": paginator.count,
        },
    )


def detalhe_curso(request, slug):
    curso = get_object_or_404(
        Curso.objects.select_related("categoria", "instrutor"),
        slug=slug,
        ativo=True,
    )
    outros = (
        Curso.objects.filter(ativo=True)
        .exclude(pk=curso.pk)
        .select_related("categoria", "instrutor")
        .order_by("-destaque", "titulo")[:4]
    )

    if request.method == "POST":
        form = InscricaoForm(request.POST, curso=curso)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.curso = curso
            try:
                inscricao.save()
            except IntegrityError:
                form.add_error(
                    "email",
                    "Já existe uma inscrição com este e-mail neste curso.",
                )
            else:
                messages.success(
                    request,
                    "Inscrição enviada com sucesso. Entraremos em contacto por e-mail.",
                )
                return redirect(curso.get_absolute_url())
    else:
        form = InscricaoForm(curso=curso)

    abrir_inscricao = request.method == "POST" and not form.is_valid()

    return render(
        request,
        "cursos/detalhe.html",
        {
            "curso": curso,
            "outros_cursos": outros,
            "form": form,
            "abrir_inscricao": abrir_inscricao,
        },
    )

