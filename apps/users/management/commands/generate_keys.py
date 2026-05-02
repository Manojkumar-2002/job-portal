import os
from pathlib import Path
from cryptography.fernet import Fernet
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = "Generate SECRET_KEY and TOTP_ENCRYPTION_KEY and write to .env"

    def add_arguments(self, parser):
        parser.add_argument(
            "--print-only",
            action="store_true",
            help="Only print the keys without writing to .env",
        )

    def handle(self, *args, **options):
        secret_key = get_random_secret_key()
        totp_key = Fernet.generate_key().decode()

        if options["print_only"]:
            self.stdout.write(self.style.SUCCESS(f"SECRET_KEY={secret_key}"))
            self.stdout.write(self.style.SUCCESS(f"TOTP_ENCRYPTION_KEY={totp_key}"))
            return

        env_path = Path(os.getcwd()) / ".env"
        existing = env_path.read_text() if env_path.exists() else ""

        lines = []
        skipped = []

        if "SECRET_KEY" not in existing:
            lines.append(f"SECRET_KEY={secret_key}")
        else:
            skipped.append("SECRET_KEY")

        if "TOTP_ENCRYPTION_KEY" not in existing:
            lines.append(f"TOTP_ENCRYPTION_KEY={totp_key}")
        else:
            skipped.append("TOTP_ENCRYPTION_KEY")

        if skipped:
            self.stdout.write(self.style.WARNING(f"Already exists in .env, skipping: {', '.join(skipped)}"))

        if lines:
            with env_path.open("a") as f:
                f.write("\n".join(lines) + "\n")
            self.stdout.write(self.style.SUCCESS(f"Written to .env: {', '.join(l.split('=')[0] for l in lines)}"))
