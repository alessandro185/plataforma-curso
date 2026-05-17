import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cursos", "0002_curso_nivel_curso_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="Inscricao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("telefone", models.CharField(blank=True, max_length=32)),
                ("observacoes", models.TextField(blank=True)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                (
                    "curso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inscricoes",
                        to="cursos.curso",
                    ),
                ),
            ],
            options={
                "ordering": ["-criado_em"],
            },
        ),
        migrations.AddConstraint(
            model_name="inscricao",
            constraint=models.UniqueConstraint(
                fields=("curso", "email"),
                name="uniq_inscricao_curso_email",
            ),
        ),
    ]
