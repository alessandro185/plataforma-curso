from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InscricaoForm
from .models import Curso


def lista_cursos(request):
    cursos = Curso.objects.filter(ativo=True).order_by("titulo")
    ag = cursos.aggregate(total_horas=Sum("carga_horaria"))
    total_horas = ag["total_horas"] or 0
    total_cursos = cursos.count()
    return render(
        request,
        "cursos/lista.html",
        {
            "cursos": cursos,
            "total_cursos": total_cursos,
            "total_horas": total_horas,
        },
    )


def detalhe_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug, ativo=True)
    outros = (
        Curso.objects.filter(ativo=True)
        .exclude(pk=curso.pk)
        .order_by("titulo")[:4]
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
