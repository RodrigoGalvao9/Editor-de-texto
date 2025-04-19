import pytest
from unittest.mock import patch, MagicMock
import App.update_utils as update_utils
import sys
import os
import platform

@pytest.fixture
def mock_version_file(tmp_path, monkeypatch):
    version_file = tmp_path / "version.txt"
    version_file.write_text("1.0.0")
    monkeypatch.setattr(update_utils, "get_local_version", lambda: "1.0.0")
    return version_file

@patch("App.update_utils.requests.get")
def test_check_for_updates_new_version(mock_get, mock_version_file):
    system = platform.system()
    if system == "Windows":
        expected_asset = "BlocoDeNotas.exe"
    else:
        expected_asset = "BlocoDeNotas"  

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tag_name": "v2.0.0",
        "assets": [
            {
                "name": expected_asset,
                "browser_download_url": f"http://fake-url/{expected_asset}"
            }
        ],
        "html_url": "http://fake-release-page"
    }
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    with patch("App.update_utils.download_and_replace") as mock_download:
        update_utils.check_for_updates(auto_download=True)
        mock_download.assert_called_once_with(
            f"http://fake-url/{expected_asset}", expected_asset
        )

@patch("App.update_utils.requests.get")
def test_check_for_updates_no_new_version(mock_get, mock_version_file, capsys):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tag_name": "v1.0.0",
        "assets": [],
        "html_url": "http://fake-release-page"
    }
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    update_utils.check_for_updates(auto_download=True)
    captured = capsys.readouterr()
    assert "Você já está usando a versão mais recente." in captured.out

@patch("App.update_utils.requests.get")
def test_check_for_updates_error_handling(mock_get, capsys):
    mock_get.side_effect = Exception("Erro de conexão")
    update_utils.check_for_updates(auto_download=True)
    captured = capsys.readouterr()
    assert "Erro ao verificar atualizações" in captured.out

@patch("App.update_utils.requests.get")
def test_download_and_replace_cross_platform(mock_get, tmp_path, monkeypatch):
    # Simula o conteúdo do arquivo baixado
    fake_content = b"conteudo-fake"
    mock_response = MagicMock()
    mock_response.iter_content = lambda chunk_size: [fake_content]
    mock_response.__enter__.return_value = mock_response
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    # Caminhos temporários para simular o download
    final_file = tmp_path / "final_asset"

    # Mock para evitar que o teste finalize o processo
    monkeypatch.setattr(sys, "exit", lambda code=0: None)

    # Define o sistema operacional e o nome do asset
    system = platform.system().lower()
    asset_name = "BlocoDeNotas.exe" if system == "windows" else "BlocoDeNotas"

    # Mock para diferentes sistemas operacionais
    if system == "windows":
        with patch("App.update_utils.subprocess.Popen") as mock_popen:
            monkeypatch.setattr(update_utils.platform, "system", lambda: "Windows")

            # Chama a função sob teste
            update_utils.download_and_replace("http://fake-url/" + asset_name, str(final_file))

            # Verifica se o arquivo foi baixado corretamente
            assert final_file.exists()
            assert final_file.read_bytes() == fake_content

            # Verifica se o executável foi iniciado
            mock_popen.assert_called_once_with([str(final_file)], shell=True)
    else:
        with patch("App.update_utils.subprocess.Popen") as mock_popen:
            monkeypatch.setattr(update_utils.platform, "system", lambda: "Linux")

            # Chama a função sob teste
            update_utils.download_and_replace("http://fake-url/" + asset_name, str(final_file))

            # Verifica se o arquivo foi baixado corretamente
            assert final_file.exists()
            assert final_file.read_bytes() == fake_content

            # Verifica se o executável foi iniciado com permissões corretas
            mock_popen.assert_any_call([str(final_file)])