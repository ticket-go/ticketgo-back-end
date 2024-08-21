from datetime import datetime
from pathlib import Path
import environ, os
import dotenv
import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Faz o backup do banco de dados"

    def handle(self, *args, **kwargs):
        dotenv.load_dotenv()

        env = environ.Env()
        environ.Env.read_env()

        def backup():
            backup_dir = Path(__file__).resolve().parent.parent.parent / "backups"

            file_name = (
                f'{env("DB_NAME")}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
            )

            backup_path = f"{backup_dir}\\{file_name}.sql"

            pg_dump_command = f'pg_dump -h {env("DB_HOST")} -p {env("DB_PORT")} -U {env("DB_USER")} -d {env("DB_NAME")} -f {backup_path}'

            print("Iniciando o backup")

            os.environ["PGPASSWORD"] = env("DB_PASSWORD")

            try:
                subprocess.run(
                    pg_dump_command, check=True, text=True, capture_output=True
                )
                print("Backup realizado com sucesso!")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar pg_dump: {e}")
                print(f"Saída padrão: {e.stdout}")
                print(f"Saída de erro: {e.stderr}")

        backup()
