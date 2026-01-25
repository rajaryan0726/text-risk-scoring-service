# Text Risk Scoring Service – Contracts

## Input Schema
{
  "text": "string (required, max 5000 chars)"
}

## Output Schema
{
  "risk_score": "float (0–1)",
  "risk_category": "LOW | MEDIUM | HIGH",
  "trigger_reasons": ["string"],
  "processed_length": "int",
  "errors": null | object
}

## Error Schema
{
  "error_code": "EMPTY_INPUT | INVALID_TYPE | TOO_LONG",
  "message": "string"
}

## Guarantees
- Service never crashes
- Always returns structured response
- Same input produces same output

## Edge Case Behavior

The service guarantees safe, deterministic behavior under the following edge conditions.

### Empty or Whitespace Input
- Input: empty string or whitespace-only string
- Behavior:
  - risk_score = 0.0
  - risk_category = LOW
  - trigger_reasons = []
  - errors = { error_code: "EMPTY_INPUT", message: "Input text is empty" }

### Extremely Long Input
- Input length exceeding MAX_LENGTH (e.g., 10,000 characters)
- Behavior:
  - Input is truncated to MAX_LENGTH
  - Truncated text is analyzed
  - No exception is raised

### Non-String Input
- Input where `text` is not a string
- Behavior:
  - Analysis is skipped
  - Structured error response is returned
  - System does not crash

### No Risk Indicators Detected
- Input contains no known risk keywords
- Behavior:
  - risk_score = 0.0
  - risk_category = LOW
  - trigger_reasons = []

### Excessive Risk Indicators
- Input contains many repeated or overlapping risk keywords
- Behavior:
  - Risk score is capped at 1.0
  - Deterministic category assignment
  - No overflow or instability

### Internal Processing Errors
- Unexpected runtime exception
- Behavior:
  - Exception is caught
  - Safe error response is returned
  - No internal details are exposed
