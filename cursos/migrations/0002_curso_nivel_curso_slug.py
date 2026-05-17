from django.db import migrations, models
from django.utils.text import slugify


def popular_slugs(apps, schema_editor):
    Curso = apps.get_model("cursos", "Curso")
    for curso in Curso.objects.all():
        if curso.slug:
            continue
        base = slugify(curso.titulo)[:95] or "curso"
        slug = base
        n = 2
        while Curso.objects.filter(slug=slug).exclude(pk=curso.pk).exists():
            slug = f"{base}-{n}"
            n += 1
        curso.slug = slug
        curso.save(update_fields=["slug"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("cursos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="curso",
            name="nivel",
            field=models.CharField(
                choices=[
                    ("iniciante", "Iniciante"),
                    ("intermediario", "Intermediário"),
                    ("avancado", "Avançado"),
                ],
                default="iniciante",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="curso",
            name="slug",
            field=models.SlugField(max_length=120, null=True, unique=True),
        ),
        migrations.RunPython(popular_slugs, noop_reverse),
        migrations.AlterField(
            model_name="curso",
            name="slug",
            field=models.SlugField(db_index=True, max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name="curso",
            name="carga_horaria",
            field=models.PositiveIntegerField(
                default=0, help_text="Total de horas do curso."
            ),
        ),
    ]
