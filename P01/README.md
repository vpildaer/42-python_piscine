# Module Notes: Code Cultivation (Object-Oriented Garden Systems)

Core theme: **foundations of Python program structure and basic OOP.**

---

## `if __name__ == "__main__":`

- Every Python file has a `__name__` variable, auto-set by Python:
  - `"__main__"` when the file is run directly (`python3 script.py`)
  - the module's own name when the file is **imported** elsewhere
- The guard lets a file be **both** a reusable module *and* a standalone script:
  code inside the guard only runs when the file is executed directly, never when imported.
- Without it, importing a file re-runs all its top-level code (prints, test calls, etc.) as a side effect — polluting output and potentially causing bugs.
- Convention: put your "exports" (functions/classes) at module level, and your test/demo code inside the guard.

## Shebangs (`#!/usr/bin/env python3`)

- `#!` at the very top of a file tells the OS which interpreter to run the script with.
- `#!/usr/bin/python3` — hardcoded path, not portable across systems.
- `#!/usr/bin/env python3` — **preferred**: uses `env` to find `python3` wherever it lives on the current system's `PATH`. Portable across macOS/Linux.
- Requires `chmod +x script.py` to actually be executable as `./script.py`.

## Classes — basics

- A class is a **blueprint**; instances are created from it.
- `__init__(self, ...)` — constructor, runs automatically on instantiation, sets up instance attributes via `self.attr = value`.
- `self` — always the first parameter of instance methods; refers to the specific instance the method is being called on.
- **Instance variables** (`self.x = ...`) — unique per object.
- **Class variables** (declared directly in the class body) — shared across all instances of that class.

## Dunder (magic) methods

- Exactly **two underscores on each side** — `__str__`, not `__str___` or `__init___`. A single typo silently breaks the special behavior (Python just treats it as a normal, unused method).
- `__str__(self) -> str` — defines what `print(obj)` / `str(obj)` displays. Prefer this over a custom `show()` method — it's the idiomatic Python way.
- `__repr__`, `__len__`, `__eq__`, `__lt__` — other common dunders for developer-facing repr, `len()`, `==`, `<`, etc.

## Method / attribute name collisions

- Don't name a method the same as an attribute (e.g. an `age` attribute *and* an `age()` method) — the method becomes unreachable, since the attribute shadows it. Use distinct names (`add_day()` instead of `age()`).

## Instance behavior via inheritance vs. per-instance parameters

Two ways to give objects different behavior:
1. **Instance-based**: pass a value (e.g. `growth_rate`) into `__init__`, store it per-instance. Simple, flexible.
2. **Inheritance-based**: each subclass overrides a class-level attribute or method (e.g. `Rose.growth_rate = 0.8` vs `Cactus.growth_rate = 0.2`). More idiomatic OOP when behavior is tied to *type/species*, not just a random parameter — enables `isinstance()` checks, shared logic in the base class, and natural extension (new subclass = new behavior, no existing code touched).

## `super()`

- `super().__init__(...)` calls the **parent class's constructor** — must include `.__init__(...)`, not just `super(...)`.
- Lets a subclass extend (not just replace) the parent's setup logic.
- Also usable in overridden methods generally: `super().method()` calls the parent's version, letting you *extend* rather than fully replace behavior (e.g. `super().show()` then print extra subclass-specific info).

## Encapsulation (protected convention)

- Python has no true "private" attributes — convention only: prefix with a single underscore (`self._height`) to signal "internal, don't touch directly."
- Pair with `get_x()` / `set_x()` methods that validate before allowing changes (e.g. rejecting negative heights).
- This is **convention-based protection**, not enforced by the language (unlike `private` in other languages).

## Inheritance & `super()` with multiple subclasses

- Common base class holds shared attributes/methods (`Plant`: name, height, age, `show()`/`__str__`).
- Subclasses (`Flower`, `Tree`, `Vegetable`) inherit shared behavior, add their own attributes, and **override** methods when they need extra behavior — calling `super().method()` first to reuse the parent's logic, then adding their own bit.
- **Overriding methods vs. adding new ones**: if the subject says "modify behavior of `grow()`/`age()` for this subclass," override those exact methods (don't invent a new method name like `grow_and_age()`) — this preserves the shared interface so *any* code that calls `.grow()` on *any* Plant subclass gets the right specialized behavior automatically (polymorphism payoff).

## Static & class methods (later exercises)

- `@staticmethod` — a method that doesn't need `self` or the class itself; behaves like a plain function namespaced inside the class.
- `@classmethod` — receives the class itself (`cls`) instead of an instance; useful for alternate constructors (e.g. "create an anonymous/default instance").

## Nested classes

- A class can be defined **inside** another class's body (used later for internal statistics tracking, e.g. a `Plant`'s private stats-tracking nested class). Useful for tightly-scoped helper structures that only make sense in the context of their outer class.

## try/except patterns

- `try: risky_call() / except SpecificError: handle()` — catch the *specific* exception type you expect (`ValueError` for bad `int()`/`float()` conversion), not a bare `except:` or overly broad `except Exception:` unless deliberate.
- **Conditions never go in `except` clauses** — `except x > 0:` is invalid syntax. Range/logic validation belongs in `if`/`elif`, *after* the risky conversion succeeds.
- `raise Exception(f"...")` — remember the `f` prefix for interpolation; a plain string literal won't substitute variables.
- Recursion is a poor tool for **input-validation retry loops** (stack builds up, no clean early exit). Prefer `while True:` + `continue`/`break` for "keep asking until valid."
- **Global flag + `for` loop** pattern for validating multiple items where *any* failure invalidates the whole batch:
  ```python
  valid = True
  for item in items:
      try:
          ...
      except ValueError:
          valid = False
          break
  if valid:
      return result
  ```
  (A `continue` inside a `for` loop only skips to the next iteration — it does NOT retry an outer `while` loop. This is a common source of bugs when validating multi-part input.)

## File I/O

- `open(file, "r")` returns a file object; type hint as `typing.IO[str]` (or `typing.TextIO`) — `typing.IO` alone is a generic type and needs a type argument (`IO[str]` for text, `IO[bytes]` for binary) or mypy will error (`Missing type arguments for generic type "IO"`).
- Prefer **wrapping the entire read/use/close sequence** inside the `try` block, not just the `open()` call — any error during reading (not just opening) needs to be caught too, or the program crashes with an uncaught exception (exit code 1) even though the file opened fine.
- Programs expected to "never crash" should exit with code `0` even on handled errors — don't call `sys.exit(1)` for gracefully-handled cases; just `return`/let the script end normally after printing the error message.
- Context managers (`with open(...) as f:`) auto-close files — cleaner than manual `f.close()`, and safe even if an exception occurs mid-block.

## List/dict comprehension idioms used throughout

- `all(condition for item in iterable)` — "every item satisfies condition." Empty iterable → vacuously `True`.
- `any(condition for item in iterable)` — "at least one item satisfies condition." Empty iterable → `False`.
- **Common bug**: writing `all(isinstance(data, X) for elem in data)` — checking the wrong variable (the whole collection instead of each element) inside the generator. Always double check the generator body references the loop variable, not the outer collection.
- Nested `all(all(...) for elem in data)` needed when validating "every element passes an *internal* all-check" (e.g. checking every key/value pair inside every dict in a list) — a single-level `all()` wrapping a generator of generators is a bug, since a generator object is always truthy regardless of its contents.

## `bool` is a subclass of `int`

- `isinstance(True, int)` → `True`. If you need to exclude booleans from a numeric check, add an explicit `and not isinstance(x, bool)`.

## `join()` for building strings — avoiding trailing separators

- Manual loop + `string += item + separator` always leaves a trailing separator after the last item.
- `separator.join(list_of_strings)` inserts the separator **only between** elements — no trailing artifact, no special-casing the last item.
- Build a list of formatted pieces first, then join once at the end — this pattern recurs constantly (CSV rows, JSON-like strings, log entries combining dict values with `": ".join(d.values())`).
