# Error Handling Standard

## Purpose

This document defines expected error handling for Lumina Rec APIs.

## Error Response Goals

API errors should be:

- Predictable
- Clear
- Safe
- Testable

## Current Error Responses

| Condition | Status | Endpoint |
|---|---:|---|
| Missing API key | 401 | /predict, /recommend |
| Invalid API key | 401 | /predict, /recommend |
| Missing required field | 422 | /predict, /recommend |
| Invalid top_n | 422 | /recommend |
| Unknown user_id | 404 | /predict, /recommend |
| Unknown movie_id | 404 | /predict |
| Rate limit exceeded | 429 | /predict, /recommend |
| Internal prediction failure | 500 | /predict |
| Internal recommendation failure | 500 | /recommend |

## Rules

- Do not expose stack traces in API responses.
- Return 404 for unknown MovieLens IDs.
- Return 422 for schema validation failures.
- Return 401 for missing or invalid API key.
- Log server side errors with request ID.
- Keep response details short and safe.

## Future Improvements

- Add error code field.
- Add error documentation in API contract.
- Add structured error response model.
- Add more negative tests.