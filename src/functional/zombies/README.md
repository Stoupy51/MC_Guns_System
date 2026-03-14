# Zombies Implementation Plan

This document describes how each map element from the editor is implemented (or needs to be implemented) in the zombies game system.

## Map Data Structure

Each element is stored as a **zb_object** compound in `mgs:maps zombies[].{save_path}[]`:
```
{pos:[x,y,z], rotation:[yaw,0.0f], group_id:N, ...type-specific fields}
```
Coordinates are **relative** to `base_coordinates`. At game start, they are converted to absolute coordinates using the base offset.

---

## Element Overview

| Element | Save Path | Fields | Status |
|---|---|---|---|
| zombie_spawn | `spawning_points.zombies` | group_id (for area gating) | ✅ Spawning works, ❌ Needs proximity-based selection |
| player_spawn_zb | `spawning_points.players` | group_id (for area gating) | ✅ Implemented |
| wallbuy | `wallbuys` | price, refill_price, refill_price_pap, weapon_id | ❌ Not implemented |
| door | `doors` | price, link_id, back_group_id, block, animation, sound | ❌ Not implemented |
| trap | `traps` | price, type, duration, cooldown, effect_radius, offset_pos, power | ❌ Not implemented |
| perk_machine | `perks` | price, perk_id, power | ❌ Not implemented |
| mystery_box_pos | `mystery_box.positions` | can_start_on | ✅ Partially (positions work, compound format & animation need update) |
| power_switch | `power_switch` | (none) | ❌ Not implemented |

---

## Interaction System

All interactive elements (wallbuys, doors, traps, perk machines, mystery box, power switch) use `minecraft:interaction` entities paired with the **Bookshelf interaction module** for event detection:
- **Right click**: Primary purchase/activation
- **Hover enter/leave**: Show/hide title + subtitle with element info and price
- Reference: https://docs.mcbookshelf.dev/en/master/modules/interaction/

---

## Group System (`group_id`)

**Purpose**: Groups define map areas that are progressively unlocked by purchasing doors. Only `zombie_spawn` and `player_spawn_zb` elements use `group_id` for runtime gating.

**How it works**:
- Zombie spawns and player spawns have a `group_id` (default 0 = starting area)
- Doors have a `back_group_id` — when a door is opened, it unlocks the corresponding group
- **Starting area** (group 0): Always accessible
- **Locked areas** (group 1, 2, ...): Spawns in these groups only activate when unlocked

**Door ↔ Group Interaction** (bidirectional doors):
- Door A has `group_id: 1`, Door B has `group_id: 2`, Door B has `back_group_id: 1`
- Buy Door B from Door A's zone → unlocks group 2 (normal: door's group_id)
- Buy Door A from Door B's zone → unlocks group 1 (Door B's back_group_id, since group 2 is already unlocked)

**Runtime tracking**:
- Storage list: `mgs:zombies game.unlocked_groups` → `[0]` initially
- When a door is bought → append its `group_id` (and `back_group_id` if applicable) to unlocked list
- Spawn filtering: Only spawn zombies from points whose `group_id` is in `unlocked_groups`
- Player respawn: Can use any player spawn whose `group_id` is unlocked

---

## Already Implemented

### Zombie Spawn (`spawning_points.zombies`)
- **Current**: Picks a random spawn point from all available spawns
- **Needs update**: Proximity-based selection — pick nearest spawns within 32 blocks of any player first, fallback to 96 blocks if none found. Also filter by `group_id` in `unlocked_groups`

### Player Spawn (`spawning_points.players`)
- **Game start**: `summon_spawns` reads compounds, summons `minecraft:marker` entities with tag `mgs.spawn_zb_player` and yaw data
- **Spawning**: `pick_spawn` selects a random spawn marker in an unlocked group

### Mystery Box Positions (`mystery_box.positions`)
- **Current**: `setup_positions` reads `[x,y,z]` arrays and summons `minecraft:interaction` entities
- **Needs update**:
  - Read `pos` from compound instead of direct array
  - Use `can_start_on` to filter eligible positions for initial active box
  - **Animation**: Item display with transformations and interpolation for weapon cycling (see https://minecraft.wiki/w/Item_display#Interpolation)
  - Items should float up and cycle using `start_interpolation` + `interpolation_duration` on the display entity's `transformation`
  - Also need animation for box moving to another place

---

## To Implement

### 1. Power Switch (`power_switch`)

**Concept**: A wall lever that enables power for the entire map. Elements with `power: true` (perk machines, traps) only become active after power is turned on.

**Data**: `game.map.power_switch[]` — compounds with `pos`, `rotation`, `group_id`

**Implementation** (in `game.py`):
- **Scoreboard**: `#zb_power mgs.data` — 0 = off, 1 = on
- **Game start**:
  - Set `#zb_power mgs.data 0`
  - For each power switch position: place a `minecraft:lever[face=wall,facing=north,powered=false]` block (with proper facing) and summon a `minecraft:interaction` entity with tag `mgs.power_switch`
- **Tick**: Check for interaction on power switches. On interact:
  - Set `#zb_power mgs.data 1`
  - Particle: `minecraft:electric_spark` at each power switch position
  - Sound: `minecraft:entity.firework_rocket.twinkle_far`
  - Announce "⚡ Power is ON!"
  - Kill the power switch interaction entities (one-time use)
  - Toggle the lever block state

**Functions**:
- `zombies/power/setup` — Iterate `game.map.power_switch`, place levers, summon interaction entities
- `zombies/power/check_use` — Detect interaction, enable power
- `zombies/power/on_activate` — Set scoreboard, particles, sound, announce, cleanup

---

### 2. Doors (`doors`)

**Concept**: Physical block barriers that players purchase to open. All door elements sharing the same `link_id` are opened together. Opening doors unlocks new areas via the group system.

**Data per door**:
- `price`: Cost to open (default 1000, shared across link_id group)
- `link_id`: Groups door blocks together (all with same link_id open at once)
- `back_group_id`: Group to unlock from the other side (-1 = none)
- `block`: Block type to place/remove (captured from offhand during editor placement)
- `animation`: 0 = `setblock destroy` (default), 1 = `setblock air` (silent), 2 = block_display launch animation
- `sound`: Custom sound on open (empty = use default setblock destroy sound)

**Implementation** (new file or in `game.py`):
- **Game start**: Iterate `game.map.doors`, for each compound:
  - Convert relative→absolute position
  - Place the `block` at the absolute position (rebuild barrier)
  - Summon `minecraft:interaction` entity with data compound and tags `mgs.door`, `mgs.gm_entity`
- **Interaction** (Bookshelf right-click):
  - Check if player has enough points >= price
  - Deduct price
  - Find all door entities with matching `link_id`
  - For each matching door:
    - Remove block based on `animation` type:
      - 0: `setblock destroy` (particles + default sound)
      - 1: `setblock air`
      - 2: Summon `block_display` at position, `setblock air`, apply transformation to launch block into the sky
    - Play custom `sound` if set
    - Kill the door interaction entity
  - Unlock group: append door's `group_id` to `game.unlocked_groups`
  - Handle `back_group_id` if applicable
  - Announce
- **Hover** (Bookshelf hover enter/leave): Show/hide title with door price

**Functions**:
- `zombies/doors/setup` — Iterate door compounds, place blocks, summon entities
- `zombies/doors/check_use` — Detect interaction, validate points
- `zombies/doors/try_open` — Deduct points, open all doors with same link_id
- `zombies/doors/open_one` — Per-entity: remove block (animation-dependent), kill self
- `zombies/doors/on_hover` — Show title with price
- `zombies/doors/on_hover_leave` — Clear title

---

### 3. Zombie Spawn Update (Proximity-Based Selection)

**Current problem**: Random spawn selection doesn't consider player proximity — zombies may spawn too far away.

**New algorithm**:
1. For each spawn point, calculate distance to nearest player
2. First pass: collect spawns within 32 blocks of any player
3. If none found: expand to 64 blocks
4. If still none: use any available spawn (fallback)
5. Pick random from the filtered set
6. Only consider spawns whose `group_id` is in `unlocked_groups`

**Functions to update**:
- `zombies/spawn_zombie` — Replace random index selection with proximity filter
- New: `zombies/find_nearby_spawn` — Score-based proximity check

---

### 4. Wallbuys (`wallbuys`)

**Concept**: Wall-mounted weapon stations. Players interact to buy a weapon. If already owned, refill ammo instead.

**Data per wallbuy**:
- `price`: Cost to buy (default 1000)
- `refill_price`: Ammo refill cost (default 500)
- `refill_price_pap`: PAP refill cost (default 4500)
- `weapon_id`: Weapon ID string (e.g. "m1911")

**Implementation**:
- **Game start**: Iterate `game.map.wallbuys`, for each compound:
  - Convert relative→absolute position
  - Summon `minecraft:interaction` entity with tags `mgs.wallbuy`, `mgs.gm_entity`
  - Store wallbuy data on entity
  - Summon `minecraft:item_display` at the same position showing the weapon:
    - `loot replace entity @s contents loot mgs:i/{weapon_id}` (or use loot table from compound)
    - Apply rotation from wallbuy yaw
    - Visual: item floating on the wall
- **Interaction** (Bookshelf right-click):
  - Read weapon_id from interaction entity data
  - Check if player already owns this weapon → refill ammo for `refill_price` (or `refill_price_pap` if PAP)
  - Otherwise buy weapon for `price`
  - Give weapon via loot table
- **Hover** (Bookshelf): Show weapon name + price via title/subtitle
- **No text_display needed** — hover events handle info display

**Functions**:
- `zombies/wallbuys/setup` — Iterate compounds, summon interaction + item_display entities
- `zombies/wallbuys/check_use` — Detect interaction, process purchase
- `zombies/wallbuys/try_buy` — Check points, buy vs refill, give weapon
- `zombies/wallbuys/give_weapon` — Macro: give weapon by ID
- `zombies/wallbuys/on_hover` — Show title with weapon name and price
- `zombies/wallbuys/on_hover_leave` — Clear title

---

### 5. Traps (`traps`)

**Concept**: Area-of-effect devices. Player activates for a cost, trap deals damage in radius for duration, then enters cooldown. Requires power if `power: true`.

**Data per trap**:
- `price`: Activation cost (default 1000)
- `type`: 0 = fire enemies, 1 = electric (oneshots non-boss mobs)
- `duration`: Active duration in ticks (default 200 = 10s)
- `cooldown`: Cooldown in ticks (default 1200 = 60s)
- `effect_radius`: [x, y, z] cuboid radius
- `offset_pos`: [x, y, z] offset from trap center to interaction entity position
- `power`: Requires power (default true)

**Implementation**:
- **Game start**: Iterate `game.map.traps`, summon entities:
  - `minecraft:interaction` at position + `offset_pos` (the button/switch location)
  - `minecraft:marker` at position (the trap center for effect area)
  - Tags: `mgs.trap`, `mgs.gm_entity`
  - Store trap data on entities
- **Interaction** (Bookshelf right-click):
  - Check `power` requirement (`#zb_power`)
  - Check trap is inactive and not on cooldown
  - Deduct `price`
  - Start trap: set duration timer on entity
- **Active tick** (while timer > 0):
  - Damage all `mgs.zombie_round` entities within `effect_radius` of trap center
  - Type 0 (fire): apply fire damage
  - Type 1 (electric): instant kill non-boss mobs
  - Particle effects at trap center
  - Decrement timer
- **Deactivation**: Timer reaches 0 → start cooldown timer
- **Cooldown tick**: Decrement cooldown, show "Recharging" via hover
- **Hover**: Show trap info, price, and status (ready/active/recharging)

**Functions**:
- `zombies/traps/setup` — Iterate trap compounds, summon interaction + marker entities
- `zombies/traps/check_use` — Detect interaction, validate power/points/state
- `zombies/traps/activate` — Start trap with duration timer
- `zombies/traps/tick` — Process active traps (damage, particles, timers)
- `zombies/traps/deactivate` — Start cooldown
- `zombies/traps/on_hover` — Show trap info via title

---

### 6. Perk Machines (`perks`)

**Concept**: Stationary machines where players buy gameplay-enhancing perks. Requires power if `power: true`. When a perk is bought, calls `#mgs:zombies/on_new_perk` function tag for extensibility.

**Available perks** (stored as `perk_id` string):
- `"juggernog"` — Increased max health (40 HP instead of 20)
- `"speed_cola"` — Faster reload speed
- `"double_tap"` — Increased fire rate / damage
- `"quick_revive"` — Enables revival of downed teammates (hold right-click near downed player to revive, BO2 style)

**Data per perk machine**:
- `price`: Cost (default 2500)
- `perk_id`: Which perk this machine gives
- `power`: Requires power (default true)

**Implementation**:
- **Game start**: Iterate `game.map.perks`, summon `minecraft:interaction` entities
  - Tags: `mgs.perk_machine`, `mgs.gm_entity`
  - Store perk data on entity
- **Interaction** (Bookshelf right-click):
  - Check `power` requirement
  - Check if player already has this perk (`mgs.zb.perk.{perk_id}`)
  - Deduct price
  - Set `mgs.zb.perk.{perk_id} = 1` for the player
  - Apply perk effects:
    - **Juggernog**: `attribute @s max_health base set 40`, heal to full
    - **Speed Cola**: Set tag/scoreboard for reload system
    - **Double Tap**: Set tag/scoreboard for damage system
    - **Quick Revive**: Enable revival ability for this player
  - Call `#mgs:zombies/on_new_perk` function tag
  - Visual/audio feedback
- **Hover**: Show perk name + price via title/subtitle

**Revival System (Quick Revive / BO2 Style)**:
- When a player is downed (health reaches 0), they enter a **"Last Stand"** state instead of instant death:
  - Player falls prone (crawling speed, heavily restricted movement)
  - 30-second bleedout timer starts
  - If another player with Quick Revive holds right-click near the downed player for ~3 seconds, the downed player is revived with partial health
  - If timer expires → player goes to spectator (current death system)
  - Without Quick Revive: no one can revive, bleedout always happens
  - This replaces the current instant-spectate death system

**Functions**:
- `zombies/perks/setup_machines` — Iterate perk compounds, summon interaction entities
- `zombies/perks/check_machine_use` — Detect interaction, validate
- `zombies/perks/buy_perk` — Macro: dispatch by perk_id
- `zombies/perks/apply_{perk_id}` — Per-perk logic (juggernog, speed_cola, double_tap, quick_revive)
- `zombies/perks/on_hover` — Show perk info
- `zombies/revival/tick` — Check for downed players, process revival progress
- `zombies/revival/start_revive` — Begin reviving a downed player
- `zombies/revival/complete` — Revive the player

---

### 7. Mystery Box Update

**Current state**: Works with simple `[x,y,z]` arrays.
**Needed updates**:
- Read `pos` from compound instead of direct array
- Use `can_start_on` to filter initial active box position
- **Animation overhaul** using `item_display` with transformations and interpolation:
  - When box opens: item_display spawns inside, transforms upward (float out of box)
  - Weapon cycling: update display item rapidly during cycling phase
  - Final reveal: smooth interpolation to final position
  - Uses `start_interpolation` + `interpolation_duration` on display entity
  - Reference: https://minecraft.wiki/w/Item_display#Interpolation

**Functions to update**:
- `zombies/mystery_box/setup_positions` — Read compound format
- `zombies/mystery_box/spawn_display` — Use transformation-based animation
- `zombies/mystery_box/cycle_display` — Animate with interpolation
- `zombies/mystery_box/show_result` — Final reveal animation

---

## Implementation Priority

1. **Power Switch** — Simple, foundational (gates perks and traps)
2. **Doors + Group System** — Core progression mechanic (gates areas, unlocks spawns)
3. **Zombie Spawn Update** — Proximity-based selection + group filtering
4. **Wallbuys** — Primary economy sink, weapon acquisition, item_display visuals
5. **Perk Machines + Revival System** — Gameplay perks, BO2-style revival
6. **Traps** — Area control with offset interaction pos
7. **Mystery Box Update** — Compound format migration + animation overhaul




We need proper inventory management.
Currently we have a starting pistol and that's all. Which is VERY wrong.
Taking inspiration of Black Ops 2, I want:
- hotbar.0 : knife (iron_sword currently)
- hotbar.1 : starting weapon (m1911)
- inventory.1 : starting weapon's magazine. (issue: it's only 7 bullets for m1911. To fix this, we'll modify magazine data to have 8 times the normal amount of bullets max. The current ammo count in the magazine should be exactly half of the magazine max (This half-count rule will be applied only to the starting weapon))
- hotbar.2 : starting empty
- inventory.2 : will store weapon's magazines
- hotbar.3 : third weapon (if mule_kick perk)
- inventory.3 : will store weapon's magazines
- hotbar.7: main throwable (frag_grenade): starting with 4 and +2 every round (max count is 4)
- hotbar.6: secondary throwable (empty by default): none for now, but keep in mind we'll use it
- hotbar.8: player info item (lore contains all information: weapons, magazines, equipments, perks, passive, ability (used or not this round))
- hotbar.4: use ability item (if not automatic, the player can use its ability) (lore with all information about the ability <= This enhance the need of an ability.py module for centralizing information and other stuff)
- Prevent any drop and moving item in inventory (inventory_changed advancement that will check the inventory logic!)
  - If dropped magazine, move it back to player's inventory (execute as item on origin)
  - Take every case!! (like swapping slot 1 & 2, etc.)

