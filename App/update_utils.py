import requests
import os
import sys
import tempfile
import webbrowser
from packaging import version
from pathlib import Path
import platform
import subprocess

def get_local_version():
    version_file = Path(__file__).parent / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"

REPO = "RodrigoGalvao9/Editor-de-texto"

def get_asset_name():
    system = platform.system().lower()
    if system == "windows":
        return "BlocoDeNotas.exe"
    elif system == "linux":
        return "BlocoDeNotas"
    else:
        raise Exception("Sistema operacional não suportado")

def check_for_updates(auto_download=True):
    local_version = get_local_version()
    print(f"Versão atual: {local_version}")

    url = f"https://api.github.com/repos/{REPO}/releases/latest"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        latest_version = data["tag_name"].lstrip("v")
        asset_name = get_asset_name()

        if version.parse(latest_version) > version.parse(local_version):
            print(f"Nova versão disponível: {latest_version}")

            asset_url = None
            for asset in data["assets"]:
                if asset["name"] == asset_name:
                    asset_url = asset["browser_download_url"]
                    break

            if asset_url and auto_download:
                download_and_replace(asset_url, asset_name)
            else:
                webbrowser.open(data["html_url"])
        else:
            print("Você já está usando a versão mais recente.")
    except Exception as e:
        print(f"Erro ao verificar atualizações: {e}")

def download_and_replace(url, asset_name):
    print("Baixando atualização...")
    local_path = os.path.join(tempfile.gettempdir(), asset_name)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Atualização baixada para: {local_path}")
    print("Iniciando nova versão...")

    try:
        if platform.system().lower() == "windows":
            subprocess.Popen([local_path], shell=True)
        else:
            os.chmod(local_path, 0o755)
            subprocess.Popen([local_path])
    except Exception as e:
        print(f"Erro ao iniciar a nova versão: {e}")
    finally:
        sys.exit(0)
