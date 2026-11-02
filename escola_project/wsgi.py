"""Configuração WSGI para o projeto escola_project."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "escola_project.settings")

application = get_wsgi_application()
app = application

# No ambiente Vercel (serverless com SQLite em /tmp), garante que as tabelas e dados existam
if os.environ.get("VERCEL"):
    try:
        from django.core.management import call_command
        call_command("migrate", interactive=False)
    except Exception as e:
        print("Aviso ao rodar migrações no Vercel:", e)
