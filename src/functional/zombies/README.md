# Zombies — TODO (implementation-ready backlog)

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


## 12. Zombies — barricade sounds  [BLOCKED on assets (HUMAN) — everything else is decided]

- [ ] (HUMAN, and the only blocker) download `repair.ogg`, `slam[1-6].ogg`, `snap[1-6].ogg`,
  `window[1-5].ogg` into `assets/sounds/zombies/barrier/`. They are not reachable from a build:
  not indexed anywhere public, and they are BO2 game assets.

**Design decision, already taken: the barricade stays single-stage.** For the record, a Black Ops 2
barricade is 6 boards torn off and rebuilt one at a time at 10 points each
([Nazi Zombies Wiki](https://nazizombies.fandom.com/wiki/Barriers)), which is almost certainly why
`slam` and `snap` ship exactly six variants — they read as one sound per board index. We are not
matching that: `mgs.zb.barrier.state` stays 0/1 with one 2s teardown (`r_timer 40`), one 1.5s repair
(`rp_timer 30`) and `+10` for the whole thing, and slam/snap are used as plain random-variant pools.
Do not "fix" this later without deciding to go 6-board on purpose.

### What the files probably are (INFERRED — not verified)

Guessed from the names plus BO2's mechanics. Confirm with `ffprobe` durations once the .oggs land —
that is exactly how the `say*` vocal ranges got pinned down, a loop and a one-shot are obvious apart:

| File | Best guess |
| --- | --- |
| `slam[1-6]` | player slamming a board into place |
| `snap[1-6]` | zombie ripping a board off |
| `window[1-5]` | zombie pounding on the intact barricade |
| `repair` | the held-interact loop while repairing |

### Wiring

Files auto-register as `mgs:zombies/barrier/<name>` (stewbeet sounds plugin), and `slam1..slam6`
collapse into one random-pick event — which is what we want now that we are single-stage.

Placeholders to replace, all in `objects/barriers/`:
- [ ] `tick.py::destroy` — `minecraft:entity.zombie.break_wooden_door` → `snap*`
- [ ] `tick.py::repair` — `minecraft:block.anvil.use` → `slam*`
- [ ] `hooks.py::instant_repair` (Carpenter) — `minecraft:block.wood.place` → `slam*`
- [ ] `tick.py::on_remover_valid` — silent today → `window*`
- [ ] `tick.py::on_repairer_valid` — silent today → `repair`

The last two run **every tick** while a barricade is being torn down / rebuilt, so they need the same
`#total_tick` timestamp budget as `enemies/vocals.py`, or a barricade under attack turns into a
machine gun of wood sounds. `window*` should be per-player budgeted (several players can watch the
same barricade); `repair` only ever has one repairer, so a per-barrier interval is enough.


---

# Inbox (quick notes — dump anything here, unorganized "basic" format is fine)

- A day in 2027: Add this map https://www.planetminecraft.com/project/black-ops-ii-mob-of-the-dead-minecraft-in-2013/

