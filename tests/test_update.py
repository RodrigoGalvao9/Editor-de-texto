import pytest
from unittest.mock import patch, MagicMock
import App.update_utils as update_utils
import sys

@pytest.fixture
def mock_version_file(tmp_path, monkeypatch):
    version_file = tmp_path / "version.txt"
    version_file.write_text("1.0.0")
    monkeypatch.setattr(update_utils, "get_local_version", lambda: "1.0.0")
    return version_file

@patch("App.update_utils.requests.get")
def test_check_for_updates_new_version(mock_get, mock_version_file):
    # Simula resposta da API do GitHub com nova versão
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tag_name": "v2.0.0",
        "assets": [
            {"name": "BlocoDeNotas.exe", "browser_download_url": "http://fake-url/BlocoDeNotas.exe"}
        ],
        "html_url": "http://fake-release-page"
    }
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    with patch("App.update_utils.download_and_replace") as mock_download:
        update_utils.check_for_updates(auto_download=True)
        mock_download.assert_called_once_with("http://fake-url/BlocoDeNotas.exe", "BlocoDeNotas.exe")

@patch("App.update_utils.requests.get")
def test_check_for_updates_no_new_version(mock_get, mock_version_file, capsys):
    # Simula resposta da API do GitHub com mesma versão
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
    # Simula erro de conexão
    mock_get.side_effect = Exception("Erro de conexão")
    update_utils.check_for_updates(auto_download=True)
    captured = capsys.readouterr()
    assert "Erro ao verificar atualizações" in captured.out

@patch("App.update_utils.requests.get")
@patch("App.update_utils.os.startfile")
def test_download_and_replace_windows(mock_startfile, mock_get, tmp_path, monkeypatch):
    # Simula download do executável no Windows
    asset_name = "BlocoDeNotas.exe"
    fake_content = b"conteudo-fake"
    mock_response = MagicMock()
    mock_response.iter_content = lambda chunk_size: [fake_content]
    mock_response.__enter__.return_value = mock_response
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    monkeypatch.setattr(sys, "exit", lambda code=0: None)
    monkeypatch.setattr(update_utils.platform, "system", lambda: "Windows")

    update_utils.download_and_replace("http://fake-url/BlocoDeNotas.exe", asset_name)
    mock_startfile.assert_called()
