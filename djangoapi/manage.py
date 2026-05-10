#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from djangoapi.settings import REMOTE_DEBUG

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoapi.settings')

    from django.conf import settings
    if settings.DEBUG:
        if REMOTE_DEBUG:
            if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
                import debugpy
                print("Running in DEBUG mode")
                debugpy.listen(("0.0.0.0", 6789))  # El puerto debe coincidir con el expuesto en Docker
                print("Esperando para depurar...")
                debugpy.wait_for_client()  # Opcional: espera a que VS Code se conecte antes de continuar
    else:
        print("Running in PRODUCTION mode")
    ###FIN AÑADIR ESTO#####

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
