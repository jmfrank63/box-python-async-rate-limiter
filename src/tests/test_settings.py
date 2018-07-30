import os
import pytest

import src.utils.settings as settings

@pytest.fixture
def box_settings(fs):
    return settings.Settings()


def test_a_new_settings_instance_is_empty(box_settings):
    assert isinstance(box_settings, settings.Settings)

def test_settings_holds_a_valid_path_to_default_folder(fs, box_settings):
    default_path = settings.DEFAULT_SETTINGS_PATH
    box_settings.path = default_path
    assert os.path.exists(default_path)

def test_prompted_for_settings_if_empty_or_does_not_exist(capsys, monkeypatch):
    def mock_input(instr):
        print(instr, end='')
        return settings.DEFAULT_CREDENTIALS
    with monkeypatch.context() as mck:
        mck.setattr('builtins.input', mock_input)
        box_settings = settings.get_credentials()
        out, _ = capsys.readouterr()
        assert out == settings.DEFAULT_PROMPT
        assert box_settings.credentials == settings.DEFAULT_CREDENTIALS



def test_settings_file_can_be_read(fs):
    pass
