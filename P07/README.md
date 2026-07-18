# Module Notes: DataDeck (Abstract Card Architecture)

Core theme: **applying abstract factory, mixin/capability composition, and strategy patterns together in one cohesive, multi-exercise system.**
(This module is a direct, practical continuation of the patterns introduced conceptually in Code Nexus — see those notes for the underlying theory.)

---

## Project-wide structural rule

- `A __init__.py file is MANDATORY for each exercise folder. All testing code will be located at the root of the git repository.`
- Recurring shape across all three exercises: `<test_script>.py` at repo root + `exN/` package folder (with `__init__.py` + implementation file(s)) — the test script imports the package and exercises it, never containing business logic itself.

## Abstract Factory pattern (ex0)

- `Creature(ABC)` — shared attributes (`name`, `creature_type` — avoid naming a param/attr `type`, it shadows the built-in), one abstract method (`attack`, since message differs per subclass), one concrete method (`describe`, since the format is identical for every subclass and belongs once in the base).
- `CreatureFactory(ABC)` — abstract `create_base()` / `create_evolved()`. Concrete factories (`FlameFactory`, `AquaFactory`) each instantiate and return their own family's concrete creatures.
- **Payoff**: calling code (`battle.py`) holds a `CreatureFactory`-typed reference and calls `.create_base()`/`.create_evolved()` generically — it never imports or names a concrete Creature class directly. Adding a new family later (`GrassFactory`) requires zero changes to existing calling code.
- **Enforcing "package exposes only factories, never concrete classes"**: don't import concrete classes into `__init__.py` (they become unreachable as `package.ConcreteClass` → `AttributeError`), or go further and **nest** concrete classes inside their factory's class body — see below.

## Mixins for cross-cutting "capabilities" (ex1)

- Capability classes (`HealCapability`, `TransformCapability`) inherit from `ABC` **only** — deliberately **not** from `Creature` — because the capability isn't inherently tied to being a Creature; keeping it separate means it could be reused for a completely different kind of object later.
- Concrete classes use **multiple inheritance** to combine a base type with a capability: `class Sproutling(Creature, HealCapability):`.
- Persistent state impacting behavior (e.g. a transform toggle affecting `attack()`'s message) — a plain instance attribute set in `__init__` (after `super().__init__(...)`), checked/flipped by the capability's own methods (`transform()`/`revert()`).
- `isinstance(obj, HealCapability)` works correctly on any object built via multiple inheritance this way — this is exactly what lets *generic* code (ex2's strategies) check "does this creature support healing" without knowing its concrete class.

## Nested classes as a design solution (used heavily in ex1)

**Problem it solves**: tension between (a) "don't expose concrete classes outside the package" and (b) needing factory methods' return types to be *precise* enough for `mypy --strict` to know the returned object really has `.heal()`/`.transform()` (a plain `Creature`-typed return fails strict type checking on calls to capability-specific methods).

**Solution**: define concrete classes (`Sproutling`, `Bloomelle`) **inside** their factory's class body (`HealingCreatureFactory.Sproutling`), rather than as independent top-level classes in the module.

- The class's only "address" becomes `Factory.NestedClass` — it was never an independently-existing top-level name, so there's nothing to accidentally forget to exclude from `__init__.py`.
- Factory methods can still type-hint the **exact** concrete return type (`def create_base(self) -> Sproutling:`), satisfying `mypy --strict`, without that type ever being importable/reachable from outside the factory.
- Tradeoff to be able to articulate: less conventional/readable than a flat module with `__all__`-based exclusion; a deliberate readability-vs-structural-guarantee tradeoff.

## Strategy pattern (ex2)

- Direct continuation of Code Nexus's strategy pattern concept, applied concretely.
- `BattleStrategy(ABC)` → abstract `act(creature)` and `is_valid(creature)`.
- Each concrete strategy's `is_valid()` checks a specific capability via `isinstance(creature, RequiredCapability)`.
- **`act()` must call `self.is_valid(creature)` explicitly as its first step**, and raise a **dedicated custom exception** (not a generic `Exception`, and not relying on an accidental `AttributeError` from calling an unsupported method) if invalid. This is more intentional, more precise for callers to catch, and doesn't risk silently swallowing unrelated bugs via an overly broad `try/except`.
- Orchestrating code (`tournament.py`) treats every strategy uniformly through the abstract interface — no `isinstance`/type-checking branches live in the orchestrator itself; that logic is fully encapsulated inside each strategy.

## Round-robin / all-pairs iteration pattern

- "Every opponent fights every other opponent once" (no duplicate pairs, no self-fights) — classic nested-loop pattern:
  ```python
  for i in range(len(items)):
      for other in items[i+1:]:
          # pair (items[i], other)
  ```
  Starting the inner loop at `i+1` (not `0`) avoids both duplicate pairings and self-pairing, without needing extra `if` checks.

## Custom exceptions for domain-specific errors

- `class InvalidStrategyError(Exception): pass` — minimal custom exception, raised deliberately (not accidentally triggered), caught specifically by name in orchestrating code (`except InvalidStrategyError:`) rather than a broad `except Exception:`.
- Lets error-handling code distinguish "this specific expected failure mode" from "some unrelated bug crashed unexpectedly" — broad exception catching risks masking real bugs during debugging/evaluation.

## Deriving display labels from existing data vs. new attributes

- When needing a human-readable label for an object that doesn't cleanly derive from one consistent rule (e.g. some "families" are best labeled by a creature name, others by a category name) — decide deliberately between:
  - Adding an explicit class-level `name` attribute per class (clear, but requires remembering to set it correctly for every future class, and can involve awkward choices like "naming a factory after a creature").
  - Deriving it from data that already exists for **functional** reasons (e.g. `factory.create_base().name`, or `type(obj).__name__` with a known suffix stripped via `str.removesuffix(...)`) — one consistent rule, no new state, automatically extends to future classes without extra work. Minor tradeoff: may have small side effects (e.g. instantiating an object just to read a label) worth being aware of, though usually harmless if cheap/stateless.

## Multiple inheritance + type hints — a genuine open question

- When a method needs an object that is simultaneously "a `Creature`" *and* "has `TransformCapability`," plain `Creature` as a type hint is too broad (misses the capability-specific methods) but there's no single class that *is* both without also being a specific concrete subclass.
- Real options: hint against the capability type alone (`TransformCapability`), accept the imprecision and rely on `is_valid()` as the actual runtime guard, or use `Protocol`/structural typing to express "must have shape X" — worth being able to discuss the tradeoffs even if you settle on the pragmatic option (broad hint + runtime `is_valid()` check) for a given exercise.
