
# ruff: noqa: E501
# Revive System (Black Ops Zombies-style, mannequin-based)
# When a player takes lethal damage, they enter a "downed" state.
# A mannequin is spawned at their death location wearing their armor/skin.
# The player spectates the mannequin and can crawl (slow movement via WASD input predicates).
# Teammates revive by standing near the mannequin. After 30s without revive, player bleed out.
# Solo + Quick Revive: auto-revive after 10s, up to 3 times.
from stewbeet import JsonDict, Mem, Predicate, set_json_encoder, write_load_file, write_versioned_function

from ..helpers import MGS_TAG

# Revive configuration
BLEED_OUT_TICKS: int = 600		# 30 seconds to be revived before bleed out
REVIVE_TICKS: int = 60			# 3 seconds of proximity to revive
REVIVE_RANGE: float = 2.5		# Blocks range for revive interaction
QUICK_REVIVE_TICKS: int = 30	# 1.5 seconds with Quick Revive perk
SOLO_QR_TICKS: int = 200		# 10 seconds for solo Quick Revive auto-revive
SOLO_QR_MAX: int = 3			# Max solo Quick Revive uses per game
CRAWL_SPEED: float = 0.06		# Blocks per tick for downed crawl movement
# HUD text display height above mannequin
HUD_OFFSET_Y_THOUSANDTHS: int = 2000  # 2.0 blocks * 1000 (for scoreboard math)


def generate_revive() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Input predicates (used to move the mannequin via spectator player input)
	def player_input(key: str) -> JsonDict:
		return {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type_specific": {"type": "minecraft:player", "input": {key: True}}}}
	Mem.ctx.data[ns].predicates[f"v{version}/input/forward"]  = set_json_encoder(Predicate(player_input("forward")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/backward"] = set_json_encoder(Predicate(player_input("backward")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/left"]     = set_json_encoder(Predicate(player_input("left")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/right"]    = set_json_encoder(Predicate(player_input("right")))
	Mem.ctx.data[ns].predicates[f"v{version}/input/any"]      = set_json_encoder(Predicate({"condition": "minecraft:any_of", "terms": [player_input("forward"), player_input("backward"), player_input("left"), player_input("right")]}))

	## Scoreboards
	write_load_file(f"""
# Revive system scoreboards
scoreboard objectives add {ns}.zb.downed dummy
scoreboard objectives add {ns}.zb.bleed dummy
scoreboard objectives add {ns}.zb.revive_p dummy

# Solo Quick Revive uses remaining
scoreboard objectives add {ns}.zb.qr_uses dummy

# Unique downed ID: links player to their specific mannequin
scoreboard objectives add {ns}.zb.downed_id dummy
""")

	# ──────────────────────────────────────────────────────────────────────────
	## On Down: called from on_respawn when player dies in zombies
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/on_down", f"""
# Mark player as downed
scoreboard players set @s {ns}.zb.downed 1
scoreboard players set @s {ns}.zb.bleed {BLEED_OUT_TICKS}
scoreboard players set @s {ns}.zb.revive_p 0
tag @s add {ns}.downed_spectator

# Reset death counter (already set 0 by on_respawn caller, but be safe)
scoreboard players set @s {ns}.mp.death_count 0

# Read death position at full float precision (multiply by 1000, store as double 0.001)
execute store result score #rv_y_raw {ns}.data run data get entity @s LastDeathLocation.pos[1] 1000
scoreboard players add #rv_y_raw {ns}.data {HUD_OFFSET_Y_THOUSANDTHS}
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @s LastDeathLocation.pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @s LastDeathLocation.pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @s LastDeathLocation.pos[2] 1000
execute store result storage {ns}:temp rv_y_hud double 0.001 run scoreboard players get #rv_y_raw {ns}.data

# Assign a unique downed ID to this player and their mannequin
scoreboard players add #downed_id_next {ns}.data 1
scoreboard players operation @s {ns}.zb.downed_id = #downed_id_next {ns}.data

# Summon mannequin (crouching pose, invulnerable, temp tag for targeting)
summon minecraft:mannequin ~ ~ ~ {{Invulnerable:1b,pose:"swimming",hide_description:true,Tags:["{ns}.downed_mannequin","{ns}.downed_new","{ns}.gm_entity"]}}

# Copy the player's downed_id to the mannequin so we can find it uniquely later
scoreboard players operation @n[tag={ns}.downed_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id

# Copy player armor to mannequin
data modify entity @n[tag={ns}.downed_new] equipment set from entity @s equipment

# Copy player head item (which contains the profile component) to get their skin
# Use the get_username loot table to generate a player_head with profile, then copy profile from it
loot replace entity @n[tag={ns}.downed_new] weapon.mainhand loot {ns}:get_username
data modify entity @n[tag={ns}.downed_new] profile set from entity @n[tag={ns}.downed_new] equipment.mainhand.components."minecraft:profile"
item replace entity @n[tag={ns}.downed_new] weapon.mainhand with minecraft:air

# Summon text_display HUD above mannequin (temp tag, teleported below)
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.downed_hud","{ns}.downed_hud_new","{ns}.gm_entity"],billboard:"vertical",shadow:1b,see_through:0b,teleport_duration:1,transformation:{{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},text:[{{"selector":"@a[tag={ns}.downed_spectator,sort=nearest,limit=1]","color":"yellow"}},{{"text":" ↓","color":"yellow"}}]}}

# Teleport mannequin and HUD to death location
function {ns}:v{version}/zombies/revive/tp_to_death with storage {ns}:temp

# Remove temp tags so future queries don't accidentally match
tag @e[tag={ns}.downed_new] remove {ns}.downed_new
tag @e[tag={ns}.downed_hud_new] remove {ns}.downed_hud_new

# Player enters spectator mode
gamemode spectator @s

# Summon invisible item_display as camera vehicle (spectator will ride it for locked third-person view)
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.downed_cam","{ns}.downed_cam_new","{ns}.gm_entity"],teleport_duration:1}}

# Copy downed_id to camera entity for unique identification
scoreboard players operation @n[tag={ns}.downed_cam_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id

# Teleport camera to mannequin position (will be offset each tick)
execute as @n[tag={ns}.downed_mannequin] at @s run tp @n[tag={ns}.downed_cam_new] ^ ^2 ^-3
tag @e[tag={ns}.downed_cam_new] remove {ns}.downed_cam_new

# Mount the spectator player into the camera entity (locks them in place)
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[tag={ns}.downed_cam] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run tag @s add {ns}.downed_mine_temp
ride @s mount @n[tag={ns}.downed_mine_temp]
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

# Announce
title @s title [{{"text":"☠","color":"red"}}]
title @s subtitle [{{"text":"You are down! A teammate can revive you.","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"red"}},{{"text":" is down!","color":"gray"}}]
""")

	## Macro: teleport mannequin and HUD to death location
	write_versioned_function("zombies/revive/tp_to_death", f"""
$tp @n[tag={ns}.downed_new] $(rv_x) $(rv_y) $(rv_z)
$tp @n[tag={ns}.downed_hud_new] $(rv_x) $(rv_y_hud) $(rv_z)
""")

	## Macro: teleport revived player to the mannequin's last position
	write_versioned_function("zombies/revive/tp_revive_pos", """
$tp @s $(rv_x) $(rv_y) $(rv_z)
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Tick: process all downed spectating players
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/tick", f"""
# Process each spectating (downed) player
execute as @a[tag={ns}.downed_spectator,scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/revive/downed_tick
""")

	## Downed tick: per-player (run as the spectating downed player)
	write_versioned_function("zombies/revive/downed_tick", f"""
# Decrement bleed timer
scoreboard players remove @s {ns}.zb.bleed 1

# Third-person view: teleport camera item_display to 3 blocks behind and 2 above the mannequin
# Player rides the item_display, so camera follows it automatically
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run tag @s add {ns}.downed_mine_temp
execute as @n[tag={ns}.downed_mine_temp] at @s as @e[tag={ns}.downed_cam] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data at @n[tag={ns}.downed_mine_temp] run tp @s ^ ^2 ^-3
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

# Re-mount player onto camera entity every tick (ensures no accidental dismount)
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[tag={ns}.downed_cam] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run tag @s add {ns}.downed_mine_temp
ride @s mount @n[tag={ns}.downed_mine_temp]
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

# Sync mannequin yaw from player look direction — use downed_id to target correct mannequin
execute as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run tag @s add {ns}.downed_mine_temp
execute as @n[tag={ns}.downed_mine_temp] run data modify entity @s Rotation[0] set from entity @p[tag={ns}.downed_spectator] Rotation[0]
execute as @n[tag={ns}.downed_mine_temp] run data modify entity @s Rotation[1] set value 0.0f
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

# Move mannequin using Bookshelf motion (smooth, physics-based, no tp stuttering)
# Zero out velocity first, then accumulate based on active inputs
execute as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run scoreboard players set @s bs.vel.x 0
execute as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run scoreboard players set @s bs.vel.y 0
execute as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run scoreboard players set @s bs.vel.z 0

# Forward/backward: local +Z / -Z (scale: 80 = 0.08 blocks/tick at scale:0.001)
execute if entity @s[predicate={ns}:v{version}/input/forward] as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run scoreboard players set @s bs.vel.z {int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/backward] as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run scoreboard players set @s bs.vel.z -{int(CRAWL_SPEED * 1000)}

# Left/right: local +X / -X
execute if entity @s[predicate={ns}:v{version}/input/left] as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run scoreboard players set @s bs.vel.x {int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/right] as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run scoreboard players set @s bs.vel.x -{int(CRAWL_SPEED * 1000)}

# Convert local velocity (relative to mannequin facing) to canonical (world), then apply motion
execute as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data at @s rotated as @s run function #bs.move:local_to_canonical
execute as @e[tag={ns}.downed_mannequin] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run function #bs.move:set_motion {{scale:0.001}}

# Keep HUD text_display anchored 2 blocks above the mannequin
execute as @n[tag={ns}.downed_mannequin] at @s run tp @n[tag={ns}.downed_hud] ~ ~2 ~

# Check for revivers (alive non-downed players within range of mannequin)
scoreboard players set #zb_reviving {ns}.data 0
execute as @n[tag={ns}.downed_mannequin] at @s run execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE}] run scoreboard players set #zb_reviving {ns}.data 1

# Solo Quick Revive auto-revive: if no teammates in-game and player has quick_revive + uses left
execute if score #zb_reviving {ns}.data matches 0 if entity @s[tag={ns}.perk.quick_revive] unless score #zb_solo_revive_block {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/check_solo_qr

# If someone is reviving, increment progress; if not, decay
execute if score #zb_reviving {ns}.data matches 1.. run scoreboard players add @s {ns}.zb.revive_p 1
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.revive_p matches 1.. run scoreboard players remove @s {ns}.zb.revive_p 2

# Show bleed timer on downed player's actionbar ONLY when not in solo QR (which has its own actionbar)
# Compute display: whole seconds and tenths digit (sec = bleed/20, tenth = (bleed%20)/2)
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_sec {ns}.data = @s {ns}.zb.bleed
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_sec {ns}.data /= #20 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data = @s {ns}.zb.bleed
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data %= #20 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data /= #2 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run data modify storage smithed.actionbar:input message set value {{json:[{{"text":"☠ Bleeding out: ","color":"red"}},{{"score":{{"name":"#rv_disp_sec","objective":"{ns}.data"}},"color":"gray"}},{{"text":".","color":"gray"}},{{"score":{{"name":"#rv_disp_tenth","objective":"{ns}.data"}},"color":"gray"}},{{"text":"s","color":"dark_gray"}}],priority:"override",freeze:2}}
execute if score #zb_reviving {ns}.data matches ..1 run function #smithed.actionbar:message

# Show revive progress bar to nearby alive players (from mannequin position)
execute if score #zb_reviving {ns}.data matches 1 as @n[tag={ns}.downed_mannequin] at @s run execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE}] run function {ns}:v{version}/zombies/revive/show_reviver_bar

# Update HUD text_display color based on revive state / bleed timer
execute if score #zb_reviving {ns}.data matches 1.. run function {ns}:v{version}/zombies/revive/hud_white
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches 400.. run function {ns}:v{version}/zombies/revive/hud_orange
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches 200..399 run function {ns}:v{version}/zombies/revive/hud_gold
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.bleed matches ..199 run function {ns}:v{version}/zombies/revive/hud_red

# Check revive complete (Quick Revive threshold if reviver nearby has perk; normal otherwise)
# Use matches 1 (exactly) to exclude solo QR mode (which sets #zb_reviving=2)
execute if score #zb_reviving {ns}.data matches 1 if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE},tag={ns}.perk.quick_revive] if score @s {ns}.zb.revive_p matches {QUICK_REVIVE_TICKS}.. run function {ns}:v{version}/zombies/revive/revive_complete
execute if score #zb_reviving {ns}.data matches 1 unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE},tag={ns}.perk.quick_revive] if score @s {ns}.zb.revive_p matches {REVIVE_TICKS}.. run function {ns}:v{version}/zombies/revive/revive_complete

# Bleed out: time's up
execute if score @s {ns}.zb.bleed matches ..0 run function {ns}:v{version}/zombies/revive/bleed_out
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Solo Quick Revive check: auto-revive if alone in game
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/check_solo_qr", f"""
# Only trigger if there are no other alive in-game players besides this downed player
execute store result score #zb_other_alive {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]
execute if score #zb_other_alive {ns}.data matches 0 run function {ns}:v{version}/zombies/revive/solo_qr_tick
""")

	## Solo QR tick: auto-increment revive progress (uses {SOLO_QR_TICKS} ticks total)
	write_versioned_function("zombies/revive/solo_qr_tick", f"""
# Check player has uses remaining
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run return 0

# Signal solo reviving so decay logic is skipped (set #zb_reviving=2)
scoreboard players set #zb_reviving {ns}.data 2

# Increment revive_p at normal speed (1/tick)
scoreboard players add @s {ns}.zb.revive_p 1

# Show solo QR auto-revive actionbar
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚡ Solo Quick Revive: ","color":"aqua"}},{{"score":{{"name":"@s","objective":"{ns}.zb.revive_p"}},"color":"green"}},{{"text":"/{SOLO_QR_TICKS}t","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message

# Auto-revive once threshold reached
execute if score @s {ns}.zb.revive_p matches {SOLO_QR_TICKS}.. run function {ns}:v{version}/zombies/revive/solo_qr_complete
""")

	## Solo QR complete: consume one use then revive
	write_versioned_function("zombies/revive/solo_qr_complete", f"""
# Consume one Quick Revive use
scoreboard players add @s {ns}.zb.qr_uses 1

# If used up all 3, remove the Quick Revive perk
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tag @s remove {ns}.perk.quick_revive
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 0
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive used up! ({SOLO_QR_MAX}/{SOLO_QR_MAX})","color":"gray"}}]

# Proceed with revive
function {ns}:v{version}/zombies/revive/revive_complete
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Reviver actionbar (run as the reviving player, context @s = reviver, nearest downed = target)
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/show_reviver_bar", f"""
# Check if reviver has Quick Revive perk
execute if entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_normal
""")

	write_versioned_function("zombies/revive/show_reviver_bar_normal", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"Reviving... ","color":"yellow"}},{{"score":{{"name":"@p[tag={ns}.downed_spectator,sort=nearest,distance=..{REVIVE_RANGE}]","objective":"{ns}.zb.revive_p"}},"color":"green"}},{{"text":"/{REVIVE_TICKS}t","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/revive/show_reviver_bar_quick", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚡ Reviving... ","color":"aqua"}},{{"score":{{"name":"@p[tag={ns}.downed_spectator,sort=nearest,distance=..{REVIVE_RANGE}]","objective":"{ns}.zb.revive_p"}},"color":"green"}},{{"text":"/{QUICK_REVIVE_TICKS}t","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message
""")

	# ──────────────────────────────────────────────────────────────────────────
	## HUD color update helpers (run as downed spectator, update nearest downed_hud)
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/hud_white", f"""
data modify entity @n[tag={ns}.downed_hud] text[0] set value {{"selector":"@a[tag={ns}.downed_spectator,sort=nearest,limit=1]","color":"white"}}
data modify entity @n[tag={ns}.downed_hud] text[1] set value {{"text":" ↓","color":"white"}}
""")

	write_versioned_function("zombies/revive/hud_yellow", f"""
data modify entity @n[tag={ns}.downed_hud] text[0] set value {{"selector":"@a[tag={ns}.downed_spectator,sort=nearest,limit=1]","color":"yellow"}}
data modify entity @n[tag={ns}.downed_hud] text[1] set value {{"text":" ↓","color":"yellow"}}
""")

	write_versioned_function("zombies/revive/hud_gold", f"""
data modify entity @n[tag={ns}.downed_hud] text[0] set value {{"selector":"@a[tag={ns}.downed_spectator,sort=nearest,limit=1]","color":"gold"}}
data modify entity @n[tag={ns}.downed_hud] text[1] set value {{"text":" ↓","color":"gold"}}
""")

	write_versioned_function("zombies/revive/hud_red", f"""
data modify entity @n[tag={ns}.downed_hud] text[0] set value {{"selector":"@a[tag={ns}.downed_spectator,sort=nearest,limit=1]","color":"red"}}
data modify entity @n[tag={ns}.downed_hud] text[1] set value {{"text":" ↓","color":"red"}}
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Revive complete: restore the downed player (run as downed spectator)
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/revive_complete", f"""
# Remove downed state
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Store mannequin position before killing it
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @n[tag={ns}.downed_mannequin] Pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @n[tag={ns}.downed_mannequin] Pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @n[tag={ns}.downed_mannequin] Pos[2] 1000

# Kill mannequin, HUD display, and camera entity
kill @n[tag={ns}.downed_mannequin]
kill @n[tag={ns}.downed_hud]
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[tag={ns}.downed_cam] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run kill @s

# Dismount from camera entity and restore adventure mode
ride @s dismount
gamemode adventure @s

# Teleport player to where the mannequin was
function {ns}:v{version}/zombies/revive/tp_revive_pos with storage {ns}:temp

# Restore max health (check for Juggernog perk)
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Heal to full and re-apply saturation
effect give @s minecraft:instant_health 1 255 true
effect give @s minecraft:saturation infinite 255 true

# Announce
title @s title [{{"text":"❤","color":"green"}}]
title @s subtitle [{{"text":"You have been revived!","color":"green"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" has been revived!","color":"gray"}}]
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Bleed out: player couldn't be revived in time (run as downed spectator)
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/bleed_out", f"""
# Remove downed state
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Kill mannequin, HUD display, and camera entity
kill @n[tag={ns}.downed_mannequin]
kill @n[tag={ns}.downed_hud]
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[tag={ns}.downed_cam] if score @s {ns}.zb.downed_id = #my_downed_id {ns}.data run kill @s

# Dismount then enter full spectator mode to watch until next round
ride @s dismount
gamemode spectator @s

# Spectate a random alive in-game player
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] run spectate @s
# Fallback if no alive players: teleport spectator somewhere reasonable
execute unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run tp @s ~ ~ ~

# Announce
title @s title [{{"text":"☠","color":"dark_red"}}]
title @s subtitle [{{"text":"You bled out. Respawning next round...","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"dark_red"}},{{"text":" has bled out.","color":"gray"}}]
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Round end respawn: revive all spectating (bled-out) players
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/revive/round_respawn", f"""
# Respawn all spectator (bled-out) players
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=spectator] run function {ns}:v{version}/zombies/revive/do_round_respawn
""")

	write_versioned_function("zombies/revive/do_round_respawn", f"""
# Restore adventure mode
spectate @s
gamemode adventure @s

# Teleport to random player spawn
function {ns}:v{version}/zombies/respawn_tp

# Re-apply saturation and heal
effect give @s minecraft:saturation infinite 255 true
effect give @s minecraft:instant_health 1 255 true

# Restore max health (check for Juggernog perk)
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Re-give starting weapon on respawn
function {ns}:v{version}/zombies/inventory/give_respawn_loadout

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" has respawned!","color":"gray"}}]
""")

	# ──────────────────────────────────────────────────────────────────────────
	## Hook: reset revive state on game start
	# ──────────────────────────────────────────────────────────────────────────
	write_versioned_function("zombies/start", f"""
# Reset revive state
scoreboard players set @a {ns}.zb.downed 0
scoreboard players set @a {ns}.zb.bleed 0
scoreboard players set @a {ns}.zb.revive_p 0
scoreboard players set @a {ns}.zb.qr_uses 0
scoreboard players set @a {ns}.zb.downed_id 0
scoreboard players set #downed_id_next {ns}.data 0
tag @a remove {ns}.downed_spectator
kill @e[tag={ns}.downed_mannequin]
kill @e[tag={ns}.downed_hud]
kill @e[tag={ns}.downed_cam]
""")

	## Hook: reset revive state on game stop
	write_versioned_function("zombies/stop", f"""
# Reset revive state
scoreboard players set @a {ns}.zb.downed 0
scoreboard players set @a {ns}.zb.bleed 0
scoreboard players set @a {ns}.zb.revive_p 0
scoreboard players set @a {ns}.zb.qr_uses 0
scoreboard players set @a {ns}.zb.downed_id 0
scoreboard players set #downed_id_next {ns}.data 0
tag @a remove {ns}.downed_spectator
kill @e[tag={ns}.downed_mannequin]
kill @e[tag={ns}.downed_hud]
kill @e[tag={ns}.downed_cam]
""")

