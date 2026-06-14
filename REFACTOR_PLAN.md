# StoupGun (MGS) — Object-Oriented Refactor Plan

> Internal Python refactor only. **The generated datapack output must stay byte-identical.**
> Source: `src/` · Build: `beet build` → `build/datapack/data` · ~23k LOC, 86 files, 119 module-level functions, **0 classes**.

---

## Current Status (live)

- ✅ **P0 Foundation** — `McfunctionGenerator` base class + verification harness.
- ✅ **P1 Game modes** — all 5 variants converted, build byte-identical.
- 🟡 **P5 Feature modules** — converted so far: all of `core/*` (bounds, commands,
  map_loading, map_menus, spawning, teleport) + `weapon/` kick, zoom, actionbar.
  ~27 generators remain (mechanical, one class per file, build-diff after each).
  Verification switched from a `/tmp` snapshot to `git status build/datapack/data`
  (build output is git-tracked, so an empty status = output unchanged).
- ⏸️ **P2 Catalog dataclasses**, **P4 shared lifecycle** — designed, not yet executed
  (P4 is the largest/riskiest; attempt only with the harness green).
- ⏭️ **P3 utilities** — deferred by design (already cohesive free functions).

Every completed step was verified with `beet build && diff -r /tmp/mgs_baseline/data
build/datapack/data` → identical. This is a large refactor (23k LOC); remaining items are
tracked as checkboxes below and can be picked up incrementally without rework.

---

## Executive Summary

The codebase is entirely procedural. Every generator follows the same skeleton and there is heavy structural repetition:

1. **Boilerplate header in every generator** — all 119 generator functions open with
   `ns = Mem.ctx.project_id` / `version = Mem.ctx.project_version`, then call
   `write_versioned_function(path, f"...{ns}...{version}...")`. The same two lines and the
   same `f"…{ns}:v{version}/…"` pattern are repeated literally hundreds of times.

2. **The five multiplayer game modes** (`free_for_all`, `team_deathmatch`, `domination`,
   `hardpoint`, `search_and_destroy`) all emit functions under
   `multiplayer/gamemodes/<key>/…` and all share the same lifecycle contract
   (`setup`, `tick`, `on_kill`, `cleanup`, + mode-specific extras). This is a textbook
   template/strategy hierarchy implemented today as 5 free functions.

3. **The three "modes"** (`multiplayer`, `zombies`, `missions`) duplicate an entire game
   lifecycle: `start`, `stop`, `join_game`, `summon_spawns` / `summon_spawn_iter` /
   `summon_spawn_at`, `tp_all_to_spawns`, `pick_spawn`, `tp_to_spawn`, `tp_player_at`,
   `respawn_tp`, `create_sidebar` / `refresh_sidebar` / `build_sidebar`, `prep_tick`,
   `end_prep`. The bodies are near-identical, parameterized only by storage name,
   score prefix, and mode path. `functional/helpers.py` already factored *some* of this
   into free line-builders (`prep_freeze_lines`, `late_join_flow_lines`, …) — evidence the
   abstraction wants to be a class.

4. **Catalog data is loose tuples.** `PRIMARY_WEAPONS`, `SECONDARY_WEAPONS`, `PERKS`,
   `GRENADE_TYPES`, `CAMO_VARIANTS`, `EQUIPMENT_PRESETS` are `list[tuple[...]]`, unpacked
   positionally all over the codebase (`for weapon_id, _, _, mag_id, mag_count, *_ in …`).
   Fragile and unreadable. Frozen dataclasses are the natural fit.

5. **`functional/helpers.py` and `functional/zombies/common.py`** are grab-bags of
   command-string builders (`MGS_TAG`, `btn`, `styled_text`, guards, deny bodies). These
   are cohesive enough to become small utility classes / a `Snbt` text helper.

6. **Item definitions** (`database/*.py`) are sequences of `add_item(...)` calls driven by
   `config/stats.py`. Lower priority — already fairly data-driven.

### Strategy & safety

- A thin **`Generator` base class** captures the universal boilerplate (`ns`, `version`,
  `func()`, `load()`, `tick()`). Every existing `main()` / `generate_*()` becomes a tiny
  wrapper that instantiates the class and calls it — **module-level signatures are
  preserved** so `__init__.py` import chains and `link.py` keep working untouched.
- Verification is a **byte diff of the generated datapack** before/after every step
  (harness below). Output identity is not argued, it is measured.
- Prefer **composition**: `GameMode` *has* a `SpawnSystem` / `SidebarSystem`, gamemodes are
  *strategies* plugged into the multiplayer mode. Inheritance only where the "is-a" is real
  (`ZombiesMode(GameMode)`).

---

## Verification Harness (do this first, run after every task)

```bash
# Baseline (captured once, before any change):
beet build
rm -rf /tmp/mgs_baseline && mkdir -p /tmp/mgs_baseline
cp -r build/datapack/data /tmp/mgs_baseline/data

# After each refactor task:
beet build && diff -r /tmp/mgs_baseline/data build/datapack/data && echo "✅ IDENTICAL"
```

Any non-empty `diff` = the refactor changed output = revert/fix before checking the box.
The `headers`/`lang` plugins are deterministic (no timestamps), so identical source state
⇒ identical bytes. A change to any displayed string also changes the auto-generated lang
keys, so string edits are caught too.

---

## Proposed Class Hierarchy

```mermaid
classDiagram
    class Generator {
        <<abstract>>
        +str ns  (Mem.ctx.project_id)
        +str version  (Mem.ctx.project_version)
        +func(path, body) void   // write_versioned_function
        +raw_function(full_path, body) void
        +load(body, prepend=False) void
        +tick(body) void
        +tag(name, registry, values) void
        +generate()* void
        +__call__()  // delegates to generate(), drop-in for old main()
    }

    class GameMode {
        +str mode          // "multiplayer" | "zombies" | "missions"
        +str storage       // mgs:<storage> storage root
        +str score_prefix  // e.g. "mp" -> mgs.mp.*
        +bool has_teams
        +SpawnSystem spawns
        +SidebarSystem sidebar
        +generate_start() void
        +generate_stop() void
        +generate_join() void
        +generate_prep() void
    }
    class MultiplayerMode
    class ZombiesMode
    class MissionsMode

    class SpawnSystem {
        +GameMode owner
        +generate()  // summon_spawns / _iter / _at, tp_all, pick_spawn, tp_to_spawn...
    }
    class SidebarSystem {
        +GameMode owner
        +generate()  // create/refresh/build sidebar
    }

    class GameModeVariant {
        <<abstract>>
        +str key       // ffa | tdm | dom | hp | snd
        +str prefix    // multiplayer/gamemodes/<key>
        +sub(name, body) void
        +setup_body()* str
        +tick_body()* str
        +on_kill_body()* str
        +cleanup_body()* str
        +generate() void
    }
    class FreeForAll
    class TeamDeathmatch
    class Domination
    class Hardpoint
    class SearchAndDestroy

    class Snbt {
        <<utility>>
        +MGS_TAG: str
        +btn(label, command, ...) str$
        +styled_text(text, **attrs) str$
        +tellraw_mgs(text, color) str$
    }

    class Weapon {
        <<dataclass frozen>>
        +str id
        +str display
        +str category
        +str mag_id
        +int mag_count
        +bool in_loadout
        +bool is_consumable
    }
    class Perk
    class ClassLoadout

    Generator <|-- GameMode
    Generator <|-- GameModeVariant
    GameMode <|-- MultiplayerMode
    GameMode <|-- ZombiesMode
    GameMode <|-- MissionsMode
    GameModeVariant <|-- FreeForAll
    GameModeVariant <|-- TeamDeathmatch
    GameModeVariant <|-- Domination
    GameModeVariant <|-- Hardpoint
    GameModeVariant <|-- SearchAndDestroy
    GameMode *-- SpawnSystem
    GameMode *-- SidebarSystem
    MultiplayerMode o-- GameModeVariant
```

---

## Refactor Tasks

### Priority 0 — Foundation (unblocks everything)
- [x] **T0.1** Capture baseline build snapshot (`/tmp/mgs_baseline/data`). *(done during planning)*
- [x] **T0.2** Create `src/functional/generator.py` with the `McfunctionGenerator` base class
  (`ns`, `version` properties from `Mem`; `func()`, `raw_function()`, `load()`, `tick()`;
  abstract `generate()`; `__call__` delegates to `generate()`). Full docstrings.
  *(class renamed `Generator` → `McfunctionGenerator`.)*
- [x] **T0.3** Verify: `beet build && diff -r` → ✅ IDENTICAL.

### Priority 1 — Game mode variants (self-contained, low risk, clear win)
- [x] **T1.1** Create `src/functional/multiplayer/gamemodes/base.py` with
  `GameModeVariant(McfunctionGenerator)` (ABC): `key`, `prefix`, `sub(name, body)` helper.
  *(Dropped the `setup_body/tick_body/...` abstract contract — DOM/HP/SnD have interleaved
  logic and extra helpers that don't fit a fixed 4-method shape; each variant implements
  `generate()` directly via `sub()`, preserving exact write order. Bodies kept byte-identical
  by binding `ns = self.ns; version = self.version` at the top of each `generate()`.)*
- [x] **T1.2** Convert `team_deathmatch.py` → `TeamDeathmatch(GameModeVariant)`; keep
  `generate_team_deathmatch()` as a one-line wrapper. Verify diff → ✅.
- [x] **T1.3** Convert `free_for_all.py` → `FreeForAll`. Verify diff → ✅.
- [x] **T1.4** Convert `domination.py` → `Domination`. Verify diff → ✅.
- [x] **T1.5** Convert `hardpoint.py` → `Hardpoint`. Verify diff → ✅.
- [x] **T1.6** Convert `search_and_destroy.py` → `SearchAndDestroy`. Verify diff → ✅.
- [x] **T1.7** `gamemodes/__init__.py` left untouched — the preserved wrapper functions keep
  the import/call chain working with zero churn. Full build diff → ✅ IDENTICAL.

### Priority 2 — Catalog dataclasses (readability, type-safety)
- [ ] **T2.1** Add frozen dataclasses to `config/catalogs.py`: `Weapon`, `SecondaryWeapon`,
  `Perk`, `GrenadeType`, `CamoVariant`, `EquipmentPreset`. Provide `__iter__`/`__getitem__`
  shims so existing positional unpacking keeps working (zero-churn migration), OR migrate
  call sites. Decide per-type; default to shims first, then migrate readers incrementally.
- [ ] **T2.2** Migrate `functional/zombies/common.py::build_weapon_magazine_data` and
  `setup_definitions.py` readers to attribute access. Verify diff after each.

### Priority 3 — Command/text utilities
- [~] **T3.1** *Deferred (low value).* `helpers.py` / `zombies/common.py` are already cohesive,
  stateless string builders. Wrapping `MGS_TAG` / `btn` / `styled_text` in a class adds
  ceremony without state or polymorphism — it violates "composition where it *makes sense*."
  Left as free functions intentionally. Revisit only if shared mutable state appears.

### Priority 4 — Shared game-mode lifecycle (largest, highest risk — do last)
- [ ] **T4.1** Create `src/functional/game_mode.py` with `GameMode(Generator)` +
  `SpawnSystem` + `SidebarSystem` (composition). Parameterize storage / score_prefix / mode.
- [ ] **T4.2** Port `multiplayer/game.py` spawn+sidebar+lifecycle into `MultiplayerMode`,
  delegating bodies through the base. Verify diff (this is the strict one).
- [ ] **T4.3** Port `zombies/game.py` into `ZombiesMode(GameMode)`. Verify diff.
- [ ] **T4.4** Port `missions/game.py` into `MissionsMode(GameMode)`. Verify diff.
- [ ] **T4.5** Collapse duplicated spawn/tp/sidebar bodies into the shared base where they
  are provably identical; keep mode-specific overrides. Verify diff. Commit.

### Priority 5 — Feature modules (incremental, opportunistic)
- [~] **T5.1** Convert `functional/weapon/*` `main()` generators to `McfunctionGenerator`
  subclasses (one class per file), wrappers preserved. **Done:** kick → `KickGenerator`,
  zoom → `ZoomGenerator`, actionbar → `ActionbarGenerator` (all diff-clean).
  **Remaining:** ammo, casing, common, grenade, projectile, raycast, sound, switch, update_lore.
- [ ] **T5.2** Convert `functional/zombies/*` `generate_*()` generators likewise. Not started
  (~19 files).
- [x] **T5.3** Convert `functional/core/*` shared writers to `McfunctionGenerator` subclasses.
  **Done:** teleport → `SharedTeleport`, bounds → `SharedBounds`, commands → `SharedCommands`,
  map_loading → `SharedMapLoading`, map_menus → `SharedMapMenus`, spawning → `SharedSpawning`.
  All diff-clean. (`commands` keeps a direct `write_tag` import for the map-script function tags.)

### Final
- [ ] **TF.1** Full `beet build && diff -r` clean. Confirm 1155 mcfunctions unchanged.
- [ ] **TF.2** Confirm no remaining `ns = Mem.ctx.project_id` boilerplate in converted files.
- [ ] **TF.3** Update this plan: all boxes checked or explicitly deferred with reason.

---

## Migration Notes / Gotchas

- **Lazy `Mem` access.** `Mem.ctx` is only valid *during* the beet pipeline. The `Generator`
  base must read `ns`/`version` lazily (in `__init__` called from the wrapper at generate
  time, or via `@property`), **never at class-definition / import time**. Instantiating
  generators at module import would read `Mem.ctx` too early and crash.
- **Output ordering matters.** `write_versioned_function` registration order can affect
  generated artifacts (and `setup_definitions.py` explicitly re-sorts `Mem.definitions`).
  Keep the call order inside each converted generator identical, and keep the `main()`
  call order in every `__init__.py` identical.
- **Preserve every displayed string verbatim.** The `auto.lang_file` plugin derives
  translation keys from text; any whitespace/case change in a tellraw silently changes
  output. The diff harness catches this — trust it.
- **Tabs vs spaces.** Files are inconsistent (`helpers.py` mixes tab- and space-indented
  defs). Match each file's existing indentation when editing to avoid noise.
- **Circular imports.** `zombies/common.py` imports from `multiplayer/classes.py`;
  `generator.py` must stay dependency-free (only import `stewbeet`) so any module can import
  it without cycles.
- **Dataclass migration risk.** Positional tuple unpacking (`*_`) is everywhere; switching
  to dataclasses without iteration shims will break readers. Use shims or migrate
  readers in the same commit, and lean on the diff.
- **`beet build` is ~29s.** Verification is not free; batch related conversions, then diff.

## Priority Order (rationale)
1. **P0 foundation** first — nothing else can subclass without `Generator`.
2. **P1 gamemodes** next — fully self-contained, smallest blast radius, proves the pattern.
3. **P2/P3** data + utils — low risk, improve every later step's readability.
4. **P4 lifecycle** last among structural work — biggest duplication payoff but highest risk;
   only attempt once the harness and base classes are battle-tested.
5. **P5** feature modules — mechanical, do opportunistically as context allows.
