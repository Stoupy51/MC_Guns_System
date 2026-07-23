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

Implemented in `src/functional/zombies/wunderfizz.py` (self-contained mini-spin, does NOT refactor the
Mystery Box internals). Editor element `wunderfizz` (slot `inventory.9`, `all_perks` flag, price 1500),
machine model `der_wunderfizz` (gold/purple), editor model-display + FIELD_DOCS added. Uses the
shared `zombies/perks/pool/*` helper for the "available perk" roll; on land the perk is collectable by the
buyer only for 10s (orb despawns after), sound = `music_box_short`. ⚠ Needs in-engine polish (orb float
visual is a simple hover, not the MB-style rise). Original spec kept below for reference.


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
- [x] **Tombstone** — DONE (`perks.py` tombstone_* + hooks in `revive.py`): on down a soul-skull marker
  spawns at the death spot with a perk snapshot; revived → discarded; bled out → inventory snapshotted, and
  after the round respawn a 60s marker lets the owner walk back to recover perks + weapons (Tombstone
  excluded). id-matched to the owner, disabled solo, no marker on full_death. Original spec below.
- [ ] ~~**Tombstone**~~ — on going down, a tombstone marker (fake power-up) spawns at the down
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
- [x] **Who's Who** — DONE (`whos_who.py`, self-contained; hooked from `revive/on_down` above Tombstone):
  co-op only; the owner keeps playing as an alive doppelganger (knife + pistol, `ww_active` tag) while their
  body drops as a revivable mannequin (id-matched, reuses the revive downed_id_match predicate). Any alive
  player (incl. the doppelganger) revives it → everything restored minus Who's Who; body bleeds out → fight
  on with the pistol (perks lost); down again as a doppelganger → normal down; solo → normal down (game
  over). ⚠ Needs in-engine verification. Original spec below.
- [ ] ~~**Who's Who**~~ — on going down, instead of the crawl/spectate flow the player keeps playing
  as a "doppelganger": teleported near (not at) their body with only knife + M1911, alive, and can
  revive their own mannequin (existing reviver proximity loop already works for any alive player).
  BO2 rules (wiki): revive succeeds → keep everything from before minus Who's Who; body bleeds out
  → keep playing as doppelganger with just the pistol (perks lost); down again *as* doppelganger →
  normal down; solo → doppelganger down = game over. Hooks: branch at `revive/on_down` (skip
  spectator+camera, still summon mannequin+HUD+bleed timer), snapshot perks/items like Tombstone.
  Mutual exclusion with Tombstone/Quick-Revive-solo interactions must be defined: suggest priority
  Who's Who > Tombstone (a Tombstone marker only spawns if Who's Who is not owned).
- [x] **Electric Cherry** — DONE (`perks.py` electric_cherry_* via the `on_reload` signal): discharge scales
  radius (2.5–6) + damage (40–100% of zombie max HP) with `capacity - remaining`. Anti-spam: 10s cooldown, or
  5s + a dry reload (gametime stamp). Also fires a full discharge when the owner goes down. Original spec below.
- [ ] ~~**Electric Cherry**~~ — electric shock around the player on reload; the emptier the magazine
  at reload start, the bigger the shock (radius+damage scale with `capacity - remaining_bullets`,
  read where the reload begins in `weapon/ammo.py`). Anti-spam (user spec, to confirm in play):
  after a shock, the next one requires 5 s cooldown + a genuinely full reload, OR fires again after
  a 10 s cooldown regardless. BO2 extra worth copying: emit one shock when the owner goes down.
  Visual: `electric_spark` particles + damage/stun (slowness) to zombies in radius.
- [x] **Widow's Wine** — DONE. Web grenade (`WEB_GRENADE` stat + `web_grenade` item, cobweb texture,
  `grenade/detonate_web` → `zombies/perks/widows_web_burst`: 20s heavy slowness + weakness + light damage).
  Passive web burst when hurt (`hurt_player` → `widows_on_hurt`, 2s cd, consumes a web). Melee bump via
  attack_damage attribute in the perk def. Lethal-slot routing: `loot_replace_lethal` + `buy_lethal_web`
  hand out webs for a Widow's Wine owner on every refill / Max Ammo / wall-buy. ⚠ Web-grenade art is a
  placeholder (reuses the frag model + a cobweb layer). Original spec below.
- [ ] ~~**Widow's Wine**~~ — replaces the grenade slot with web grenades (`hotbar.7`):
  - Web grenade: new grenade weapon item (grenade framework: `GRENADE_TYPE` stat, `weapon/grenade.py`); explosion webs zombies — slow (heavy slowness or movement_speed modifier) for **20 s** (BO3 value), light damage.
  - Passive: when a zombie damages the owner and they have ≥1 web grenade, consume one → web burst centered on the player, no damage to the player (hook: `zombies/hurt_player.py::on_hurt`).
  - Melee: increased knife damage while owned (attribute pattern like `insta_kill_melee_on`, smaller value; BO3 also slows knifed zombies — optional).
  - Ammo rules: cannot be swapped away; any grenade wall-buy refills webs instead of the bought type (task 9's wall-buy work must respect this); Max Ammo refills to 4 (`inventory/replenish_grenades` + `bonus.py::max_ammo_grenades` currently hardcode `frag_grenade` when the slot is empty — parametrize by owned-perk).
- [x] **Timeslip** — speed-ups (BO4 perk; no exact published numbers, user-decided multipliers). DONE:
  - Base speed factor is **×2**, not ×3 (only quantified reference "about half the time" ≈2×, matching
    the `music_box`→`music_box_short` jingle ratio). **Pack-a-Punch is the exception at ×3** (long anim).
  - Grenade/equipment throw cooldown **×0.5**: DONE — `raycast.py::raycast/main` halves the fire
    cooldown for the owner when the held weapon is a grenade (`stats.grenade_type` present).
  - Mystery Box spin **×2** for pulls bought by the owner: DONE — `mb.timeslip` flag stamped on the
    pull display at `mystery_box.py::try_use`, extra −1/tick in `spin_tick_one` (preserves the 104
    float trigger + exact anim==0 landing).
  - Pack-a-Punch animation **×3**: DONE — `pap.py` flags the machine `zb.pap.timeslip` off the owner at
    `anim/start`, and `game_tick` runs `anim/step` **three times per tick** for flagged machines
    (`anim/step_timeslip` = 2 extra gated steps). Stepping instead of decrementing-by-3 preserves every
    exact-tick phase trigger (298/280/252/225/205…). The jingle swaps to the 3× asset
    `jingle_sting_short` and the display slide interpolation shortens to 7t so the slides keep up.
    ⚠ In-engine timing polish (slide sync at 3×) still worth an eyeball, but logic is complete.
  - Trap cooldown **×0.75**: DONE — `traps.py::apply_timeslip_cd`, scaled at activation when the
    activator owns Timeslip.
  - "Fast Travel" from BO4 has no equivalent system here — traps only.
- [x] **Dying Wish** — DONE (`perks.py` dying_wish_* + `revive/on_down` intercept, highest priority):
  off cooldown, teleport back to the death spot, restore, 9s Berserk (resistance V + strength V + big melee
  attribute + speed), then left at 1 HP; skips lose_all. Escalating cooldown (60s × uses), ticked in
  `player/tick`. Original spec below.
- [ ] ~~**Dying Wish**~~ — instead of entering the downed state: 9 s Berserk (invulnerable, melee
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

- [x] Dying Wish: I was not at 1hp when the effect finished, I was at full health. Fix that.
      DONE — /data can't write player Health; dying_wish_end now clamps max_health to 1 then restores it.
  - Human update: I tried again, and no the player health is still not at 1 when the effect ends. Use a calculated /damage instead with a damage type that bypasses resistances.
- [x] Web grenades: it is bugged, sometimes the item displays stays frozen until I launch a new one. it also affect other projectiles (like monkey bomb when I throw them). Like it thinks there are no more items to tick.
      DONE — retired the fragile #grenade_count gate; grenade/tick now iterates @e[tag=grenade] directly.
- Der Wunderfizz: There is a lag spike when I retrieve the perk from the machine. I'm not sure it's for every perk machine or just the Der Wunderfizz. Find and optimize it! (remember the optimisation skill in this repo)
- Who's Who: Should work in Single player, and if the player died and have both Quick Revive and Who's Who in solo, Who's Who should have the priority.

