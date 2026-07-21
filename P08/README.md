# Module Notes: The Matrix (Welcome to the Real World of Data Engineering)

Core theme: **professional project hygiene — isolating environments, managing dependencies reproducibly, and externalizing configuration/secrets.**

*Status: ex0 and ex1 fully implemented and debugged. Ex2 discussed conceptually, not yet coded.*

---

## The three-layer "onion" this module builds

1. **Isolate** where packages live → virtual environments (ex0)
2. **Declare & manage** what packages are needed, reproducibly → pip vs. Poetry (ex1)
3. **Configure** behavior/secrets without hardcoding them → environment variables / `.env` (ex2)

---

## Ex0 — Virtual environment detection (`construct.py`)

### The core technique
- `sys.prefix` — path to the Python installation **currently in use** by the running process.
- `sys.base_prefix` — path to the **real, underlying** installation, regardless of venv status.
- **No venv active** → the two are equal (same installation).
- **Venv active** → they diverge: `sys.prefix` points into the venv folder, `sys.base_prefix` points to the real system install.
- Standard detection: `sys.prefix != sys.base_prefix` → `True` means "in a venv."
- **Naming gotcha**: double check what your boolean variable's name actually implies vs. what the comparison evaluates to — `is_venv = (sys.prefix == sys.base_prefix)` is backwards-named (it's actually true when *not* in a venv) even if the branches using it are still logically correct. Misleading names cause real confusion later even when the logic itself works.

### Useful values/functions
- `sys.executable` — full path to the currently-running interpreter binary (different from `sys.prefix`, which is a directory, not the binary itself).
- `os.path.basename(path)` — cleanly extracts just the last path component (e.g. the venv folder's own name) from a full path. Preferred over `os.path.split(path)` when you only need one side of the split (`split` returns a 2-tuple; mismatching that against a `str` type hint is a real mypy error).
- `site.getsitepackages()` — returns the path(s) where `pip install` would place packages for the current interpreter; differs automatically based on venv-vs-global context. Can raise `AttributeError` in some virtualenv setups where this function isn't available — worth guarding with `except AttributeError`, not a bare `except Exception`, since you know the specific likely failure mode.

### String/escape gotcha
- `\a` inside a normal (non-raw) string is the **bell/alert control character**, not literal backslash-a — a real trap when printing a path like `matrix_env\Scripts\activate`. Fix with a **raw string** (`r"..."`), but remember raw strings don't process `\n` as a newline either — so don't try to end a raw string with `\n` expecting an actual line break; use a separate `print()` call instead.

### Structural notes
- Simple `if/else` branching on the one boolean check, printing an entirely different block of text for each scenario, wrapped in `if __name__ == "__main__":`.
- `importlib`/`site` calls here are all reliably available on every standard interpreter — the one line worth defensively wrapping is `site.getsitepackages()`, given its known cross-environment inconsistency.

---

## Ex1 — Dependency management: pip vs. Poetry (`loading.py`)

### Checking dependency availability without crashing
- `import importlib.util` (importing bare `importlib` does **not** automatically expose `importlib.util` — submodules of a package aren't auto-loaded just because the parent package was imported; must import the submodule explicitly).
- `importlib.util.find_spec("pandas")` — checks *whether a module exists/is importable* without actually importing it. Returns `None` if not found, a `ModuleSpec` object if found. **Does not give you the module itself** — a spec is metadata, not the loaded module; you can't read `.__version__` off a spec.
- `importlib.import_module("pandas")` — performs the **real** import, and **returns the actual module object** — this is what you call `.__version__` on. Common bug: calling `.__version__` on the *string name* you're iterating over (`k.__version__`) instead of on the object returned by `import_module` — strings don't have version numbers.
- Catching failures broadly enough: `ModuleNotFoundError` only covers "genuinely not installed." A package that **is** installed but broken/incompatible (e.g. a numpy/matplotlib ABI version mismatch) raises `ImportError`/`AttributeError` instead — `ModuleNotFoundError` is actually a *subclass* of `ImportError`, so catching `ImportError` covers both "not found" and "found but broken." Worth catching multiple specific exception types here rather than one narrow type, given real installed-but-broken scenarios happen in practice (encountered directly: a numpy 2.x / matplotlib-built-for-numpy-1.x conflict from mixing global installs).
- **This is a direct real-world illustration of why venvs (ex0) matter**: installing packages globally/system-wide, at different times, risks exactly this kind of binary incompatibility between interdependent packages. A fresh venv + a single `pip install -r requirements.txt` resolves compatible versions together, avoiding this class of bug entirely.

### `sys.modules` caching — why split "checking" from "using" is safe
- Once a module has been imported anywhere in the running process (e.g. during your dependency-check loop), it's cached in `sys.modules`. A later, completely separate function doing a normal `import pandas as pd` doesn't re-run any setup cost — it just retrieves the already-cached module reference.
- This means it's clean and safe to have one function purely responsible for **checking/reporting** availability (using `importlib.util`/`importlib.import_module` machinery), and a **separate** function responsible for the **real work**, using plain, ordinary top-level-style imports — without worrying about "wasting" an import or triggering anything twice.
- The subject's explicit note *"flake8 and mypy errors are allowed for this exercise, only for import errors"* is a signal that plain top-level imports inside your real logic are expected/fine — the `importlib` machinery is specifically for the graceful-detection phase, not meant to wrap every single import in the file.

### numpy — data generation
- Subject requirement: **numpy must be the actual source of the dataset** — not `range()`, not a hardcoded list.
- `numpy.random.randint(low, high, size=n)` -> uniform distribution (every value equally likely) — visually boring/flat as a histogram.
- `numpy.random.normal(loc=mean, scale=stddev, size=n)` -> Gaussian/bell-curve distribution — produces a much more meaningful "distribution" visualization. Note: unlike `randint`, values aren't hard-bounded, so they can technically exceed your intended range slightly; `numpy.clip(data, low, high)` can enforce a hard range if that matters for your labeling.
- Type-hinting a numpy array: `numpy.typing.NDArray` (from `numpy import typing`) — a plain `list[int]` annotation is incorrect and misleading, since `numpy.random.*` functions return `numpy.ndarray`, not a Python `list`.

### pandas / matplotlib
- Wrapping a numpy array in `pandas.DataFrame(data)` gives you data-manipulation capability (`.describe()`, etc.) with minimal code — satisfies "uses pandas for data manipulation" even without deep analysis.
- `pyplot.hist(data, bins=n, ...)` is the natural chart type for showing a **distribution** shape — a default `.plot()` (line plot) on sequential data shows values in sample order, which doesn't actually represent "distribution" meaningfully; worth matching the chart type to what you're semantically claiming to show.
- **Order matters between `savefig()` and `show()`**: some matplotlib backends can clear/reset figure state once an interactive window (`show()`) is closed. Calling `savefig()` *before* `show()` guarantees the file captures the fully-intact figure regardless of what happens during/after the interactive display step.

### `pyproject.toml` for Poetry — minimal correct structure
```toml
[tool.poetry]
name = "..."
version = "0.1.0"
description = "..."
authors = ["..."]
package-mode = false   # true package-building not needed for a standalone script

[tool.poetry.dependencies]
python = "^3.10"       # Poetry always requires an explicit python constraint
pandas = ">=2.1.0"
numpy = ">=1.25.0"
matplotlib = ">=3.7.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```
- **`package-mode = false`** — tells Poetry "just manage dependencies for a script, don't try to build/install this as a distributable package" (which is the default assumption otherwise, and would expect a matching package folder structure that doesn't exist here).
- Don't mix the modern PEP 621 `[project]` table with `[tool.poetry]` — pick one convention consistently; Poetry's traditional convention keeps dependencies inside `[tool.poetry.dependencies]`.
- `[build-system]` is required boilerplate, largely copy-paste, but necessary for the file to be considered valid/buildable by tooling.

### `KeyboardInterrupt` vs. `Exception`
- `KeyboardInterrupt` inherits from `BaseException` directly, **not** from `Exception`. This means `except Exception:` genuinely will not catch it — a separate `except KeyboardInterrupt:` clause is needed (and works correctly) to handle it distinctly, e.g. when a user interrupts a blocking `plt.show()` window wait.
- Worth being cautious about a broad top-level `except Exception as e: print(e)` wrapping your whole `__main__` block — it silently swallows *any* unexpected bug with just a one-line message, which can mask real problems during development/evaluation rather than surfacing a full traceback. More specific, narrower exception handling closer to where an error can actually occur is generally more debuggable than one broad catch-all at the very top.

---

## Ex2 — Environment variables & secrets (`oracle.py`) — conceptual notes so far

### `python-dotenv`
- Library's job: load `KEY=VALUE` lines from a `.env` file **directly into `os.environ`**, the same place real OS-level environment variables live. Code downstream reads `os.getenv("KEY")` uniformly — it doesn't need to know or care whether the value came from a real environment variable or from the `.env` file.
- Call the loading function once, early, before reading any config values.

### The five required variables
`MATRIX_MODE`, `DATABASE_URL`, `API_KEY`, `LOG_LEVEL`, `ZION_ENDPOINT` — each read via `os.getenv(...)`, with a deliberate decision per-variable about whether a default/fallback makes sense, or whether a missing value should be flagged as a real problem (not crash, but clearly reported — same "graceful degradation" spirit as ex1's missing-dependency handling).

### Dev vs. prod distinction
- Deliberately open-ended in the subject — just needs to be **visibly different** in output based on `MATRIX_MODE`. Options: stricter validation in production (e.g. refuse to start without a real `API_KEY`), different verbosity tied to `LOG_LEVEL`, or a clear mode-dependent summary line.

### Precedence: real env vars over `.env` file
- Real OS environment variables set **before** the script runs (e.g. `MATRIX_MODE=production python3 oracle.py`) are already present in `os.environ` by the time the dotenv-loading function runs. Many dotenv implementations deliberately **do not override** already-set variables — meaning real environment variables naturally "win" over `.env` file values, without needing to write explicit override-priority logic yourself. Worth testing this behavior directly to confirm rather than assuming.

### `.env.example` vs. `.env`
- `.env.example` — **committed**, template only, placeholder/fake values, tells other developers what variables exist.
- `.env` — **never committed**, real local values, excluded via `.gitignore`.

### Why `.env` must be gitignored — the actual reasoning to articulate
- Git history is effectively permanent and often shared. A secret committed once remains recoverable from history even after a later commit deletes the file, unless history itself is rewritten (disruptive, not always fully effective once cloned/forked elsewhere). Never committing the real file avoids the exposure at the source, rather than needing cleanup after the fact.
- In production, real values are typically set directly as environment variables by the hosting platform — no `.env` file needs to exist there at all, which is inherently more secure than shipping a config file containing real secrets.

### To fill in once ex2 is actually implemented
- [ ] Final structure of the "environment security check" section — what each of the three checks concretely verifies
- [ ] Specific dev/prod behavioral difference chosen
- [ ] Confirmed precedence behavior (env var vs. `.env`) via direct testing
- [ ] Final `.gitignore` contents (Python artifacts + `.env`)

