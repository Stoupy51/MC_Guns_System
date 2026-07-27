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


## 11. Zombies — save a game and load it later  [NOT IMPLEMENTED — specced only]

Goal: "Save & Quit" like Black Ops — freeze a run to a slot, reload it another day and carry on.
Deliberately left unbuilt: it is the only backlog item that has to serialize **every** subsystem's
state at once, and a half-correct restore silently corrupts a map (doors visually shut but pathable,
a box that can't be bought, perks nobody owns). It needs an in-game verification pass per subsystem,
so it is specced here instead of shipped blind.

Storages persist in the world save, so a save slot is just a compound under a dedicated storage —
no files, no external state. Suggested layout, one entry per slot in `mgs:zombies_saves slots[]`:

```
{ name:"Saturday run", map:"<map id>", variant:"vanilla|zonweeb", round:17, saved_at:<gametime>,
  players:[ {uuid:[I;..], name:"Stoupy51", points:.., kills:.., downs:.., lethal_type:.., ability:..,
             passive:.., qr_uses:.., dw_uses:.., max_health:.., perks:{juggernog:1,..},
             inventory:[<player Inventory NBT>]} ],
  map_state:{ power:0|1, pap_unlocked:0|1, doors:[<group ids opened>], spawns:[<unlocked group ids>],
              box:{pos:[..], uses:.., moved:0|1}, wallbuys:[<bought ids per player>] } }
```

What has to be captured, and where it lives today (this list IS the work):
- [ ] Round + game meta — `storage mgs:zombies game` (`map`, `variant`, `round`, `state`).
- [ ] Per-player scores — `mgs.zb.points` / `kills` / `downs` / `passive` / `ability` / `qr_uses` /
  `dw_uses` / `lethal_type`, every `mgs.zb.perk.<id>` (`PERK_DEFINITIONS` in `perks.py`) plus the
  `mgs.perk.<id>` tags, and `max_health` (Juggernog sets base 40).
- [ ] Per-player inventory — the whole `Inventory` NBT (guns carry their PAP level, camo, ammo and
  slot tags in `custom_data`). **Restore already exists**: `zombies/inventory/restore_inventory`
  (built for Who's Who / Tombstone) takes a copied `Inventory` list in `mgs:temp _restore.items`.
- [ ] Map progress — `#zb_power` (`power.py`), PAP unlock (`pap.py`), opened doors (`doors.py`:
  door entities + the `mgs.spawn_unlocked` tag on the spawn points each door group unlocks),
  Mystery Box position/uses (`mystery_box.py`), barrier repair state (`barriers.py`).
- [ ] Save UI: admin menu button → slot picker dialog (`register_dialog`, same pattern as
  `zombies/admin/powerups`); load UI: slot list on the setup dialog next to "Select Map".
- [ ] Load flow: run the normal `zombies/start` on the saved map/variant first (so every subsystem
  initializes the way it always does), then replay the saved state — set `game.round`, re-run each
  saved door's open function, `power/turn_on` if saved, restore per-player scores/perks/inventory
  for the players present, and skip (or park in spectator) any saved player who is offline.
- [ ] Only allow saving between rounds (the 5s gap after `round_complete`) so no live zombie,
  power-up, downed body or thrown grenade has to be serialized. This single constraint removes most
  of the hard cases — do not skip it.


## 12. Multiplayer — one death, two death messages  [NEEDS REPRO]

From a playtest log, both lines at the same timestamp (= same tick), same victim:

```
[CHAT] DenisBrogniartBG sent Stoupy51 to the shadow realm     <- random_kill_message (attacker found)
[CHAT] Stoupy51 forgot how gravity works                      <- random_death_message (no attacker)
```

So one death printed through both the attributed and the unattributed path. The two paths are
`multiplayer/simulate_death` (bullet/OOB interception, `game.py`) and `multiplayer/on_respawn`
(vanilla death detected via the `deathCount` criterion, `loadouts/class_selection.py`). Both already
guard on `mp.spectate_timer matches 1..` / `gamemode=spectator`, and both set that state through
`enter_death_spectate` — reading the code, neither order of execution reproduces this, including the
S&D branch (`snd/on_death` does set spectator). So the guard is being defeated by something not
visible in the source path: needs a repro to pin down.

- [ ] Repro attempt: FFA/TDM, victim on low HP, killed by a bullet on the same tick as an
  out-of-bounds / void tick (`core/bounds.py` deals `10000 out_of_world`, a *real* vanilla death).
- [ ] If it can't be reproduced, make it unreproducible by construction: give the death a one-tick
  claim (`#mp_death_claim` per player, set by whichever path prints first and checked by both)
  instead of relying on `spectate_timer` / gamemode, which `enter_death_spectate` sets only at the
  very end and never in the S&D branch.


---

# Inbox (quick notes — dump anything here, unorganized "basic" format is fine)

- Pouvoir mettre un flag aux spawns de zombies en mode éditeur pour indiquer que dès que ces zombies spawnent, ils doivent path finder jusqu'à une barriere précise
- When mystery box is moving, all grayed mystery boxes are hidden (which is odd), why would the mystery box placeholder be removed if no box was or will move here?
- Mystery Box: Add a message in chat indicating WHERE the box moved. To know that, add in the editor a way to name the place where the box is (for each box) and a fallback to the current message if the name is not set!

