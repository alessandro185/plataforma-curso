from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Categoria(models.Model):
    nome = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)[:80] or "categoria"
        super().save(*args, **kwargs)


class Instrutor(models.Model):
    nome = models.CharField(max_length=120)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Instrutor"
        verbose_name_plural = "Instrutores"

    def __str__(self):
        return self.nome


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
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cursos",
    )
    instrutor = models.ForeignKey(
        Instrutor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cursos",
    )
    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Deixe em branco para 'Gratuito'.",
    )
    avaliacao = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0,
        help_text="Nota de 0.0 a 5.0.",
    )
    total_alunos = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    carga_horaria = models.PositiveIntegerField(
        default=0,
        help_text="Total de horas do curso.",
    )
    destaque = models.BooleanField(
        default=False,
        help_text="Exibir em destaque no topo do catálogo.",
    )

    class Meta:
        ordering = ["-destaque", "titulo"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("cursos:detalhe", kwargs={"slug": self.slug})

    @property
    def preco_display(self):
        if self.preco is None:
            return "Gratuito"
        if self.preco == 0:
            return "Gratuito"
        valor = f"{self.preco:.2f}".replace(".", ",")
        return f"R$ {valor}"

    @property
    def avaliacao_inteira(self):
        return int(round(float(self.avaliacao)))

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

