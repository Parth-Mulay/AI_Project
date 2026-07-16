# Bug Reproduction Notes

## 1. Import-path failure
- Symptom: pytest failed during collection because package-relative imports were not resolving consistently.
- Evidence: ImportError surfaced when the test suite attempted to import the application modules.
- Fix: Standardized imports to use package-safe relative imports and added a fallback for the logger configuration.

## 2. Upload endpoint regression
- Symptom: the FastAPI upload route returned 405 for file uploads because the static mount intercepted the route before the API router handled it.
- Evidence: Exercising the endpoint with the FastAPI test client showed the route conflict.
- Fix: preserved API routing precedence and confirmed the upload endpoint now accepts multipart uploads successfully.

## 3. NLP dependency resilience
- Symptom: the upload pipeline failed when optional NLP dependencies such as dateparser and spaCy were unavailable.
- Evidence: the upload endpoint raised ModuleNotFoundError in the NLP pipeline during test execution.
- Fix: introduced fallback logic so the app continues processing with a lightweight rule-based path when advanced NLP packages are absent.
