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


## 9. Zombies — Black Ops 2 zombie vocals  [DONE, pending in-game check]

The 66 downloaded .oggs in `assets/sounds/zombies/entity/` were regrouped into the six sets the
build-time grouper (`(.+?)(?:_)?(\d+)$`) can see, and wired in `enemies/vocals.py`:

| Set | Count | From | Used by |
| --- | --- | --- | --- |
| `ambient` | 12 | say1-6, say20-25 | `horde_ambient`, walking/running horde |
| `attack` | 16 | hurt1-14, say7-8 | `hurt_player/on_hurt` |
| `sprint` | 7 | say26-32 | `horde_ambient`, sprint-gait zombies |
| `death` | 11 | death, death2-11 | `on_zombie_dying` |
| `crawler_ambient` | 18 | say9-19, say35-41 | nothing yet — no crawler enemy |
| `crawler_sprint` | 2 | say33-34 | nothing yet |

The spec's ranges were literal filenames (there is no `say0`; the first file is `say1`), which was
confirmed by duration: say26-34 run 3.0-4.9s while every other say is 0.4-2.2s.

Per-player budgets, one channel each so a wall of death groans can't drown out the scream that tells
you a sprinter is behind you — all `#total_tick` timestamps, no per-tick decrement:
- sprint 100t (longest clip is 99t, so literally one scream at a time, as asked)
- attack 20t (1/s; eight zombies on you would otherwise be eight overlapping grunts)
- death 4t (a Nuke kills the whole round in one tick)

Gait → vocal set comes from `mgs.zb_sprint`, tagged in `zombies/types/normal` at round 10+ (speed
0.29+) and untagged by the round-15+ 10% walker roll.

- [ ] **Verify in-game** (only unchecked item): sprint screams don't overlap, attack grunt is
  directional and comes from the zombie that hit you, a Nuke doesn't wall of noise.
- [ ] Crawlers: when a legless enemy exists, point it at `VOCAL_CRAWLER_AMBIENT` /
  `VOCAL_CRAWLER_SPRINT` and tag it `mgs.zb_sprint` on the same gait rule. The constants and the
  budgets already exist; it is a selector change in `horde_ambient`, nothing more.


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


---

# Inbox (quick notes — dump anything here, unorganized "basic" format is fine)

- Make the step_height attribute of zombies 1 block tall
- Add barriers repairs sounds => find them on internet "repair.ogg", "slam[1-6].ogg", "snap[1-6].ogg", "window[1-5].ogg". And check what they are actually about to correctly use them in our zombies implementation!

