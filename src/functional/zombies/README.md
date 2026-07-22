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


## 2. Missions — mobs drop their weapon on death  [DONE]

The whole drop (static `item_display` + interaction hitbox, 30 s pickup, spare 50% mag embedded as
`drop_mag`, raycast straight down so mid-air deaths land on the floor) now lives in
`src/functional/core/weapon_drop.py` as `shared/drops/*`; only the capture step is per-caller.

- [x] Refactor: `core/weapon_drop.py::write_shared_weapon_drop_functions` emits `shared/drops/drop`
  (entry) + spawn/mag/pickup/collect/take/swap/overkill. Callers fill `mgs:temp _dropw` (the gun
  item, no `Slot` tag) and `#drop_ammo mgs.data`, then call `shared/drops/drop` positioned at the
  corpse. `weapon_drop_tick_lines(ns)` is the lifetime countdown, called from both game ticks.
  Tags/objective are no longer mp-prefixed: `mgs.dropped_gun` · `mgs.drop_int` · `mgs.drop_timer`.
- [x] MP capture (`multiplayer/drop_held_weapon`) is now just the hotbar.1/2 slot pick + the live
  ammo score; everything else moved out.
- [x] Mission capture: `missions/drop_enemy_weapon` reads `equipment.mainhand` into `_dropw`
  (verified in-game: `/data get entity @n[tag=mgs.mission_enemy] equipment.mainhand` returns the
  full gun stack). It tags the mob `mgs.drop_done`, so every trigger below is idempotent.
- [x] Primary trigger: `raycast/apply_damage` (and `projectile/damage_entity`) fire the drop on the
  killing shot, where `@s` is the victim and still holds the gun. No corpse scan involved.
- [x] Backup trigger: `missions/death_watch_tick` → `missions/check_enemy_dead` reads
  `data get entity @s Health` into a score and drops at `..0`, the same read raycast uses for kill
  detection. Two NBT compound matches were tried there first and each went 0-for-34 in playtest
  (`DeathTime:1s`, then `Health:0.0f`) — never use one of those as the death signal here.
- [x] Mob drop ammo: `#drop_ammo 0` → the shared path's "half a magazine" branch, so mobs drop the
  same 50% mag + one spare 50% mag a player's empty gun leaves behind.
- [x] Vanilla drop removed: `mob_ai.py::mob/default/on_new` set `HandDropChances`, a key that no
  longer exists (renamed `drop_chances` in 1.21.5), so armed mobs were silently rolling the vanilla
  8.5% mainhand drop. Now `drop_chances {mainhand:0.0f,offhand:0.0f}` — the explicit drop is the
  only one.
- [x] Pickup gate accepts missions players (`mgs.mi.in_game`) alongside MP; hotbar rules and the
  Overkill two-primaries check are unchanged, which is what missions wants since it runs MP classes.
- [x] Playtested: mobs drop their gun at the corpse.
- [ ] Still unverified in the field: a mob killed mid-air / on a rooftop, the 30 s despawn, pickup
  take/swap, the spare mag landing in the main inventory, and the Overkill deny.


## 2b. Missions — death handling  [IMPLEMENTED — needs playtest]

- [x] Fake death at the end of prep: `mgs.mp.death_count` (the `deathCount` criterion) kept counting
  in the lobby, and `player/tick` fires `missions/on_respawn` as soon as the state turns active — so
  any death taken before the mission killed the player the instant the countdown ended.
  `missions/start` now clears it (and `mp.spectate_timer`), like multiplayer and zombies already did.
- [x] Simulated death, as in multiplayer: `utils/signal_and_damage(_plain)` routes lethal damage on a
  `mgs.mi.in_game` player (state must be `active` — `mi.in_game` is an opt-in flag set in the lobby)
  to `missions/simulate_death`, which heals instead of dying. No vanilla death → no world-spawn
  teleport, and the corpse position stays meaningful.
- [x] Spectate from the death point: a simulated death leaves the body where it fell, so
  `enter_death_spectate` skips `spectate_random_player` when `mgs.mi.died_here` is set and the
  camera simply stays there. Vanilla deaths (fall, lava, the OOB kill) have already been teleported
  to the world spawn by then, so those still spectate a teammate. Respawning always goes back to a
  mission spawn via `missions/respawn_tp` — respawning at the death point was tried and rejected.
- [x] Mobs stop shooting a dead player: `mob/tick` picks its target with `on attacker`, which has no
  gamemode filter and outlives the fight, so a mob kept firing at the spectator camera of whoever
  last shot it. It now drops a target that is not in adventure/survival and falls through to the
  nearest-live-player search (which already excluded spectators).
- [x] `missions/enter_death_spectate` is now shared by both paths, and drops the held gun at the
  corpse the same way multiplayer does.
- [ ] Playtest: die to an enemy bullet (no death screen, camera stays at the body, mobs stop firing
  at it), die to fall damage (spectates a teammate), both respawning at a mission spawn after the
  3 s countdown with a fresh loadout.


## 3. Zombies — partial ("chip-in") purchases for doors & perks  [IMPLEMENTED — needs playtest]

Editor-configurable partial payments: e.g. a 5000-point door with `partial_price: 500` takes 10
payments of 500 (from any mix of players). **Doors = global** progress (any player can contribute).
**Perks = local** progress (each player pays their own perk; no contributing to someone else's).

Chunking rule (decided): fixed `partial_price` chunks, the last one being whatever is left. The
payer must afford the whole chunk — no pay-what-you-have.

- [x] Editor (`map_editor.py`): `partial_price: 0` on `door` and `perk_machine` `defaults`
  (0/absent = disabled, buy in one payment), `FIELD_DOCS` entries for both (global vs local is
  spelled out in the tooltip), and `maps/editor/set_door_link_partial_price` so it propagates
  across the `link_id` like every other door field.
- [x] Old maps: `maps/editor/backfill_zb_defaults` fills any `defaults` field the saved map
  predates onto the summoned marker (absent-only), so `partial_price` shows `0` instead of a blank
  row. Generic — every future field addition gets the same treatment for free.
- [x] Doors (`zombies/doors.py`): `mgs.zb.door.partial` + `mgs.zb.door.paid` on the interaction
  entities. `doors/read_price` (shared by click + hover) resolves `#door_total` (full price),
  `#door_price` (this click) and `#door_paid`. A payment is mirrored onto every entity of the link
  group, so both sides of every linked door agree; `doors/announce_progress` reports
  `<player> chipped in N points for <door> (paid/total)` to everyone, and the door opens on the
  chunk that reaches the total (announced with the total, not the last chunk).
- [x] Perks (`zombies/perks.py`): `mgs.zb.perk.partial` on the machine + per-player
  `mgs.zb.perkpaid.<perk_id>` objectives generated from `PERK_DEFINITIONS` and reset in
  `zombies/start`/`stop` next to the ownership resets. `perks/read_price` is the macro twin of the
  door one; `perks/store_progress` records the payment, `perks/announce_progress` reports
  `<Perk>: paid/total points paid` to the payer only. `perks/apply` clears the progress score, so
  a perk obtained any other way (random-perk power-up) voids it too and a re-buy after a down
  starts from zero.
- [x] Solo Quick Revive dynamic pricing: kept `paid` and compared against the *current* price, as
  suggested. Both `read_price` functions clamp remaining at 0, so a price that drops below the
  progress makes the next click free instead of refunding points.
- [x] Hovers: both show `Chip in: <chunk> points  (paid/total)` when enabled, the plain
  `Cost: <price> points` otherwise. The perk one shows the hovering player's own progress.
- [ ] Playtest: a linked multi-door paid by two players (both sides show the same progress, one
  announcement per chunk, opens on the last one); a perk machine where two players each build their
  own progress; the last chunk being a remainder (price not a multiple of `partial_price`); a
  chip-in Quick Revive while the solo discount flips on a player joining.


## 4. Zombies — new placeable: Der Wunderfizz (random perk machine)

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


## 5. Zombies — add the 8 missing perks

Perk definitions live in `PERK_DEFINITIONS` (`zombies/perks.py`); everything downstream
(scoreboards, apply/lose_all, info-paper lore, inventory mini-items, random-perk power-up)
is generated from it. Machine recolors: `src/database/others.py::override_model(<dye>)`
(accent = `<dye>_concrete`, accent2 = `<dye>_terracotta`) + one default-model line comment in
`perks.py` `setup_iter`. Editor: extend `FIELD_DOCS[("perk_machine","perk_id")]` list.

Color plan (user-picked; dyes already used: red=jugg, lime=speed, yellow=dtap, light_blue=QR,
green=mule, orange=stamin):
| Perk | Color wanted | Dye suggestion |
|---|---|---|
| PhD Flopper | purple | `purple` |
| Deadshot Daiquiri | really dark green | no darker vanilla green dye free (`green` is Mule Kick) → custom accent textures or `gray`+green accent2 — (HUMAN) taste call |
| Tombstone | brown | `brown` |
| Who's Who | cyan | `cyan` |
| Electric Cherry | dark blue | `blue` |
| Widow's Wine | black + red | two-tone: hand-written child model (accent=black_concrete, accent2=red_terracotta) instead of the single-dye helper |
| Timeslip | purple, lighter than PhD | `magenta` |
| Dying Wish | blue | `blue` taken by Cherry → custom texture or two-tone blue/white — (HUMAN) taste call |

- [ ] **PhD Flopper** — immune to explosions and fall damage.
  Fall: `attribute @s minecraft:fall_damage_multiplier base set 0` (removal: reset). Explosions:
  self-damage from our own grenades/launchers is dealt by the custom explosion path
  (`weapon/grenade.py` / `projectile.py`, `#grenade_explosion_power` / `#projectile_explosion_power` configs) — gate player damage there on the perk score; check trap fire too.
- [ ] **Deadshot Daiquiri** — +35% accuracy, −35% recoil.
  Accuracy: spread comes from `mgs:gun accuracy` (from `ACCURACY_BASE` stat) in the raycast path — scale by 0.65 when perk owned (pattern: a `mgs.special.*` score like Speed Cola's `quick_reload`). Recoil: `weapon/kick.py`, scale by 0.65 the same way.
- [ ] **Tombstone** — on going down, a tombstone marker (fake power-up) spawns at the down
  position; revived → it silently despawns; bled out → after the round-end respawn the player has
  **60 s** to reach it and recover **all perks + weapons** they had (BO2 uses ~90 s and excludes
  Tombstone itself from the recovery — follow that exclusion). Only the owner can see the pickup as
  theirs / collect it (id-match pattern: `revive.py` `downed_id` predicate or MB `mb.buyer` score).
  Hooks: snapshot perk scores in `revive/on_down` **before** `perks/lose_all` runs; snapshot
  `Inventory` to storage in `revive/bleed_out` (items survive the downed phase — they're only
  cleared by `give_respawn_loadout` at round respawn); spawn the marker entity in `on_down`,
  despawn in `revive_complete`, start the 60 s timer in `do_round_respawn`. No marker if the player
  died out of the map (`revive/full_death` path). Not a `powerups.py` drop — separate entity/tag so
  the shuffle-bag/pickup loop never touches it. Solo: BO2 disables Tombstone solo (a solo bleed-out
  is game over anyway) — hide/deny purchase when solo like the QR-solo special case.
- [ ] **Who's Who** — on going down, instead of the crawl/spectate flow the player keeps playing
  as a "doppelganger": teleported near (not at) their body with only knife + M1911, alive, and can
  revive their own mannequin (existing reviver proximity loop already works for any alive player).
  BO2 rules (wiki): revive succeeds → keep everything from before minus Who's Who; body bleeds out
  → keep playing as doppelganger with just the pistol (perks lost); down again *as* doppelganger →
  normal down; solo → doppelganger down = game over. Hooks: branch at `revive/on_down` (skip
  spectator+camera, still summon mannequin+HUD+bleed timer), snapshot perks/items like Tombstone.
  Mutual exclusion with Tombstone/Quick-Revive-solo interactions must be defined: suggest priority
  Who's Who > Tombstone (a Tombstone marker only spawns if Who's Who is not owned).
- [ ] **Electric Cherry** — electric shock around the player on reload; the emptier the magazine
  at reload start, the bigger the shock (radius+damage scale with `capacity - remaining_bullets`,
  read where the reload begins in `weapon/ammo.py`). Anti-spam (user spec, to confirm in play):
  after a shock, the next one requires 5 s cooldown + a genuinely full reload, OR fires again after
  a 10 s cooldown regardless. BO2 extra worth copying: emit one shock when the owner goes down.
  Visual: `electric_spark` particles + damage/stun (slowness) to zombies in radius.
- [ ] **Widow's Wine** — replaces the grenade slot with web grenades (`hotbar.7`):
  - Web grenade: new grenade weapon item (grenade framework: `GRENADE_TYPE` stat, `weapon/grenade.py`); explosion webs zombies — slow (heavy slowness or movement_speed modifier) for **20 s** (BO3 value), light damage.
  - Passive: when a zombie damages the owner and they have ≥1 web grenade, consume one → web burst centered on the player, no damage to the player (hook: `zombies/hurt_player.py::on_hurt`).
  - Melee: increased knife damage while owned (attribute pattern like `insta_kill_melee_on`, smaller value; BO3 also slows knifed zombies — optional).
  - Ammo rules: cannot be swapped away; any grenade wall-buy refills webs instead of the bought type (task 9's wall-buy work must respect this); Max Ammo refills to 4 (`inventory/replenish_grenades` + `bonus.py::max_ammo_grenades` currently hardcode `frag_grenade` when the slot is empty — parametrize by owned-perk).
- [ ] **Timeslip** — speed-ups (BO4 perk; no exact published numbers, user-decided multipliers):
  - Grenade/equipment throw cooldown reduced (grenade `COOLDOWN` stat is copied to the player score on throw — scale it, suggest ×0.5).
  - Mystery Box spin ×3 faster **for pulls bought by the owner**: initial `mb.anim` is 105 (`mystery_box.py::try_use`) — start it at ~35 or tick it 3×/tick for that display.
  - Pack-a-Punch animation ×3 faster: PAP timer is 300 ticks (`pap.py`, phase comments around line ~797) — same approach.
  - Trap cooldown ×0.75: cooldown starts at `zb.trap.cd_max` when deactivating (`traps.py`) — scale at activation when the activator owns Timeslip.
  - "Fast Travel" from BO4 has no equivalent system here — traps only.
- [ ] **Dying Wish** — instead of entering the downed state: 9 s Berserk (invulnerable, melee
  greatly increased — reuse the `insta_kill` melee attribute pattern), then left at 1 HP; per-use
  increasing cooldown. Wiki confirms 9 s / invuln / 1 HP / growing cooldown but publishes no
  numbers → suggest 60 s first use, +60 s each subsequent (bossbar or actionbar for cooldown).
  Hook: the down decision point — zombies deaths route `game.py::on_respawn` → `revive/on_down`;
  intercept there when off cooldown: teleport back to `LastDeathLocation`, restore, berserk,
  after 9 s set to 1 HP (skip `perks/lose_all` entirely on that path). Priority above Who's Who.

Shared checklist for EVERY perk above:
- [ ] `PERK_DEFINITIONS` entry (+ `commands`/`removal_commands` where the effect is attribute/score-based; `lose_all` and `zombies/stop` handle removal generated from it — verify stop resets any new `mgs.special.*` scores/attributes/tags it introduces).
- [ ] Machine model line in `others.py` + default-model mapping (automatic: `perks/override_perk_model` uses `perk_machine_$(perk_id)`).
- [ ] `FIELD_DOCS[("perk_machine","perk_id")]` list + task 6 price tooltip.
- [ ] Song wiring once assets exist (task 7).


## 6. Zombies — editor tooltips for perk machines

- [ ] Add `FIELD_DOCS[("perk_machine", "price")]` with the suggested prices (overrides the generic
  "price" fallback): Juggernog 2500 · Speed Cola 3000 · Double Tap 2000 · Quick Revive 1500 ·
  Stamin-Up 2000 · PhD Flopper 2000 · Deadshot Daiquiri 1500 · Mule Kick 4000 · Tombstone 2000 ·
  Who's Who 2000 · Electric Cherry 2000 · Widow's Wine 4000 · Timeslip 1500 · Dying Wish 4000.
- [ ] Document the random-perk pool behavior (task 4): tooltip on the perk machine (and the
  Wunderfizz element) explaining that the random-perk power-up / Wunderfizz draw from the perks
  placed on the map (unless the Wunderfizz `all_perks` option is set).


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


## 8. Zombies — Monkey Bombs (Mystery Box tactical)  [IMPLEMENTED — needs playtest + assets]

Reference (wiki): thrown, attracts all zombies for ~7 s, detonates ~9 s after the throw; up to 3
carried; replenished by Max Ammo. Stored in `hotbar.6`, limit 3 (item count), refilled ONLY by
Max Ammo or a wall-buy — not per-round.

- [x] Item: `monkey_bomb` (`config/stats.py::MONKEY_BOMB` + `database/grenades.py`) — grenade
  framework type `"monkey_bomb"`, 180t fuse, frag-style blast (damage 130 = BO ~1000 via the 2/15
  HP conversion, one-shots the horde to ~round 10). Carries `tactical:true` (routes wallbuy/
  inventory flows, excluded from the camo pipeline) + `stats.base_weapon` (box duplicate check).
- [x] Attraction: `zombies/monkey_bomb.py` — reuses the escort taxi (`escort.py`) instead of the
  old visible-iron-golem + fake-damage aggro hack. Twice a second the thrown monkey (`monkey/attract`,
  radius 40) redirects zombies that ALREADY have an escort by flagging their trader
  (`escort/redirect_to_monkey`) and starts fresh monkey-targeted escorts on the nearest un-escorted
  ones (`monkey/pull_one` → `escort/start` with `#zb_escort_mode 1`), capped by escort's
  `MAX_ESCORTS`. A monkey-flagged trader's `retarget` routes to `escort/retarget_monkey` (aims at the
  nearest `monkey_bomb`); `escort/zombie_tick` rides toward it (`monkey_ride`, skips the player
  releases) and releases within `MONKEY_RELEASE` (4) so the horde gathers on the monkey; the fuse
  blast then clears the crowd via the normal frag attribution (kill points work). Everything reverts
  automatically once the monkey is gone (zombie_tick drops the flag when no `monkey_bomb` remains).
  Hooks still live in `weapon/grenade.py` init/tick/detonate. Note: dogs are NOT attracted — the
  escort freezes its passenger with NoAI, which resets a wolf's max HP (see `escort.py`). ⚠ VERIFY
  IN-GAME: crowd gathering on the monkey looks right, escort budget not starved on big rounds.
  - Human feedback (addressed): visible iron golem removed entirely (no taunt entity now); zombies
    are pulled to the monkey through escort.py, handling both existing escorts (redirect their
    trader) and non-existing ones (start a capped monkey escort).
  - Human feedback #2 (addressed): *"some zombies are not really attracted, they chase me, stop,
    chase me, stop, while the monkey is 7-10 blocks beside"*. Cause: `escort/start` summons the
    trader **at the zombie**, so a zombie stood next to the player put an invisible trader inside the
    player's reach and escort's right-click safeguard (`discard_near_player`) deleted it within a
    tick or two. The pulse retried twice a second, and each abort froze the zombie (NoAI) then
    unfroze it facing the player with a 2 s speed boost — the stutter exactly. Then: *"make every
    zombie under the distance be escorted despite the limit, even if they are close to players"*.
    Now:
    - `monkey/attract` has **no `MAX_ESCORTS` gate and no `limit=`** on its candidate selector: every
      eligible zombie in the 40-block radius gets its own taxi. The cap bounds the cost of the
      stuck-rescue escorts, which run all game; a monkey lives ~9 s and a half-attracted crowd is
      worse than the extra traders. It does mean one wandering trader per zombie in radius, each
      pathing at `PATHFINDING_RANGE` — watch the tick rate on a big round.
    - Monkey traders are **exempt from `discard_near_player`**, so they may walk right into a
      player's face. Only monkey ones — the safeguard is unchanged for stuck-rescue escorts.
    - The click that exemption would cost is given back: `WanderingTrader.mobInteract` returns
      `CONSUME` on empty offers (`WanderingTrader.java:118`), and a right-click aimed at an entity
      never falls through to item use, so the gun silently didn't fire. The new
      `right_click_entity` advancement (`weapon/common.py`) catches
      `player_interacted_with_entity` on a `mgs.zb_escort` trader while holding a gun and runs the
      normal `set_pending_clicks` path. `CONSUME` carries `ItemContext.DEFAULT`, so `handleInteract`
      really does report the gun stack and the item predicate matches.
    - `TRADER_REACH_GUARD` (the safeguard radius) is its own constant now, but stays at **6**: entity
      reach is the `minecraft:entity_interaction_range` attribute, which zombies raises to **5** for
      its players — the vanilla 3 does not apply, so 6 is one block of margin, not three.
    - A monkey escort that gives up (`escort/give_up_monkey`) detaches quietly instead of falling
      through to the teleport rescue, which would have dropped the zombie next to a player — the
      opposite of the monkey's job — and instead of taking the `zb_escort_failed` flag, which only
      the teleport ever clears and would have locked that zombie out of escorts for the whole game.
  - Human feedback #3 (addressed): *"the zombie is escorted to the monkey, then the trader
    disappears (should not until the monkey explodes), so the zombie goes to me, then the trader
    reappears, the zombie goes to the monkey, etc."*. Cause: **arrival released the zombie**. The
    escort taxi was built for stuck rescue, where release hands a zombie to a player it can now see;
    at a monkey there is nothing to hold it — the monkey has no aggro of its own (the visible
    iron-golem fake-damage hack it replaced did), so `detach` turned it to face the nearest player,
    gave it a speed nudge, and vanilla `NearestAttackableTargetGoal` did the rest. It walked out past
    the 6-block re-grab floor, the next attract pulse grabbed it again — one trader summon/kill per
    round trip, which is the blinking the report describes. Now:
    - Arrival calls `escort/monkey_hold` instead of `escort/release`: the zombie stays frozen on its
      trader (NoAI, so it can't attack either) until the monkey is gone. Zombies freeze on first
      contact with `MONKEY_RELEASE`, i.e. spread around the monkey along their approach paths rather
      than stacking on it, and well inside the 7-block blast (`stats.py MONKEY_BOMB`).
    - `monkey_hold` deliberately skips `escort_tail`: standing still at the monkey is the goal, so
      the watchdog would otherwise call it stuck after 5 s and hand the zombie back. It refreshes the
      TTL and clears `stuck_ticks`, so the normal escort resumes on a clean window if the monkey
      vanishes without killing it (`zombie_tick` drops the trader's monkey flag then).
    - `give_up_monkey` now *also* holds rather than detaching: a trader that stalls short of the
      monkey was the second copy of the same loop (detach → runs at player → re-grabbed). Freezing
      the zombie where it stands is what the monkey is for anyway; it just misses the pile and
      survives the blast.
  - [ ] Playtest the above: crowd gathers **and stays** with a monkey thrown at your feet, no trader
    blinking, guns still fire while a monkey-escorted zombie is in your face, and the tick rate holds
    on a round-20+ horde.
  - [ ] Known side effect, unverified: the trader shares the zombie's exact hitbox, so a **knife
    swing** at a monkey-escorted zombie may land on the invisible (invulnerable) trader instead.
    Bullets are unaffected — the raycast skips `global.ignore`. If this bites, the fix is the same
    recovery trick on the attack path, or a pull that isn't the taxi at all: the only vanilla lever
    that outranks player targeting is `HurtByTargetGoal` (priority 1 vs 2, `Zombie.java:138-142`),
    i.e. an invisible living bait at the monkey plus a token `damage … by` tick — and that bait
    cannot be `Invulnerable`, since `canBeSeenAsEnemy()` is false for invulnerable entities and the
    target would drop instantly.
- [x] Mystery Box: pool entry + `default_give/monkey_bomb` → shared `wallbuys/give_tactical`
  (3 in `hotbar.6`, slot-tagged). Holding any monkeys = owned → rerolls like duplicate guns
  (`check_owned_result` + `capture_collected_name` now scan hotbar.6).
- [x] Max Ammo: `bonus.py::max_ammo_grenades` tops `hotbar.6` back to 3 (refill only, never grants).
- [ ] TODO: Don't make the monkey bomb roll like a grenade (exception)
- [ ] (HUMAN) model: first-pass cymbal monkey exists (`database/models/monkey_bomb.json`, vanilla
  brown-wool/gold/TNT textures) — adjust to taste.
- [ ] (HUMAN) sounds: real toy-jingle + explosion .oggs (placeholder note-block chimes cycle
  pitches each pulse, see `zombies/monkey/pulse`).


## 9. Zombies — wall-buys for non-gun items + equipment loadout refactor  [IMPLEMENTED — needs playtest]

Wall-buys now route by item KIND, probed once at setup from the display item's custom_data and
stored in `wallbuy_data.<id>.kind`: 0 gun (+magazine, unchanged flow) · 1 knife (`knife` key) ·
2 lethal grenade (`stats.grenade_type`) · 3 tactical (`tactical` key overrides grenade).

- [x] Editor: kind is derived, no new map field; `magazine_id` optional (pre-cleared at setup so a
  missing field can't leak); `FIELD_DOCS` for `weapon_id`/`magazine_id` document the non-gun ids.
- [x] Purchase flows (`wallbuys.py`, dispatched in `on_right_click` before the gun path):
  - `buy_knife` → replaces `hotbar.0`, no refill, denies if already owned. First knife item:
    **`bowie_knife`** (`database/others.py`, damage 153 = BO 1150 via 2/15 → one-hit kills to ~R11,
    netherite-sword texture placeholder, suggest ~3000 pts on maps);
  - `buy_lethal` → `hotbar.7` ×4; same-type = refill at `refill_price` (full → free deny),
    different type = replace at full price. Widow's Wine hook comment left in place (task 5);
  - `buy_tactical` → `hotbar.6` ×3, same rules; `give_tactical` is the silent shared core the
    Mystery Box uses. Kind-aware hover shows "(Refill)"/"(Owned)" suffixes.
- [x] Death consistency: `give_respawn_loadout` = starting loadout (clears bought knife/equipment)
  then frags cut to **2** — game start keeps 4.
- [x] Max Ammo parity: lethals to 4, tacticals to 3, both only when owned; per-round
  `replenish_grenades` (+2) stays lethal-only.
- [x] Empty-slot refills give the RIGHT lethal type. A per-player `mgs.zb.lethal_type` score
  (index into `config/stats.py::LETHAL_GRENADE_IDS`, 0=frag) is set on give (starting loadout=frag)
  and on a lethal wall-buy (`inventory/record_lethal_type`, from the bought `weapon_id`). When the
  slot is empty, `inventory/give_lethal_type`/`loot_replace_lethal` re-give that type — used by
  round-end `replenish_grenades` (count 2), `bonus/max_ammo_grenades` (count 4), and
  `recreate_critical_items` (recovery). Previously all three hardcoded `frag_grenade`.
- [ ] Playtest: knife/grenade/semtex/monkey wallbuys on a real map (place via editor with empty
  `magazine_id`), hover prices, refill/full/deny paths, slot enforcement after purchases.
  - Human feedback (addressed): bought semtex, used all, round ended → now gives 2 semtex, not 2
    frag. Cause was the empty-slot branch always giving frag; the ≥1-left path was already correct
    because it just increments the existing stack. Fixed via the `lethal_type` tracking above.


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

- Zombies: fast restart button in menu, AND when game ends (OP only as suggest command)

