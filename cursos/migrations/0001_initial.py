from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Curso",
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
                ("titulo", models.CharField(max_length=100)),
                ("descricao", models.TextField()),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                ("ativo", models.BooleanField(default=True)),
                ("carga_horaria", models.IntegerField(default=0)),
            ],
        ),
    ]
