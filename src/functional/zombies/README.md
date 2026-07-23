# Zombies — TODO (implementation-ready backlog)

How this file works:
- Each numbered section below is a specced task with the decisions already made, the researched
  values, and pointers into the code so it can be picked up cold and implemented.
- `(HUMAN)` marks steps only Stoupy can do (assets, taste calls). Everything else is implementable.
- Quick/unspecced ideas go in the **Inbox** section at the very bottom (any format); they get
  promoted into specced sections here later.

Shared code map (used by many tasks below):
- Python generators in `src/functional/zombies/*.py` emit mcfunctions (stewbeet `write_versioned_function` / `write_load_file` / hooks into `zombies/start`, `zombies/stop`, `zombies/game_tick`, `zombies/preload_complete`).
- In-game map editor: `src/functional/map_editor.py` — `ALL_ELEMENTS` (element types + `defaults` = the per-element config fields), `FIELD_DOCS` (the ⓘ tooltips), `EDITOR_MODES["zombies"]["slots"]` (spawn-egg slots; next free zombies slot is `inventory.9`).
- Buyables use Bookshelf `#bs.interaction:on_right_click` / `on_hover`; deny/guard helpers in `zombies/common.py`.
- Config scores: `#zb_* mgs.config`, initialized in `zombies/game.py` → `zombies/start` (lines ~110–114).
- Zombies hotbar layout (`zombies/inventory.py`): `0` knife · `1-3` guns (3 = Mule Kick) · `4` ability item (Zonweeb variant) · `5` forbidden · `6` equipment_2 / tactical (slot is already enforced by `check_slots` but nothing is ever given there yet) · `7` equipment_1 (frags, count 4) · `8` info paper · `inventory.1-3` magazines paired with `hotbar.1-3`.
- Respawn loadout after full death (`inventory/give_respawn_loadout`): knife + M1911 + half mag + 4 frags (spec below says 2 — see task 9).


## 1. Multiplayer — knife skin/camo in loadouts  [BLOCKED: needs knife art first]

**Blocker (HUMAN):** the camo pipeline (`src/database/camo.py`) blends a *weapon texture* with a
*material texture* (HSL-color / overlay blend onto the item's `override_model` textures). The knife
is a plain vanilla `iron_sword` built inline by `helpers.py::knife_item_snbt()` — no custom model,
no texture, so there is nothing to blend. Need a knife model + texture in the item DB first.

Once art exists:
- [ ] Add the knife as a DB item with `override_model` (like guns), keep `custom_data {mgs:{knife:true}}`.
- [ ] Extend `camo.py::main()` to include it — it currently iterates only items with `custom_data.mgs.gun`; either tag the knife item as camo-eligible or special-case it. Camo item ids follow `<base>_<material>` (e.g. `knife_gold`), suffixes from `CAMO_VARIANTS` in `src/config/catalogs.py`.
- [ ] Loadout editor (`multiplayer/loadouts/editor.py`): add a "Knife" row → camo-only submenu (reuse `camo_actions_snbt` pattern). New trigger range in `catalogs.py` (next free: ~530+ is `TRIG_OVERKILL_SEC_BASE`, use e.g. 540 `TRIG_KNIFE_CAMO_BASE`). Store `knife_camo` in the editor snapshot + committed loadout. Free (no Pick-10 cost), like other camos.
- [ ] Apply in `multiplayer/loadout.py::apply_class_dynamic` (the `hotbar.0` knife give): parametrize `knife_item_snbt` with an `item_model`/camo suffix.
- [ ] Missions gets it for free — `missions/game.py` applies loadouts via the same `multiplayer/apply_class` → `apply_class_dynamic`. Verify in-game.
- Zombies keeps its plain knife (separate give in `zombies/inventory.py`), until a zombies knife wall-buy exists (task 9).


## 4. Zombies — new placeable: Der Wunderfizz (random perk machine)  [DONE]

Implemented in `src/functional/zombies/wunderfizz.py`. Editor element `wunderfizz` (slot `inventory.9`,
`all_perks` flag, `can_start_on` flag, price 1500), machine model `der_wunderfizz` (gold/purple), editor
model-display + FIELD_DOCS added. Uses the shared `zombies/perks/pool/*` helper for the "available perk"
roll; on land the perk is collectable by the buyer only for 10s (orb despawns after).

**Now roams like the Mystery Box** (shared primitives in `src/functional/zombies/roaming.py`: teddy-bear
loot table, ±512 interaction hide/show, "after N uses roll 1-in-3 to move"). A map can hold several
Wunderfizz spots — only one is ACTIVE at a time; the rest show a grayed-out `der_wunderfizz_disabled`
cabinet. After 4+ uses a pull can land on the teddy bear (buyer refunded) and the machine roams to
another spot; the roam is a model-swap (old spot → disabled, new spot → live) with the bear as the
visual cue rather than physically flying the cabinet. The Mystery Box was refactored onto the same
shared primitives and now shows the `mystery_box_disabled` crate at its inactive spots too.
⚠ In-engine polish (roam timing, disabled model look, orb float) is a HUMAN eyeball pass.


Reference (BO2 Origins, callofduty.fandom.com/wiki/Der_Wunderfizz): 1500/use; behaves like a
Mystery Box for perks; in Origins it could grant perks that have **no machine on the map** (PhD,
Deadshot, Electric Cherry existed only through it, with higher odds).

Spec (decided):
- Cost **1500** (configurable per machine via editor `price`).
- On buy: cycles perk icons like the Mystery Box spin, lands on one random perk, then it is
  collectable **by the buyer only**, and despawns after **10 s** uncollected (mirror the MB
  ready-window pattern — MB uses `mb.anim` counting down to −150 for its window).
- Pool = perks the buyer doesn't own, **restricted to perks with a machine on this map** by
  default; editor option `all_perks: false` — when true, rolls across every defined perk
  (Origins behavior). ⚠ Code fact: the `random_perk` **power-up** currently does NOT filter by
  map — `powerups.py::activate/random_perk` iterates all of `PERK_DEFINITIONS`. Build one shared
  "available perk pool" helper (map machines → available set; flag widens to all) and use it for
  BOTH the power-up and the Wunderfizz, then document the behavior in editor tooltips (task 6).

Implementation notes:
- [ ] Editor: new `ALL_ELEMENTS` entry (`save_type: "zb_object"`, `save_path: "wunderfizz"`, defaults `{price: 1500, power: True, all_perks: False}`), zombies slot `inventory.9`, add to `MODEL_DISPLAY_ELEMENTS` + a `maps/editor/displays/wunderfizz` mirror.
- [ ] Model: base the machine on the perk-machine display pipeline (`zombies/perks/setup_iter` → `display/summon_machine_display`, transforms/rotation identical). New `wunderfizz` item model in `src/database/others.py` (perk machines are `Item(id=..., override_model=...)` with vanilla textures). Look, per the wiki: mystery-box-sized machine with a glass **orb/globe on top** where perk bottles swirl; struck by lightning periodically (particle idea: `end_rod`/`electric_spark` bursts). During the spin, show tiny perk-machine models cycling at the orb center — reuse the mini perk items (`perk_machine_<id>` models, same ones the inventory perk display items use) on a small `item_display`.
- [ ] Refactor before building: the MB spin/cadence/land/collect flow (`mystery_box.py::spin_tick_one`, `cycle_step_one`, buyer-pid tracking) and the perk grant path (`perks/apply` + `on_new_perk` signal) both get reused here. Extract shared Python helpers that emit the spin/collect functions parametrized by pool + on-collect — avoid duplicating the mcfunction bodies AND the Python that writes them.
- [ ] Power gating: reuse `mgs.zb.perk.power`-style check + `deny_requires_power_body`.
- [ ] Sound: play **`assets/sounds/zombies/mystery_box/music_box_short.ogg`** (`mgs:zombies/mystery_box/music_box_short`) as the spin/use jingle for the Wunderfizz (user-picked).


## 7. Zombies — perk purchase songs  (mostly HUMAN)

State: `assets/zombies_perk_songs/` already holds 10 staged .oggs — deadshot, doubletap,
`jungernog` (typo → rename `juggernog`), mulekick, phdflopper, quickrevive, speedcola, staminup,
tombstone, whoswho. They are NOT wired (not under `assets/sounds/`).

- [ ] (HUMAN — explicitly the LAST thing on this list) download the missing final-seconds cuts:
  electric_cherry, widows_wine, timeslip, dying_wish (+ optionally a Wunderfizz jingle).
- [ ] Wiring (any time after assets land): move/rename to `assets/sounds/zombies/perks/<perk_id>.ogg`
  (same auto-registration as `zombies/powerups/*` sounds → playable as `mgs:zombies/perks/<perk_id>`),
  play in `zombies/perks/apply/<perk_id>` (generated per-perk in `perks.py`) — positional at the
  machine or private to the buyer, match the power-up sound conventions (`pu_snd` in `powerups.py`).


## 10. Zonweeb — ideas backlog

("zonweeb" is also the zombies game variant with passives/abilities — `zombies/ability.py`;
these are gameplay ideas from Zonweeb, not necessarily tied to the variant.)

- [ ] Special zombie: an "aura" zombie that grants damage resistance to zombies near it.
  Sketch: new type function alongside `zombies/types/{normal,fast,tank,armed}` (`round.py`),
  distinctive look (glowing/colored equipment so players can prioritize it), aura tick every ~10
  ticks applying brief resistance (or a health-boost/DR attribute) to zombies within ~5 blocks;
  spawn cadence e.g. 1 per round after some round via `calc_round_count`-style gating or the
  `special_spawn` markers (currently used by dog rounds; documented as reusable for minibosses).


---

# Inbox (quick notes — dump anything here, unorganized "basic" format is fine)

