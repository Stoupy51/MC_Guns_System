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
  Mystery Box position/uses (`mystery_box.py`), barricade repair state (`barricades.py`).
- [ ] Save UI: admin menu button → slot picker dialog (`register_dialog`, same pattern as
  `zombies/admin/powerups`); load UI: slot list on the setup dialog next to "Select Map".
- [ ] Load flow: run the normal `zombies/start` on the saved map/variant first (so every subsystem
  initializes the way it always does), then replay the saved state — set `game.round`, re-run each
  saved door's open function, `power/turn_on` if saved, restore per-player scores/perks/inventory
  for the players present, and skip (or park in spectator) any saved player who is offline.
- [ ] Only allow saving between rounds (the 5s gap after `round_complete`) so no live zombie,
  power-up, downed body or thrown grenade has to be serialized. This single constraint removes most
  of the hard cases — do not skip it.


## 12. Zombies — barricade sounds  [DONE — kept as the provenance record]

Assets are in `assets/sounds/zombies/barricade/` (19 files, Vorbis 48 kHz mono 96 kbps).
Not verified in game yet: whether the Carpenter slam burst is too much on a map with many barricades.

### Provenance (VERIFIED — these are the real Treyarch files, not lookalikes)

Ripped from `WAW_Sound_Dump.7z`, a community dump of Call of Duty: World at War's uncompressed
`Sound/sfx/` tree, posted on the NZ:P forum
([thread](https://nzportable.forumotion.com/t1989-world-at-war-nazi-zombies-sound-dump) ·
[direct](https://www.dropbox.com/s/lxzhzqml9755hwz/WAW_Sound_Dump.7z?dl=1)).
Source is WaW rather than BO2 because BO2's own banks are `.sabl`/`.sabs` with **hashed** alias names,
so they cannot be searched by name and no verifiable extractor exists — but BO2 reuses the WaW zombie
and barricade SFX wholesale, so these are the same recordings the BO2 player hears.

| Ours | WaW original | Count | What it is (verified by duration + envelope) |
| --- | --- | --- | --- |
| `bang[1-5]`  | `levels/zombie/windows/windows_0[0-4]`      | 5 | zombie pounding the intact barricade, 1.0-1.7s |
| `snap[1-6]`  | `levels/zombie/wood_snap/wood_snap_0[0-5]`  | 6 | board torn off, sharp crack, 0.4-1.3s |
| `slam[1-6]`  | `levels/zombie/board_slam/board_slam_0[0-5]`| 6 | board slammed in, one-shot decaying -12→-40 dB, 1.8-2.7s |
| `repair`     | `levels/zombie/windows/wood_repair/repair_ching` | 1 | 3.53s of *sustained* hammering (holds -18..-24 dB flat then cuts), i.e. a whole rebuild, not a single hit |

Renamed `windows_*` → `bang*` so the event id is not `zombies/barricade/window*`, which read as a
separate thing from the barricade itself.

The dump also confirmed two earlier inferences and one non-need:
- `levels/zombie/new_zombie_vox/` really does have a **`behind`** folder (5 files) alongside
  `ambient` (21), `attack` (23), `crawl` (6), `death` (11), `elec` (6), `sprint` (15), `sprint2` (9),
  `taunt` (7). So the `behind` channel in `enemies/vocals.py` is a real Treyarch category, not a guess.
  `death` being exactly 11 also matches our `death1-11` one-for-one.
- `levels/zombie/boards_float/boards_float.wav` is the Carpenter boards-flying-up sound. Not needed,
  `powerups/carpenter.ogg` already exists.

It also fixed the sprint vocals. Treyarch ships **two** sprint sets — `new_zombie_vox/sprint` (14 files,
0.7-2.5s) and `new_zombie_vox/sprint2` (9 files, 3.0-5.3s) — and duration-matching pinned the downloaded
pack's `sprint1-7` onto `sprint2` (1-24 ms apart), i.e. it shipped the long set. `sprint*` is now the
short primary set, so a scream no longer sits 5 seconds behind the zombie that made it (see
[[vocals]] `VOCAL_SPRINT` for why `/playsound` cannot follow an entity at all).
Still unresolved from the same comparison, and deliberately left alone: only `crawler_ambient6-11` match
WaW's 6 `crawl` vocals (0 ms exact), so the other 12 files in `crawler_ambient*` are miscategorised.
Duration matching is decisive for long clips and exact-0 hits but ambiguous under ~1.5s — three of our
files all "matched" `taunt_02` — so a full remap of the 66 vocals needs real spectral fingerprinting.

**Design decision, already taken: the barricade stays single-stage.** For the record, a Black Ops 2
barricade is 6 boards torn off and rebuilt one at a time at 10 points each
([Nazi Zombies Wiki](https://nazizombies.fandom.com/wiki/Barriers)), which is why `slam` and `snap`
ship exactly six variants — one per board index. We are not matching that: `mgs.zb.barricade.state`
stays 0/1 with one 2s teardown (`r_timer 40`), one 1.5s repair (`rp_timer 30`) and `+10` for the whole
thing, and slam/snap are used as plain random-variant pools.
Do not "fix" this later without deciding to go 6-board on purpose.

### Wiring

Files auto-register as `mgs:zombies/barricade/<name>` (stewbeet sounds plugin), and `slam1..slam6`
collapse into one random-pick event — which is what we want now that we are single-stage.

All five placeholders are replaced, in `objects/barricades/`:
- [x] `tick.py::destroy` — `snap*`, one-shot when the boards come off
- [x] `tick.py::repair` — `slam*`, one-shot when the rebuild completes
- [x] `hooks.py::instant_repair` (Carpenter) — `slam*`, one per barricade, unbudgeted on purpose
- [x] `tick.py::on_remover_valid` — `bang*`, budgeted per player at `BANG_INTERVAL`
- [x] `tick.py::start_repairing_player` — `repair_no_cash`, budgeted per player at `REPAIR_INTERVAL`

`on_remover_valid` runs **every tick** of the 40-tick teardown, so it carries the same `#total_tick`
timestamp budget as `enemies/vocals.py` or a barricade under attack becomes a machine gun of wood hits.
Budgets are per player, not per barricade: several players can stand at one window.
The repair hammering hangs off `start_repairing_player` rather than the per-tick `on_repairer_valid` —
it fires exactly once when a repairer is assigned, and the clip already outlasts the 30-tick repair. Its
budget exists only so tapping sneak to restart a repair cannot stack copies of it.


---

# Inbox (quick notes — dump anything here, unorganized "basic" format is fine)

- A day in 2027: Add this map https://www.planetminecraft.com/project/black-ops-ii-mob-of-the-dead-minecraft-in-2013/

