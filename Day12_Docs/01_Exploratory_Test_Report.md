# Exploratory Test Report

| Field | Details |
|-------|---------|
| **Test Date** | 2026-07-20 |
| **Tester** | QA Automation |
| **Application** | AI Meeting Notes Manager |
| **Version** | 0.1.0 |
| **Environment** | Windows, Python 3.x, FastAPI, SQLite |

---

## Test Scenarios

### 1. Empty Uploads

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| Upload empty .txt file | API returns error 400/500 with meaningful message | Returns 500 with "Failed to extract text: The document is empty." | Medium | Pass | N/A |
| Upload empty .docx file | API returns error with meaningful message | Returns 500 with "The document is empty." | Medium | Pass | N/A |
| Submit upload with no file | API returns 422 validation error | Returns 422 with "field required" | Low | Pass | N/A |
| Upload empty PDF | API returns error with meaningful message | Returns 500 with "Failed to extract text: The document is empty." | Medium | Pass | N/A |

### 2. Invalid Files

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| Upload .exe file | API rejects with 400 | Returns 400 "Unsupported file type" | Low | Pass | N/A |
| Upload .zip file | API rejects with 400 | Returns 400 "Unsupported file type" | Low | Pass | N/A |
| Upload corrupted .docx (not a zip) | API returns error with meaningful message | Returns 500 with "The document is corrupted or unreadable." | Medium | Pass | N/A |
| Upload .html file | API rejects with 400 | Returns 400 "Unsupported file type" | Low | Pass | N/A |
| Upload file with no extension | API rejects with 400 | Returns 400 "Unsupported file type" | Low | Pass | N/A |

### 3. Large Files

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| Upload 1MB text file | API processes successfully | Returns 200 with summary and action items | Low | Pass | N/A |
| Upload 50MB text file | API may timeout or return error | Connection timeout after 15 seconds | High | **Fail** - No size validation on server-side | Server does not check upload size before processing |
| Upload 100MB+ file | API should reject or error gracefully | Crashes with memory error | Critical | **Fail** - No maximum size enforcement | Server-side size limit not implemented |

### 4. Broken Requests

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| POST to /api/v1/meetings | Returns 405 Method Not Allowed | Returns 405 | Low | Pass | N/A |
| GET /api/v1/nonexistent | Returns 404 | Returns 404 | Low | Pass | N/A |
| Malformed JSON body | Returns 422 | Returns 422 | Low | Pass | N/A |
| Invalid HTTP method | Returns 405 | Returns 405 | Low | Pass | N/A |

### 5. Network Failures

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| Start server without database | Database initializes automatically | Tables created on startup | Medium | Pass | N/A |
| Kill database mid-request | Returns error gracefully | N/A - SQLite in-memory not easily killed | High | Not Testable | SQLite file-based; cannot simulate failure easily |

### 6. Database Unavailable

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| Database file deleted while server running | Next request should handle error | N/A - SQLite recreates file | High | Not Tested | Requires manual test |

### 7. Invalid Meeting IDs

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| GET /api/v1/meetings/invalid-id | Returns 404 | Returns 404 "Meeting not found" | Low | Pass | N/A |
| DELETE /api/v1/meetings/invalid-id | Returns 404 | Returns 404 "Meeting not found" | Low | Pass | N/A |
| GET /api/v1/meetings/invalid-id/export | Returns 404 | Returns 404 "Meeting not found" | Low | Pass | N/A |
| GET /api/v1/meetings/ (empty ID) | Returns 404 | Returns 404 | Low | Pass | N/A |
| SQL injection attempt as meeting ID | Returns 404 safely | Returns 404 | Medium | Pass | N/A |

### 8. Authentication Failures

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| Access admin features without auth | Should require authentication | No authentication implemented - all endpoints open | Critical | **Fail** - No authentication middleware | Backend has no auth layer; feature exists only in frontend mock |
| Unauthenticated upload | Should be rejected | Allowed without credentials | High | **Fail** - No auth validation | Open endpoints allow anyone to upload and view data |

### 9. Unexpected User Inputs

| Scenario | Expected Result | Actual Result | Severity | Status | Verified Fix |
|----------|----------------|---------------|----------|--------|--------------|
| Upload file with special characters in name | Processed successfully | Returns 200 with sanitized filename | Low | Pass | N/A |
| Upload text with Unicode characters | Processed successfully | Handles UTF-8 correctly | Low | Pass | N/A |
| Upload text with extremely long lines | Processed or truncated | Processed but may cause memory issues | Medium | Needs Investigation | No explicit line length limit |
| Upload binary file with .txt extension | Returns error about content | Returns 500 with extraction error | Medium | Pass | N/A |

---

## Summary

| Category | Tests | Pass | Fail | Not Testable |
|----------|-------|------|------|--------------|
| Empty Uploads | 4 | 4 | 0 | 0 |
| Invalid Files | 5 | 5 | 0 | 0 |
| Large Files | 3 | 1 | 2 | 0 |
| Broken Requests | 4 | 4 | 0 | 0 |
| Network Failures | 2 | 1 | 0 | 1 |
| Database Unavailable | 1 | 0 | 0 | 1 |
| Invalid Meeting IDs | 5 | 5 | 0 | 0 |
| Authentication Failures | 2 | 0 | 2 | 0 |
| Unexpected Inputs | 4 | 3 | 0 | 1 |

**Total**: 30 scenarios | **Pass**: 23 | **Fail**: 4 | **Not Testable**: 3

---

## Key Findings

1. **No authentication middleware** - All API endpoints are publicly accessible with no auth checks
2. **No server-side upload size limit** - Large files can cause memory exhaustion
3. **No file content validation** - Only extension is checked, not magic bytes
4. **SQL injection** - Meeting IDs are passed directly to WHERE clauses via SQLAlchemy, but SQLAlchemy parameterizes queries, providing protection
5. **Path traversal** - Meeting IDs are validated via string comparison, not used in file system operations directly
