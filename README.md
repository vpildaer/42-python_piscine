# Python Piscine — 42 Belgium

A concept-by-concept summary across all eleven modules, in curriculum order. This is the
high-level index — for the seven modules with detailed bug-and-fix histories, a deeper
companion file already exists (referenced under each). For the four modules summarized
here for the first time (Growing Code, Garden Guardian, Data Quest, Data Archivist), the
key concepts are drawn directly from their subjects.

---

## P00 — Growing Code (Python Fundamentals Through Garden Data)

**Theme:** absolute basics — expressions, variables, functions, control flow, no classes yet.

- **Strict file-per-function discipline**: each exercise is *only* a function, no `if __name__ == "__main__":`, no top-level code, no calling the function in the file itself. A separate `main.py` helper imports and runs functions by exact name — reinforces that function *names* are a real contract, not just a style choice.
- `print()`, `input()`, `int()` — basic I/O and type conversion; input always arrives as `str` and must be explicitly converted.
- Simple arithmetic (rectangle area, summing three harvests) — no libraries, just expressions.
- Conditionals: strict vs. inclusive thresholds matter (`> 60` for harvest-ready, `> 2` for watering) — precise boundary reading is part of the exercise.
- Two equivalent approaches to repetition, required to produce **identical output**: iterative (`range()`-driven loop) vs. recursive (nested helper function, default parameter values, or a separate helper) — an early, concrete first exposure to "same result, different mechanism," foreshadowing FuncMage's closures/recursion much later.
- Type hints: optional (but recommended) for most exercises, **mandatory** starting at the module's final exercise — first exposure to writing and checking hints with `mypy`.
- `str.capitalize()` and other string methods introduced as the first taste of methods on built-in types.
- Exact function signatures matter mechanically here, not just stylistically — the grading/testing harness imports by exact name.

---

## P01 — Code Cultivation (Object-Oriented Garden Systems)

**Theme:** program structure fundamentals → foundational OOP (classes, inheritance, encapsulation).
*(Full detailed notes: `01_code_cultivation_notes.md`)*

- `if __name__ == "__main__":` and shebangs — why a file can be both a runnable script and a safely-importable module.
- `class`, `__init__`, `self`, instance vs. class variables — the shift from Growing Code's bare functions to objects holding their own state.
- Dunder methods (`__str__`), inheritance and `super()`, method/attribute name collisions.
- Encapsulation via the single-underscore convention (`_height`) plus `get_x()`/`set_x()` validation — Python's convention-based (not enforced) privacy.
- Multiple specialized subclasses (`Flower`, `Tree`, `Vegetable`) sharing a common base, overriding methods while reusing parent logic via `super()`.
- `@staticmethod` / `@classmethod`, nested classes for internal bookkeeping (per-instance stats tracking).
- Recurring practical bugs: `all()`/`any()` generator-expression scoping mistakes, `bool` being a subtype of `int`, trailing-separator string-building fixed by `str.join()`.

---

## P02 — Garden Guardian (Data Engineering for Smart Agriculture — Exception Handling)

**Theme:** `try`/`except`/`finally`, built-in exceptions, and designing your own exception hierarchies.

- `input_temperature()`-style validation functions: convert, then **raise** (not just print) when a value is out of range — the shift from "just report the problem" to "let the caller decide how to handle it."
- Catching **specific** exception types (`ValueError`, `ZeroDivisionError`, `FileNotFoundError`, `TypeError`) rather than a single bare `except:` — and catching **multiple types in one `try` block**, either via separate `except` clauses or a single tuple of types.
- A deliberately mypy-flagged `TypeError`-raising line (string + int concatenation) — a rare case where the subject explicitly wants a static-analysis warning left in place, because the exercise's whole point is exercising that failure mode at runtime.
- **Custom exception hierarchies**: `GardenError` as a base, `PlantError`/`WaterError` as subclasses — catching the base class transparently catches every subclass, which is the actual organizational payoff of inheriting from a shared custom base rather than bare `Exception` everywhere.
- Default messages on custom exceptions (supplying a fallback string in `__init__` if the caller doesn't provide one).
- `finally` — code that runs **regardless** of whether an exception occurred, used here for guaranteed resource cleanup ("closing the watering system") even when an earlier step failed and the function returns early.
- Overarching design principle repeated project-wide: **the program must never crash** — every failure mode needs a deliberate, graceful path back to normal execution.

---

## P03 — Data Quest (Mastering Python Collections)

**Theme:** the four core collection types, generators, and comprehensions — via a game-analytics theme.

- `sys.argv` — first real exposure to command-line arguments as a list of strings; first real use of `import` for something other than a same-project file.
- **Lists**: ordered, mutable — parsing scores from arguments, filtering invalid ones, computing `sum()`/`max()`/`min()`/average/range.
- **Tuples**: ordered, *immutable* — modeling fixed 3D coordinates, unpacking into named components, used because the data genuinely shouldn't change after creation.
- **Sets**: unordered, unique elements — `union()`/`intersection()`/`difference()` for comparing achievement collections across players; noticing that an empty set prints as `set()` (never `{}`, which Python reserves for an empty *dict*).
- **Dictionaries**: key-value pairs — parsing `key:value`-style command-line arguments into a validated inventory, `dict.keys()`/`values()`/`update()`, computing percentage-of-total per key, tie-breaking rules for "most/least abundant."
- **Generators**: `yield`, `typing.Generator`, `next()` — functions that produce values on demand instead of materializing a whole collection in memory; an *infinite* generator (`gen_event`) vs. a *finite, list-consuming* generator (`consume_event`) that shrinks a list as it yields, usable directly in a `for` loop.
- **Comprehensions** (list, dict, and — mentioned as also possible — set): capitalizing/filtering names in one line, building a scores dictionary and a derived "above-average" dictionary directly from a comprehension, without a manual loop.
- Foreword's real-world framing: choosing the *wrong* collection type (e.g., linear-scan lists for large-scale membership checks) is a genuine, historically-documented performance failure mode — "your data structure is your algorithm."

---

## P04 — Data Archivist (Digital Preservation — File Operations)

**Theme:** file I/O, from basic `open()`/`read()`/`write()` up to the `with` statement.

- `open()`, reading a file's full contents, `close()` — and explicitly handling `FileNotFoundError`/`PermissionError` as *expected*, common failure modes rather than crashes.
- `typing.IO`/`typing.TextIO` as the type hint for a file object — and the mypy quirk that `typing.IO` alone needs a type argument (`IO[str]`) or it errors as an incomplete generic.
- Writing new files — transforming read content (appending a character per line) and saving it, creating or overwriting as needed.
- `sys.stdin`/`sys.stdout`/`sys.stderr` as the three standard I/O "channels" — deliberately reading input *without* `input()`, and routing error messages specifically to **stderr** (with a distinguishing prefix) instead of mixing them into normal stdout output — a real separation-of-concerns technique used by real command-line tools.
- `flush()` — making sure buffered output is actually written out immediately, not just queued.
- The **`with` statement** (context manager) — deliberately withheld until the final exercise so its benefit is felt by contrast: automatic, guaranteed file closing even if an exception occurs mid-block, without needing a manual `finally: f.close()`.
- A function returning `(bool, str)` — success flag plus content-or-error-message — as an alternative to raising exceptions, letting the caller branch on the result without a `try/except` at the call site.

---

## P05 — Code Nexus (Polymorphic Data Streams — Abstract Classes & Polymorphism)

**Theme:** `ABC`, polymorphism, `Protocol`/duck typing, and building a genuinely pluggable pipeline.
*(Full detailed notes: `02_code_nexus_notes.md`)*

- `ABC` + `@abstractmethod` for defining a shared contract (`validate`/`ingest`/`output`) that every subclass must fulfill — concrete methods living in the base class only when logic is genuinely subclass-agnostic.
- Overriding with **narrower** parameter/return types than the abstract base declares — deliberate, common, and defensible, even though it can trigger stricter type-checker warnings.
- Polymorphism in practice: a router (`DataStream`) treating every registered processor uniformly through the shared interface, so adding a new data type never requires touching the router's own code.
- Hiding concrete implementation classes from a package's public surface via `__init__.py`, or — a stronger technique — nesting concrete classes inside the factory that produces them.
- `Protocol` (structural typing / duck typing) vs. `ABC` (nominal typing) — a plugin class matching a `Protocol`'s method shape counts as compatible without ever inheriting from it; used for interchangeable export plugins (CSV/JSON).
- FIFO "oldest first" extraction patterns (`pop(0)`, not `pop()`), and tracking an ever-incrementing rank counter that survives removals from the middle of a collection.
- `mypy` list invariance (`list[int]` vs. `list[int | float]` not being interchangeable) and the fix of annotating the variable explicitly at creation.

---

## P06 — The Codex (Mastering Python's Import Mysteries)

**Theme:** the "four sacred mysteries" — packages, import styles, absolute vs. relative imports, circular dependencies.
*(Full detailed notes: `03_the_codex_imports_notes.md`)*

- `import X` vs. `from X import Y` — namespace-object access vs. bare-name access, and when each is called for.
- `__init__.py` as a package's controllable "front door" — selectively exposing some names while leaving others unreachable from outside, a deliberate API-surface-control technique.
- Absolute imports (full path from project root) vs. relative imports (`.`/`..`, position relative to the *current file's* place in the package tree) — relative imports keep a package portable internally but cannot reach anything outside their own package hierarchy.
- Circular imports: the exact failure mechanism (module A pauses mid-load to load B, B tries to import from A's still-incomplete state), and three legitimate fixes — deferred/local imports, restructuring the dependency direction, or extracting a shared third module.
- `flake8`/`mypy` false-positives specific to `__init__.py` re-exports (`# noqa: F401`, `--strict`'s stricter re-export rules) — recognizing when a warning is a known, acceptable convention rather than a real bug.

---

## P07 — DataDeck (Abstract Card Architecture — Design Patterns)

**Theme:** Abstract Factory, capability mixins, and the Strategy pattern, applied together on one system.
*(Full detailed notes: `04_datadeck_notes.md`)*

- **Abstract Factory**: an abstract `CreatureFactory` with `create_base()`/`create_evolved()`, letting calling code request objects generically without ever importing or naming the concrete product classes.
- **Capability mixins**: `HealCapability`/`TransformCapability` inheriting only from `ABC` (deliberately *not* from the main `Creature` base), combined via multiple inheritance — separating "what a thing is" from "what a thing can do," reusable independent of any specific class hierarchy.
- Nesting concrete product classes *inside* their factory as a structural solution that simultaneously satisfies "don't expose concrete classes" and "let `mypy --strict` know the factory's exact return type."
- **Strategy pattern**: interchangeable `BattleStrategy` objects (`NormalStrategy`/`AggressiveStrategy`/`DefensiveStrategy`), each self-reporting compatibility via `is_valid()` before `act()` runs — keeping the orchestrating code free of any type-checking branches.
- Custom exceptions raised deliberately (not accidentally, via a stray `AttributeError`) for invalid strategy/creature combinations.
- Round-robin all-pairs iteration (`for i in range(n): for other in items[i+1:]`) for a tournament that pairs everyone with everyone else exactly once.

---

## P08 — The Matrix (Data Engineering for the Real World — Environments & Config)

**Theme:** virtual environments, pip vs. Poetry, and environment-variable-based configuration.
*(Full detailed notes: `05_the_matrix_notes.md`)*

- Detecting an active virtual environment via `sys.prefix` vs. `sys.base_prefix` (equal outside a venv, diverging inside one); `sys.executable` for the running interpreter's path; `site.getsitepackages()` for install location — with an awareness that this last call can itself be environment-dependent and worth guarding defensively.
- Why venvs exist at all: a real, hands-on encounter with a genuine version-conflict crash (mismatched numpy/matplotlib binary versions from a global install) as the concrete motivation.
- `pip` + `requirements.txt` vs. Poetry + `pyproject.toml` (`[tool.poetry]`, `[tool.poetry.dependencies]`, `[build-system]`, `package-mode = false` for a non-installable script) — reproducibility and dependency-resolution tradeoffs between the two tools.
- `importlib.util.find_spec()` (checks existence without importing) vs. `importlib.import_module()` (performs the real import, returns the actual module object) — and why only the *returned module object*, never the string name, has a real `.__version__`.
- Environment variables and `.env` files via `python-dotenv` — real OS-set variables naturally taking precedence over `.env`-file values because of load-order timing; `.env.example` (committed template) vs. `.env` (never committed, `.gitignore`d) and the concrete reasoning for why (permanent, often-shared Git history).

---

## P09 — Cosmic Data (Pydantic Models & Validation)

**Theme:** declarative data validation — `BaseModel`, `Field`, enums, custom cross-field rules, nested models.
*(Full detailed notes: `06_cosmic_data_pydantic_notes.md`)*

- `BaseModel` + `Field(...)` replacing hand-written `set_x()`/`isinstance()` validation from Code Cultivation with declarative type hints and constraints (`min_length`/`max_length` for strings, `ge`/`le` for numbers).
- `Optional[str]`/`str | None` (what types are acceptable) vs. `Field(default=...)` (whether a value must be supplied at all) — two genuinely separate concerns, easy to conflate, directly responsible for a real "field required" bug.
- Automatic type coercion (a well-formatted string handed to a `datetime` field gets parsed automatically) — more forgiving than manual `isinstance()` checks, while still strict about genuinely invalid input.
- Enums for fixed-choice fields, plus a `mypy --strict` nuance: pass the enum **member** itself into a constructor, not its unwrapped `.value` string.
- `@model_validator(mode='after')` (the current, non-deprecated way to do cross-field business-rule validation) — must be a plain instance method (not classmethod-style), must `return self`, and any `ValueError` raised inside gets wrapped by Pydantic into a structured `ValidationError` (with a `"Value error, "` prefix — safely stripped with `str.removeprefix`, never `str.lstrip`, which strips by character set and can silently over-strip).
- Nested models (`list[CrewMember]` inside `SpaceMission`) — validating the outer model unavoidably validates every nested model too, so one invalid nested item fails the whole outer construction, confirmed directly rather than just assumed.

---

## P10 — FuncMage (Functional Programming — Lambdas, Higher-Order Functions, Closures, `functools`, Decorators)

**Theme:** functions as first-class values — the most conceptually dense module of the piscine.
*(Full detailed notes: `07_funcmage_functional_programming_notes.md`, plus a concept-by-concept eval-prep doc: `08_funcmage_evaluation_prep.md`)*

- **Lambdas**: single-expression, nameless functions for short, throwaway logic passed directly to `sorted()`/`filter()`/`map()`/`max()`/`min()` — vs. `def` once logic needs a name, multiple statements, or reuse.
- **Higher-order functions**: functions that take or return other functions; composability emerges naturally when a returned function matches the *same signature* as its inputs, so outputs can freely feed back into other higher-order functions. `Callable` (from `collections.abc`, a type hint) vs. `callable()` (a runtime built-in check).
- **Closures** and `nonlocal`: an inner function remembering its enclosing scope after that scope has finished executing. `nonlocal` is required only for genuine *reassignment* (`x += 1`), never for merely reading a variable or mutating a mutable object's *contents* without rebinding its name — the exact distinction that separates `mage_counter` (needs it) from `memory_vault`'s dict-based storage (doesn't). `nonlocal` reaches one private, known enclosing scope; `global` reaches unprotected, shared, module-wide state — the real reason one is allowed and the other forbidden here.
- **`functools`**: `reduce` (general two-argument folding, more flexible than `sum()`) paired with the `operator` module's ready-made functions; `partial` for pre-filling some arguments and leaving others for later; `lru_cache` for memoization (recursive calls must go through the *decorated* function itself, or caching never applies to the recursive sub-calls); `singledispatch` for type-based branching without manual `isinstance()` chains.
- **Decorators**: structurally a higher-order function combined with a closure. `functools.wraps` preserves the original function's identity/metadata. Plain decorators need two nested function levels; **decorator factories** (needing their own configuration, like `min_power` or `max_attempts`) need three. `@staticmethod` for methods needing neither `self` nor `cls`.
- The module's sharpest recurring lesson: `mypy`/`flake8` verify types and style, **never logic** — several real, functioning-looking bugs here (an ignored parameter, a decorator silently reading an unrelated global variable by name coincidence, a test that accidentally exercised the wrong code path) passed both tools cleanly while still being completely wrong, and were only caught by actually running the code and reasoning about whether the output made sense.

---

## Cross-module throughlines

- **Static tools catch types/style, never intent.** From Code Cultivation's silent `all()`-generator bugs through FuncMage's global-shadowing bug, the recurring lesson across the *entire* piscine is that `mypy`/`flake8` passing cleanly is necessary but never sufficient — actually running the code and checking the output against your own reasoning is the only real test of correctness.
- **Encapsulation deepens progressively**: convention-based (`_attr`) in Code Cultivation → enforced via `ABC` contracts in Code Nexus → structural/duck-typed via `Protocol` → declarative via Pydantic's `Field` constraints — the same underlying goal (valid, well-shaped data) solved with increasingly powerful tools.
- **"Don't expose the concrete thing, only the interface"** recurs in three different disguises: `__init__.py` selective exposure (The Codex, DataDeck), `Protocol`-based duck typing (Code Nexus), and nested nested-class factories (DataDeck) — all the same underlying instinct applied differently depending on the constraint.
- **Graceful degradation over crashing** is an explicit, repeated requirement from Garden Guardian's "never crash" through The Matrix's "handle missing dependencies gracefully" through Pydantic's structured validation errors — the piscine consistently frames error handling as a design responsibility, not an afterthought.

