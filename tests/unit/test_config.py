"""Unit tests for application configuration."""

from src.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_AUTHOR,
    DEBUG,
    LOG_LEVEL,
    MAX_UPLOAD_SIZE_MB,
    API_TIMEOUT_SECONDS,
    RETRY_ATTEMPTS,
    SUPPORTED_AUDIO_FORMATS,
    SUPPORTED_EXPORT_FORMATS,
    AI_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)


class TestProjectConfig:
    def test_project_name(self):
        assert PROJECT_NAME == "AI Meeting Notes Manager"

    def test_project_version(self):
        assert isinstance(PROJECT_VERSION, str)
        assert len(PROJECT_VERSION) > 0

    def test_project_author(self):
        assert isinstance(PROJECT_AUTHOR, str)
        assert len(PROJECT_AUTHOR) > 0

    def test_debug_flag(self):
        assert isinstance(DEBUG, bool)

    def test_log_level(self):
        assert LOG_LEVEL in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    def test_max_upload_size(self):
        assert isinstance(MAX_UPLOAD_SIZE_MB, int)
        assert MAX_UPLOAD_SIZE_MB > 0

    def test_api_timeout(self):
        assert isinstance(API_TIMEOUT_SECONDS, int)
        assert API_TIMEOUT_SECONDS > 0

    def test_retry_attempts(self):
        assert isinstance(RETRY_ATTEMPTS, int)
        assert RETRY_ATTEMPTS > 0

    def test_supported_audio_formats(self):
        assert ".mp3" in SUPPORTED_AUDIO_FORMATS
        assert ".wav" in SUPPORTED_AUDIO_FORMATS
        assert isinstance(SUPPORTED_AUDIO_FORMATS, list)

    def test_supported_export_formats(self):
        assert "markdown" in SUPPORTED_EXPORT_FORMATS
        assert isinstance(SUPPORTED_EXPORT_FORMATS, list)

    def test_ai_model(self):
        assert isinstance(AI_MODEL, str)

    def test_temperature(self):
        assert isinstance(TEMPERATURE, (int, float))
        assert 0 <= TEMPERATURE <= 1

    def test_max_tokens(self):
        assert isinstance(MAX_TOKENS, int)
        assert MAX_TOKENS > 0
