from pathlib import Path

from backend.ai.guardrails import Guardrails
from backend.ai.llm_service import AISummaryService
from backend.ai.rag import LocalRagPipeline

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_guardrails_rejects_empty_input() -> None:
    guardrails = Guardrails(max_input_chars=2000)
    try:
        guardrails.validate_input("   ")
    except ValueError as exc:
        assert "empty" in str(exc).lower()
    else:
        raise AssertionError("expected empty input to fail")


def test_ai_summary_service_falls_back_when_unconfigured(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    service = AISummaryService(provider=None)
    result = service.generate_summary("Priya will review the migration plan by Friday.")
    assert result["source"] == "fallback"
    assert "review" in result["summary"].lower()


def test_rag_pipeline_retrieves_related_chunk() -> None:
    storage_path = PROJECT_ROOT / "test_rag_store.json"
    storage_path.unlink(missing_ok=True)

    try:
        pipeline = LocalRagPipeline(storage_path=storage_path)
        pipeline.index_documents([
            "The team agreed to ship the authentication module by Friday.",
            "The product launch will happen in two weeks.",
        ])
        matches = pipeline.retrieve("authentication module deadline", top_k=1)
    finally:
        storage_path.unlink(missing_ok=True)

    assert matches
    assert "authentication" in matches[0]["text"].lower()
