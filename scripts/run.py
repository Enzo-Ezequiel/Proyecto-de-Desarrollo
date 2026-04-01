"""
Script de ejecución rápida para la aplicación FastAPI.

Ejecuta la aplicación en modo desarrollo con auto-recarga.
"""

import subprocess
import sys


def main() -> None:
    """Ejecuta la aplicación FastAPI."""
    print("🚀 Iniciando aplicación FastAPI...")
    print("📍 URL: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("⏹️  Presiona CTRL+C para detener la aplicación\n")

    try:
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
            cwd=".",
        )
    except KeyboardInterrupt:
        print("\n✅ Aplicación detenida.")


if __name__ == "__main__":
    main()
