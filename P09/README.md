# Module Notes: Cosmic Data (Pydantic Models & Validation)

Core theme: **declarative data validation with Pydantic v2 — replacing hand-written `isinstance()`/`set_x()` checks with type-hint-driven, automatic validation.**

*Status: all three exercises complete, passing `mypy --strict` and `flake8`.*

---

## The core shift from earlier modules

In Code Cultivation, validation meant writing manual `set_height()`/`set_age()` methods with explicit `if value < 0: print(error)` checks. Pydantic replaces that entire pattern: you **declare** what a valid value looks like (type + constraints), and the library generates the constructor, the checks, and the error messages automatically. Same underlying goal (reject bad data), dramatically less boilerplate.

## `BaseModel`

- Inherit from `pydantic.BaseModel` instead of writing `__init__` yourself.
- Declare fields as class-level attributes with type hints — Pydantic auto-generates a validating constructor. Passing wrong types / out-of-range values raises `ValidationError` immediately at construction time.

## `Field(...)` — attaching constraints beyond a bare type hint

- A bare type hint (`crew_size: int`) only checks "is this an int at all." `Field()` attaches extra constraints.
- **Different keyword names for different field types** — don't assume one constraint vocabulary applies everywhere:
  - Strings: `min_length`, `max_length`
  - Numbers (`int`/`float`): `ge` (≥), `le` (≤) — also `gt`/`lt` for strict bounds
  - Lists/collections: `min_length`/`max_length` also apply (e.g. `crew: list[CrewMember] = Field(min_length=1, max_length=12)`)
- `Field(default=...)` gives a field a default value, making it optional to supply at construction.

## `Optional[str]` (or `str | None`) vs. `Field(default=...)` — two separate concerns, easy to conflate

- **`Optional[str]`** governs *what types are acceptable* — `str` or `None`.
- **`Field(default=...)`** governs *whether the field must be supplied at all* when constructing the object.
- **Real bug hit directly**: `notes: Optional[str] = Field(max_length=200)` — no `default=` — meant `notes` was still a *required* field (Pydantic error: `Field required [type=missing]`), even though the type allowed `None`. `Optional` alone does NOT make a field skippable.
- Fix: `Field(max_length=200, default=None)`. When declaring an `Optional` field, think about whether `None` (genuinely absent) or an empty value (`""`) is the more semantically honest default — they mean different things.

## Automatic type coercion

- Pydantic doesn't just check types — it often **converts** compatible input into the declared type. Passing a well-formatted string to a `datetime`-typed field gets automatically parsed into a real `datetime` object, rather than rejected for "wrong type."
- Different from the strict `isinstance()`-based manual validation used in earlier modules — Pydantic is more forgiving at the input boundary while still strict about genuinely invalid data.
- Worth testing directly (and being ready to explain at evaluation): pass a plain ISO-format string into a `datetime` field and confirm what type comes out on the other side.

## Enums for fixed-choice fields

- `from enum import Enum` — define a class with fixed named members (e.g. `ContactType.radio = "radio"`), then type a model field against that enum (`contact_type: ContactType`).
- Pydantic automatically rejects anything not matching one of the defined members — no manual `if value not in [...]` check needed.
- **mypy `--strict` gotcha**: passing `SomeEnum.member.value` (the *unwrapped raw string*) into a field typed as the enum itself is a real type mismatch under strict checking, even though Pydantic would often coerce a matching string into the enum member at runtime. Static type checking doesn't know about that runtime coercion — pass the **enum member itself** (`ContactType.radio`, not `.value`) to satisfy `--strict`.
- Access the underlying value for display purposes via `.value` (e.g. `member.rank.value` prints `"commander"`, not the enum repr).

## `@model_validator(mode='after')` — custom cross-field business rules

- Replaces the deprecated Pydantic v1 `@validator` decorator — v2 code should always use `@model_validator`.
- **`mode='after'` runs once all individual fields are already validated** — the method receives a plain **instance method signature**: just `self`, nothing else. **Deprecation trap hit directly**: writing `def validator(cls, self):` (classmethod-style, two params) triggers `PydanticDeprecatedSince212` — `mode='after'` validators must be plain instance methods now.
- **Must `return self`** at the end — omitting this breaks the returned object (Pydantic expects the validator to hand back the finalized instance).
- Return type hint: the class itself (e.g. `-> 'SpaceMission'`), not `None` — since you're genuinely returning `self`.
- Inside the validator, **raise `ValueError(...)`** for a failed business rule — Pydantic specifically catches `ValueError` raised inside validators and wraps it into its own structured `ValidationError`. (Worth confirming: does a custom exception class get this same automatic wrapping, or is `ValueError` specifically what Pydantic's internals look for? Check docs if unsure before an evaluator asks.)
- Use `@model_validator` for rules that need the **whole object at once**, or that depend on the **relationship between multiple fields** — anything a single-field `Field()` constraint can't express (a length bound is single-field; "physical contact must be verified" depends on two different fields together).

## Reading the structured error: `ValidationError.errors()`

- `ValidationError` isn't just a flat message — `.errors()` returns a **list of dicts**, one per failed field, each with keys like `'msg'`, `'loc'`, `'type'`, `'ctx'`.
- `e.errors()[0]['msg']` extracts just the first failure's message. Multiple fields can fail simultaneously — `[0]` only shows one; be aware of (and ready to explain) this limitation if a test case could trigger more than one violation at once.
- **`raise ValueError("your message")` inside a validator produces a `.msg` string prefixed with `"Value error, "`** (Pydantic's own generic label distinguishing a plain `ValueError` from one of its built-in constraint failures). To get back just the original message:
  - **Wrong tool, initially used**: `str.lstrip("Value error, ")` — `lstrip` strips a **character set**, not a literal substring. It happened to work on one specific message purely by luck (the next real character didn't collide with the strip-set), but would silently over-strip on a different message sharing letters with `"Value error, "`.
  - **Correct tool**: `str.removeprefix("Value error, ")` (Python 3.9+) — checks and removes the exact literal string as one unit, safe regardless of what follows.

## Nested models — validation cascades automatically

- A model field can be typed as a **list of another Pydantic model** (`crew: list[CrewMember]`). Each element is independently, fully validated.
- **Confirmed directly**: constructing the outer model (`SpaceMission`) requires validating every field, including the nested list — meaning each `CrewMember` inside must itself pass validation as an unavoidable part of validating the outer object. A single invalid nested member (e.g. `age=15` breaking `CrewMember`'s own constraint) causes the **entire outer construction to fail**, and this happens *before* the outer model's own `@model_validator` even runs (since `mode='after'` only fires once all fields, including nested ones, have already passed).
- This mirrors the nested-class technique from DataDeck (`Sproutling` inside `HealingCreatureFactory`), but for a different purpose — there it was about hiding a class from a package's public interface; here it's about modeling a genuine has-a relationship where each nested object carries independent validation.

## Iterating over nested lists inside a validator — syntax traps hit directly

- **Misplaced `for` clause bug**, encountered twice in the same file:
  ```python
  # WRONG — the `for` sits outside the function call, making the whole
  # parenthesized expression a generator object, not the intended result
  if not (any(...) or any(...) for member in self.crew):
  sum(member.years_experience >= 5) for member in self.crew  # same bug
  ```
  The fix is making sure `for member in self.crew` sits **inside** the single aggregating call it belongs to:
  ```python
  if not any(member.rank == Rank.commander or member.rank == Rank.captain
             for member in self.crew):

  if sum(member.years_experience >= 5 for member in self.crew) < len(self.crew) / 2:
  ```
- `any(condition for item in iterable)` — "at least one satisfies." `sum(condition for item in iterable)` — counts how many satisfy (booleans act as `1`/`0` in arithmetic context) — a clean idiom for "at least N%" business rules.
- Comparing a bare generator object against a number (e.g. `generator < some_float`) raises `TypeError: '<' not supported between instances of 'generator' and 'float'` — a strong signal the `for` clause is in the wrong place if this error appears.

## Practical evaluation-prep habits from this module

- Test the two things the subject explicitly flags as "Think About" prompts *before* the evaluation, don't just reason about them abstractly: (1) passing a string into a `datetime` field, observing the coercion; (2) constructing an outer model with one deliberately-invalid nested model, observing exactly when/how it fails.
- A deprecation warning is worth reading fully and fixing at the root cause, not suppressing — the classmethod-vs-instance-method validator signature issue was a genuine, correctly-diagnosed bug, not noise.
- When an outer `try/except` around a function that already internally handles its own exception looks "unreachable" — that's not automatically a bug. It can be a deliberate defensive choice (e.g. protecting against an evaluator modifying inputs live during a defense) as long as you can articulate why you kept it.

