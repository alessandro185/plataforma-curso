from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Curso(models.Model):
    class Nivel(models.TextChoices):
        INICIANTE = "iniciante", "Iniciante"
        INTERMEDIARIO = "intermediario", "Intermediário"
        AVANCADO = "avancado", "Avançado"

    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    descricao = models.TextField()
    nivel = models.CharField(
        max_length=20,
        choices=Nivel.choices,
        default=Nivel.INICIANTE,
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    carga_horaria = models.PositiveIntegerField(
        default=0,
        help_text="Total de horas do curso.",
    )

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("cursos:detalhe", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:95] or "curso"
            slug = base
            n = 2
            while Curso.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Inscricao(models.Model):
    """Pedido de inscrição feito pelo visitante no site público."""

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="inscricoes",
    )
    nome = models.CharField(max_length=120)
    email = models.EmailField()
    telefone = models.CharField(max_length=32, blank=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        constraints = [
            models.UniqueConstraint(
                fields=["curso", "email"],
                name="uniq_inscricao_curso_email",
            ),
        ]

    def __str__(self):
        return f"{self.nome} — {self.curso.titulo}"
