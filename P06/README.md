# Module Notes: The Codex (Mastering Python's Import Mysteries)

Core theme: **how Python's import system actually works — packages, absolute vs. relative imports, and circular dependencies.**

---

## `import X` vs `from X import Y`

- **`import X`** — imports the whole module as a namespace object. Access everything with a prefix: `X.thing()`. Keeps origin explicit in code (`elements.create_fire()` — obviously came from `elements`).
- **`from X import Y`** — pulls a specific name directly into the current namespace. Access it bare: `Y()`. More concise, but loses the "where did this come from" clarity, and risks naming collisions between modules.
- Both are valid, "correct" styles — chosen based on what a script/exercise specifically demonstrates, not a strict rule about which is "better."

## Packages and `__init__.py`

- A folder becomes an **importable package** only when it contains `__init__.py` (even empty).
- `__init__.py` is the package's "front door" — runs once, on first import of the package. Anything it explicitly imports becomes accessible as `package.thing`.
- **Selective exposure**: if `__init__.py` imports `create_air` but never imports `create_earth`, then `package.create_air()` works, but `package.create_earth()` raises `AttributeError` — even though `create_earth` is defined in a file *inside* the package. This is a deliberate, common pattern for controlling a public API surface (hide internals, expose only what's meant to be public).
- Reaching a file `folder/sub.py` **directly** (bypassing `__init__.py` entirely): `import folder.sub` (dotted path mirrors the folder path, `/` → `.`, drop `.py`), then reference as `folder.sub.thing()`.

## Absolute vs. relative imports

- **Absolute import**: full path from the project's top level, e.g. `from elements import create_fire` — always resolves relative to the program's entry point/root, regardless of which file does the importing.
- **Relative import**: `.`/`..` dots describe a path *relative to the current file's position in the package hierarchy*.
  - `.` = same package as the current file (e.g. `from .elements import create_earth` inside `alchemy/potions.py`, reaching `alchemy/elements.py`).
  - `..` = go up one level to the parent package, then resolve from there (e.g. `from ..potions import strength_potion` inside `alchemy/transmutation/recipes.py`, reaching `alchemy/potions.py`).
- **`..` beyond the top-level package** → `ImportError: attempted relative import beyond top-level package`. Relative imports only work *within* a package's own hierarchy — they can't reach something that isn't part of that package tree at all (e.g. a standalone top-level `elements.py` sitting outside `alchemy/` entirely needs an **absolute** import, not relative dots, regardless of how many dots you add).
- **When to use which**: relative imports keep a self-contained package portable (if you move/rename the whole package folder, internal relative references still work unchanged). Absolute imports are necessary — and often preferred by convention/PEP 8 as the more explicit default — for anything reaching outside the current package, or for top-level project structure in general.

## Circular imports

- **The trap**: Module A imports something from Module B at the top of the file; Module B imports something from Module A at the top of *its* file. Loading A pauses to load B; B tries to import from A, but A is only **partially initialized** (execution paused at the very import line that triggered B's load) — the needed name doesn't exist in A yet → `ImportError: cannot import name 'x' from partially initialized module ...(most likely due to a circular import)`.
- **Fix 1 — deferred/local import**: move the import from the top of the file into the *body of the function* that actually needs it. Since a function body doesn't execute until the function is *called* (not when the module is first loaded/defined), by the time the import actually runs, both modules have already finished loading — breaking the cycle.
- **Fix 2 — restructure dependencies**: eliminate the need for one of the two directions entirely — e.g., pass required data as a **function parameter** instead of importing it directly, so only one module needs to know about the other.
- **Fix 3 — shared third module**: extract the shared piece (e.g. a constants list) into its own file that both original modules import from independently, without needing each other.
- Multiple valid fixes exist — pick one, but be ready to explain the others conceptually (this is a common evaluation question).

## Nested packages, deep dotted imports

- A file 3 levels deep (`alchemy/transmutation/recipes.py`) can be reached directly via `import alchemy.transmutation.recipes`, referenced afterward via the full dotted path, or aliased on import (`import alchemy.transmutation.recipes as recipes`) for shorter references afterward.
- Each intermediate folder in a nested package structure needs its own `__init__.py` to be recognized as a package at all.

## `flake8` / `mypy` quirks specific to `__init__.py`

- **`F401 'X' imported but unused`**: extremely common false-positive in `__init__.py` files — you import something there *specifically* so other files can reach it via the package namespace, not because `__init__.py` itself uses it. Suppress deliberately with `# noqa: F401` on each such line — this is the accepted convention, not a workaround to be embarrassed about.
- **`mypy --strict` "does not explicitly export attribute"**: similar false-positive — strict mode wants an explicit re-export marker (`as name`, or `__all__`) for names imported via `from .module import name` inside `__init__.py`. Plain `mypy` (non-strict) typically doesn't flag this. Worth checking whether the project explicitly requires `--strict` before treating this as a real problem to fix.
- A **deliberately unreachable name** (e.g. testing that `create_earth` correctly raises `AttributeError` when accessed via the package) will *also* trigger a real, intentional mypy error — expected and correct, not a bug to fix.

## PEP 8 formatting notes picked up here

- `E302 expected 2 blank lines, found 0` — top-level function/class definitions need 2 blank lines before/after, consistently, across a whole file.
