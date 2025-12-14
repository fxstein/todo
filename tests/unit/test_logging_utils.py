from todo_ai.utils.logging import get_logger, setup_logging


def test_setup_logging_console(capsys):
    logger = setup_logging(verbose=True)
    logger.info("Test Info")
    logger.debug("Test Debug")

    captured = capsys.readouterr()
    assert "Test Info" in captured.out
    assert "Test Debug" in captured.out


def test_setup_logging_file(tmp_path):
    log_file = tmp_path / "test.log"
    logger = setup_logging(log_file=log_file)

    logger.info("File Info")

    content = log_file.read_text(encoding="utf-8")
    assert "File Info" in content


def test_get_logger():
    logger = get_logger()
    assert logger.name == "todo_ai"
