# Failure Taxonomy – Text Risk Scoring Service

This document enumerates all known and anticipated failure modes in the
Text Risk Scoring Service and defines how each is handled in a
deterministic, safe, and contract-compliant manner.

The goal of this taxonomy is to ensure that the service never crashes,
never produces undefined behavior, and always returns a structured,
predictable response under all conditions.

---

## Design Principles

- Same input always produces the same output (determinism)
- No unhandled exceptions
- All failures are converted into structured responses
- Resource usage is bounded
- Behavior is explicit and documented

---

## F-01: Empty Input

**Cause:**  
The input text is an empty string or contains only whitespace.

**Risk:**  
No meaningful content is available for analysis, and downstream logic
could behave unpredictably.

**Handling Strategy:**  
- Detect empty input after normalization
- Return a structured error response
- No scoring is attempted

**Response Behavior:**  
- risk_score = 0.0  
- risk_category = LOW  
- trigger_reasons = []  
- errors.error_code = `EMPTY_INPUT`

**Why This Is Safe:**  
Prevents unnecessary processing and guarantees predictable behavior for
invalid but common user input.

---

## F-02: Invalid Input Type

**Cause:**  
The input is not a string (e.g., null, number, object, array).

**Risk:**  
String operations such as normalization and matching would raise runtime
exceptions.

**Handling Strategy:**  
- Validate input type at the engine boundary
- Reject non-string inputs immediately

**Response Behavior:**  
- risk_score = 0.0  
- risk_category = LOW  
- trigger_reasons = []  
- errors.error_code = `INVALID_TYPE`

**Why This Is Safe:**  
Enforces strict API contracts and prevents runtime crashes caused by
unexpected input types.

---

## F-03: Excessively Long Input

**Cause:**  
Input text exceeds the maximum allowed length.

**Risk:**  
Potential performance degradation or denial-of-service behavior due to
unbounded processing.

**Handling Strategy:**  
- Truncate input deterministically to a fixed maximum length
- Continue analysis on the truncated text
- Record truncation as an explicit reason

**Response Behavior:**  
- Analysis performed on truncated text
- "Input text was truncated to safe maximum length" added to trigger_reasons

**Why This Is Safe:**  
Ensures bounded resource usage while preserving deterministic behavior.

---

## F-04: Keyword Saturation (Score Explosion)

**Cause:**  
A large number of risk keywords appear in the input, especially within a
single category.

**Risk:**  
Unbounded score growth leading to meaningless or exaggerated risk
classification.

**Handling Strategy:**  
- Apply per-category score caps
- Limit total score to a maximum of 1.0

**Response Behavior:**  
- Category score is clamped to a defined maximum
- Overall risk_score is normalized and capped

**Why This Is Safe:**  
Prevents runaway scoring and preserves meaningful category thresholds.

---

## F-05: Substring False Positives

**Cause:**  
Naive substring matching causes false positives  
(e.g., "die" matching inside "studies").

**Risk:**  
Incorrect risk detection and inflated risk scores.

**Handling Strategy:**  
- Use regex-based word-boundary matching
- Ensure only whole-word or explicit phrase matches are detected

**Response Behavior:**  
- Only valid keyword matches contribute to scoring
- No false-positive triggers from partial matches

**Why This Is Safe:**  
Preserves semantic integrity of keyword detection and improves reliability.

---

## F-06: Score Overflow or Drift

**Cause:**  
Accumulated scores exceed the intended numeric range due to repeated
detections across categories.

**Risk:**  
Risk category thresholds become meaningless.

**Handling Strategy:**  
- Clamp total score to the range [0.0, 1.0]
- Apply deterministic threshold logic

**Response Behavior:**  
- risk_score always ∈ [0.0, 1.0]
- risk_category derived consistently from score

**Why This Is Safe:**  
Maintains stable and interpretable scoring semantics.

---

## F-07: Unexpected Runtime Exception

**Cause:**  
Unexpected errors during processing (e.g., regex failure, internal bug).

**Risk:**  
Service crash or undefined behavior.

**Handling Strategy:**  
- Wrap entire analysis pipeline in a global try/except block
- Convert any unexpected exception into a structured error response
- Do not expose stack traces

**Response Behavior:**  
- risk_score = 0.0  
- risk_category = LOW  
- trigger_reasons = []  
- errors.error_code = `INTERNAL_ERROR`

**Why This Is Safe:**  
Guarantees system availability and prevents crashes under all conditions.

---

## F-08: Determinism Violation

**Cause:**  
Non-deterministic logic such as randomness, time-based decisions, or
unordered processing.

**Risk:**  
Same input producing different outputs across executions.

**Handling Strategy:**  
- No randomness used anywhere in the engine
- Fixed thresholds, weights, and processing order
- Determinism validated through tests

**Response Behavior:**  
- Identical inputs always produce identical outputs

**Why This Is Safe:**  
Ensures reproducibility, testability, and demo reliability.

---

## Summary

This failure taxonomy demonstrates that the Text Risk Scoring Service:

- Anticipates failure instead of reacting to it
- Converts all failures into structured, predictable responses
- Never crashes or produces undefined behavior
- Preserves deterministic guarantees under stress and edge cases

This document serves as the authoritative reference for failure handling
behavior in the system.
