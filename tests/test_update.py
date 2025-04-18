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
    asset_name = "BlocoDeNotas.exe"
    fake_content = b"conteudo-fake"

    mock_response = MagicMock()
    mock_response.iter_content = lambda chunk_size: [fake_content]
    mock_response.__enter__.return_value = mock_response
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    monkeypatch.setattr(sys, "exit", lambda code=0: None)

    system = platform.system()

    if system == "Windows":
        with patch("App.update_utils.os.startfile") as mock_startfile:
            monkeypatch.setattr(update_utils.platform, "system", lambda: "Windows")
            update_utils.download_and_replace("http://fake-url/BlocoDeNotas.exe", asset_name)
            mock_startfile.assert_called_once()
    else:
        with patch("App.update_utils.subprocess.Popen") as mock_popen:
            monkeypatch.setattr(update_utils.platform, "system", lambda: system)
            update_utils.download_and_replace("http://fake-url/BlocoDeNotas.exe", asset_name)
            assert mock_popen.call_count >= 2
            chmod_call = mock_popen.call_args_list[0][0][0]
            exec_call = mock_popen.call_args_list[1][0][0]
            assert "chmod" in chmod_call or exec_call[0].startswith("./")
