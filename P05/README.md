# Module Notes: Code Nexus (Polymorphic Data Streams in the Digital Matrix)

Core theme: **abstract base classes, polymorphism, and duck typing via `Protocol`.**

---

## `ABC` and `@abstractmethod`

- `from abc import ABC, abstractmethod`
- A class inheriting from `ABC` becomes an **abstract base class** — it defines a *contract* other classes must fulfill.
- `@abstractmethod` methods have no real implementation (`pass`) in the base class — **every subclass must override them**, or Python refuses to instantiate that subclass at all (`TypeError: Can't instantiate abstract class X with abstract method y`).
- A **concrete method** (no `@abstractmethod`) can still live in the ABC — used when the logic is identical for every subclass and doesn't need to be overridden (e.g. an `output()` method that just manipulates already-normalized internal string data, regardless of which subclass produced it).
- **Rule of thumb for what's abstract vs. concrete**: if the *behavior* genuinely differs per subclass (validating/ingesting different data types) → abstract. If the logic is subclass-agnostic once data reaches a common internal format → concrete, lives once in the base.

## Overriding with narrower signatures

- Abstract method in base: `def ingest(self, data: Any) -> None` — must accept anything, since the base class can't know what specific type each subclass wants.
- Concrete override in subclass: `def ingest(self, data: int | float | list[int | float]) -> None` — narrows the accepted type to exactly what that subclass supports.
- This intentionally deviates from strict type-substitutability rules (may trigger mypy warnings) — expected and defensible: the *base* method's contract is "accept anything," and each subclass's override is more specific about what it actually processes, while callers going through the abstract interface remain safe.
- Same idea applies to **return types**: a subclass's factory method can return a more specific type than the abstract base's declared return type (e.g. returning `Sproutling` instead of generic `Creature`), as long as the narrower type is still a valid subtype — this can also be used to satisfy `mypy --strict` when a subclass's return value has extra methods (like `.heal()`) the base return type doesn't declare.

## Polymorphism, in practice

- Code that only knows about the **abstract interface** (`DataProcessor`, `CreatureFactory`, `BattleStrategy`) can operate uniformly over *any* concrete subclass, without knowing or caring which one it's actually holding.
- Example: `proc.validate(elem)` / `proc.ingest(elem)` inside a router (`DataStream`) — same two lines work whether `proc` is a `NumericProcessor`, `TextProcessor`, or `LogProcessor`. Each subclass's own override runs automatically based on the object's *actual* runtime type — this dispatch is the essence of polymorphism.
- Big practical payoff: **adding a new subclass never requires modifying the router/caller code.** New data type → new subclass implementing the interface → works immediately with existing `DataStream`/`CreatureFactory`-consuming code.

## Abstract Factory pattern

- Problem: calling code wants to create objects (Creatures, etc.) **without hardcoding which concrete class** to instantiate.
- Solution: an abstract `Factory` class declares `create_x()` / `create_y()` as abstract methods. Concrete factories (`FlameFactory`, `AquaFactory`) each implement these to produce their own family's concrete objects.
- Calling code holds a factory reference typed as the **abstract** factory type, and calls `.create_x()` generically — it never needs to `import` or reference the concrete product classes (`Flameling`, `Aquabub`) directly at all.

## Hiding concrete classes via `__init__.py`

- A package's `__init__.py` controls what's importable as `package.thing`.
- To satisfy "expose only the factory, not the concrete class": simply **don't import** the concrete class into `__init__.py`. If a name was never imported into the package's namespace, `package.ConcreteClass` raises `AttributeError` — even though the class still technically exists in some file inside the package.
- **Nested classes as a stronger alternative**: defining concrete classes (`Sproutling`, `Bloomelle`) *inside* their factory class body means they were never independently-existing top-level names to begin with — no risk of forgetting to exclude them from `__init__.py`, and factory methods can still return the *exact* concrete type (satisfying strict type checking) without that type ever being reachable from outside except through the factory. Tradeoff: less conventional/readable than a flat module layout.
- `__all__ = [...]` in `__init__.py` — explicitly declares the "public" names of a package; complements (doesn't replace) controlling actual imports.

## Mixins / multiple inheritance for "capabilities"

- When behavior (e.g. "can heal", "can transform") should be usable by *multiple, unrelated* class hierarchies later, don't bake it into the main base class (`Creature`). Instead, define it as a **separate abstract class** inheriting only from `ABC` (not from `Creature`).
- Concrete classes then inherit from **both**: `class Sproutling(Creature, HealCapability):` — Python supports multiple inheritance directly.
- `isinstance(obj, HealCapability)` returns `True` for any object built this way, regardless of its `Creature` lineage — lets generic code check "does this thing have capability X" without knowing its concrete type.
- Persistent per-instance state (e.g. a transform toggle) lives as a normal instance attribute, initialized in `__init__` after `super().__init__(...)`; other methods (like `attack()`) can branch behavior by checking that state.

## `Protocol` — structural typing / duck typing

- `from typing import Protocol`
- Different from `ABC`: **no inheritance required**. A class doesn't need to explicitly `class MyPlugin(SomeProtocol):` — if it simply implements a method matching the Protocol's declared signature, it's considered compatible ("if it walks like a duck...").
- Used for pluggable/interchangeable components where you don't control or want to force a specific inheritance relationship (e.g. export plugins: CSV, JSON — unrelated classes, no shared base, just a shared method shape).
- `ABC` = nominal typing (must explicitly inherit). `Protocol` = structural typing (must just match the shape).

## Strategy pattern

- Problem: behavior differs based on *some* trait of an object (e.g. creature capability), and you don't want the "orchestrating" code (tournament logic) to contain type-checking branches for every possible trait.
- Solution: encapsulate each behavior variant into its own class implementing a shared interface (`BattleStrategy` → `act()`, `is_valid()`). The orchestrator just calls `strategy.act(thing)` uniformly.
- `is_valid(thing) -> bool` — lets a strategy self-report whether it's compatible with a given object (checked via `isinstance(thing, RequiredCapability)`).
- **Validate *inside* `act()` itself** (call `self.is_valid()` as the first line, raise a dedicated exception if it fails) — don't rely on accidentally-triggered `AttributeError`s from calling an unsupported method. A dedicated custom exception (`class InvalidStrategyError(Exception): pass`) is clearer and more intentional than a bare `Exception(...)`, and lets calling code catch precisely that failure mode without accidentally swallowing unrelated bugs.

## Rank/order tracking pattern (queues, not stacks)

- "Oldest first" (FIFO) means popping from **index 0**, not the last index — `list.pop(0)`, not `list.pop()` (which removes the *last* item, i.e. LIFO/stack behavior).
- A **counter that only increments** (never resets/derived from current list length) is needed to track "original processing rank" if items can be removed from the middle/front of a collection — `len(list)` alone can't recover a removed item's original position once it's gone.

## `list[int]` vs `list[int | float]` — mypy invariance

- Mypy treats `list[int]` and `list[int | float]` as **unrelated types**, even though every `int` is valid wherever `int | float` is expected — because lists are mutable, and mypy can't safely assume it's OK to treat a `list[int]` as interchangeable with a broader type (someone could append a `float` into what's declared as `list[int]` elsewhere).
- Fix: **explicitly annotate the variable** with the broader type at creation time (`data: list[int | float] = [1, 2, 3]`) rather than passing a list literal directly into a function expecting the union type.

## Custom exceptions

- `class MyError(Exception): pass` — a minimal custom exception class. Lets callers catch *specifically* your error type (`except MyError:`) rather than a broad `except Exception:`, avoiding accidentally masking unrelated bugs.
