from decimal import Decimal
from django.db import migrations


def create_initial_data(apps, schema_editor):
    Categoria = apps.get_model('cursos', 'Categoria')
    Instrutor = apps.get_model('cursos', 'Instrutor')
    Curso = apps.get_model('cursos', 'Curso')

    cat_prog, _ = Categoria.objects.get_or_create(nome='Programação', defaults={'slug': 'programacao'})
    if cat_prog.slug != 'programacao':
        cat_prog.slug = 'programacao'
        cat_prog.save()

    cat_web, _ = Categoria.objects.get_or_create(nome='Desenvolvimento Web', defaults={'slug': 'desenvolvimento-web'})
    if cat_web.slug != 'desenvolvimento-web':
        cat_web.slug = 'desenvolvimento-web'
        cat_web.save()

    cat_api, _ = Categoria.objects.get_or_create(nome='Backend e APIs', defaults={'slug': 'backend-e-apis'})
    if cat_api.slug != 'backend-e-apis':
        cat_api.slug = 'backend-e-apis'
        cat_api.save()

    inst_ana, _ = Instrutor.objects.get_or_create(
        nome='Ana Ferreira',
        defaults={'bio': 'Especialista em Python e Engenharia de Dados com 8+ anos de experiência.'}
    )
    inst_carlos, _ = Instrutor.objects.get_or_create(
        nome='Carlos Mendes',
        defaults={'bio': 'Tech Lead e desenvolvedor full stack Django & React.'}
    )
    inst_beatriz, _ = Instrutor.objects.get_or_create(
        nome='Beatriz Costa',
        defaults={'bio': 'Arquiteta de software e especialista em microsserviços e cloud.'}
    )

    c1 = Curso.objects.filter(slug='python-do-zero-ao-profissional').first()
    if c1:
        c1.categoria = cat_prog
        c1.instrutor = inst_ana
        c1.preco = None
        c1.avaliacao = Decimal('4.8')
        c1.total_alunos = 1240
        c1.destaque = True
        c1.save()
    else:
        Curso.objects.create(
            titulo='Python do Zero ao Profissional',
            slug='python-do-zero-ao-profissional',
            descricao='Aprenda lógica de programação, orientação a objetos, automação de tarefas e fundamentos sólidos em Python 3.',
            carga_horaria=40,
            nivel='iniciante',
            categoria=cat_prog,
            instrutor=inst_ana,
            preco=None,
            avaliacao=Decimal('4.8'),
            total_alunos=1240,
            destaque=True,
            ativo=True,
        )

    c2 = Curso.objects.filter(slug='desenvolvimento-web-com-django').first()
    if c2:
        c2.categoria = cat_web
        c2.instrutor = inst_carlos
        c2.preco = Decimal('89.90')
        c2.avaliacao = Decimal('4.6')
        c2.total_alunos = 880
        c2.destaque = True
        c2.save()
    else:
        Curso.objects.create(
            titulo='Desenvolvimento Web com Django',
            slug='desenvolvimento-web-com-django',
            descricao='Domine o ecossistema Django: MVT, formulários, autenticação, ORM, painel administrativo e boas práticas.',
            carga_horaria=60,
            nivel='intermediario',
            categoria=cat_web,
            instrutor=inst_carlos,
            preco=Decimal('89.90'),
            avaliacao=Decimal('4.6'),
            total_alunos=880,
            destaque=True,
            ativo=True,
        )

    c3 = Curso.objects.filter(slug='apis-restful-e-arquitetura-backend').first()
    if c3:
        c3.categoria = cat_api
        c3.instrutor = inst_beatriz
        c3.preco = Decimal('129.90')
        c3.avaliacao = Decimal('4.9')
        c3.total_alunos = 512
        c3.destaque = False
        c3.save()
    else:
        Curso.objects.create(
            titulo='APIs RESTful e Arquitetura Backend',
            slug='apis-restful-e-arquitetura-backend',
            descricao='Construa APIs escaláveis, documentação interativa, testes automatizados e integração de microsserviços.',
            carga_horaria=35,
            nivel='avancado',
            categoria=cat_api,
            instrutor=inst_beatriz,
            preco=Decimal('129.90'),
            avaliacao=Decimal('4.9'),
            total_alunos=512,
            destaque=False,
            ativo=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0004_categoria_instrutor_alter_curso_options_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_code=migrations.RunPython.noop),
    ]
