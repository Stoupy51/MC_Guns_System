
# ruff: noqa: E501
# Zombies Round System
# Wave-based round progression with zombie spawning, scaling, and round completion.
from stewbeet import Mem, write_versioned_function


def generate_zombies_rounds() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Round System ──────────────────────────────────────────────

	## Start a new round
	write_versioned_function("zombies/start_round", f"""
# Increment round number
execute store result score #zb_round {ns}.data run data get storage {ns}:zombies game.round
scoreboard players add #zb_round {ns}.data 1
execute store result storage {ns}:zombies game.round int 1 run scoreboard players get #zb_round {ns}.data

# Calculate zombies to spawn this round: base formula = round * 4 + (player_count - 1) * 2
execute store result score #zb_player_count {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
scoreboard players remove #zb_player_count {ns}.data 1
scoreboard players operation #zb_player_count {ns}.data *= #2 {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data = #zb_round {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data *= #4 {ns}.data
scoreboard players operation #zb_to_spawn {ns}.data += #zb_player_count {ns}.data

# Store zombies to spawn and remaining count
scoreboard players operation #zb_remaining {ns}.data = #zb_to_spawn {ns}.data

# Set spawn timer (spawn a zombie every 2 seconds = 40 ticks)
scoreboard players set #zb_spawn_timer {ns}.data 20

# Grace period: don't check game over for 3 seconds (60 ticks)
scoreboard players set #zb_round_grace {ns}.data 60

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 40 10
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"Round ","color":"red","bold":true}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}}]

# Signal round start
function #{ns}:zombies/on_round_start

# Refresh sidebar
function {ns}:v{version}/zombies/refresh_sidebar

# Announce
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"red"}},{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" has begun!","color":"red"}}]
""")

	## Spawn a single zombie using proximity-based selection from spawn markers
	write_versioned_function("zombies/spawn_zombie", f"""
# Tag nearby unlocked zombie spawns
# First pass: 32 blocks from any alive player
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked,distance=..32] add {ns}.zb_near

# Second pass: 64 blocks if none found
execute unless entity @e[tag={ns}.zb_near] as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] at @s run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked,distance=..64] add {ns}.zb_near

# Fallback: any unlocked spawn
execute unless entity @e[tag={ns}.zb_near] run tag @e[tag={ns}.spawn_zb,tag={ns}.spawn_unlocked] add {ns}.zb_near

# Pick random from tagged set and spawn
execute as @n[tag={ns}.zb_near,sort=random] at @s run function {ns}:v{version}/zombies/do_spawn_zombie

# Cleanup
tag @e[tag={ns}.zb_near] remove {ns}.zb_near
""")

	## Actually spawn the zombie at the marker position (@s = spawn marker, at @s)
	write_versioned_function("zombies/do_spawn_zombie", f"""
# Store position for macro
execute store result storage {ns}:temp _zpos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _zpos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _zpos.z double 1 run data get entity @s Pos[2]

# Determine zombie level based on round
# Rounds 1-5: level 1, 6-10: level 2, 11-15: level 3, 16+: level 4
execute if score #zb_round {ns}.data matches ..5 run data modify storage {ns}:temp _zpos.level set value "1"
execute if score #zb_round {ns}.data matches 6..10 run data modify storage {ns}:temp _zpos.level set value "2"
execute if score #zb_round {ns}.data matches 11..15 run data modify storage {ns}:temp _zpos.level set value "3"
execute if score #zb_round {ns}.data matches 16.. run data modify storage {ns}:temp _zpos.level set value "4"

# Spawn the zombie
function {ns}:v{version}/zombies/summon_zombie_at with storage {ns}:temp _zpos
""")

	## Summon zombie at absolute position (macro)
	write_versioned_function("zombies/summon_zombie_at", f"""
# Summon a regular zombie (not armed)
$summon minecraft:zombie $(x) $(y) $(z) {{Tags:["{ns}.zombie_round","{ns}.gm_entity","{ns}.nukable"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty"}}

# Scale health based on round level
$execute as @n[tag={ns}.zombie_round,tag=!{ns}.zb_scaled] run function {ns}:v{version}/zombies/scale_zombie {{level:"$(level)"}}
""")

	write_versioned_function("zombies/scale_zombie", f"""
tag @s add {ns}.zb_scaled

$scoreboard players set #zb_level {ns}.data $(level)

# Level 1: default 20 HP (rounds 1-5) — no changes needed
# Level 2: 30 HP (rounds 6-10)
execute if score #zb_level {ns}.data matches 2 run attribute @s minecraft:max_health base set 30
execute if score #zb_level {ns}.data matches 2 run data modify entity @s Health set value 30f

# Level 3: 40 HP (rounds 11-15)
execute if score #zb_level {ns}.data matches 3 run attribute @s minecraft:max_health base set 40
execute if score #zb_level {ns}.data matches 3 run data modify entity @s Health set value 40f

# Level 4: 60 HP (rounds 16+)
execute if score #zb_level {ns}.data matches 4 run attribute @s minecraft:max_health base set 60
execute if score #zb_level {ns}.data matches 4 run data modify entity @s Health set value 60f

# Increase speed slightly at higher levels
execute if score #zb_level {ns}.data matches 3 run attribute @s minecraft:movement_speed base set 0.26
execute if score #zb_level {ns}.data matches 4 run attribute @s minecraft:movement_speed base set 0.30
""")

	## Spawn tick: spawn zombies on a timer
	write_versioned_function("zombies/spawn_tick", f"""
# Decrease spawn timer
scoreboard players remove #zb_spawn_timer {ns}.data 1
execute if score #zb_spawn_timer {ns}.data matches 1.. run return 0

# Reset timer (spawn every 1 tick)
scoreboard players set #zb_spawn_timer {ns}.data 1

# Spawn a zombie
function {ns}:v{version}/zombies/spawn_zombie

# Decrease count to spawn
scoreboard players remove #zb_to_spawn {ns}.data 1
""")

	# Round Completion ──────────────────────────────────────────

	write_versioned_function("zombies/round_complete", f"""
# Guard: prevent re-triggering every tick
scoreboard players set #zb_to_spawn {ns}.data -1

# Signal round end
function #{ns}:zombies/on_round_end

# Title
title @a[scores={{{ns}.zb.in_game=1}}] times 10 40 10
title @a[scores={{{ns}.zb.in_game=1}}] title [{{"text":"Round Complete!","color":"green","bold":true}}]

# Give all players 500 bonus points for surviving the round
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run scoreboard players add @s {ns}.zb.points 500

# Announce
execute store result score #completed_round {ns}.data run data get storage {ns}:zombies game.round
tellraw @a ["",{{"text":"","color":"dark_green","bold":true}},"🧟 ",{{"text":"Round ","color":"green"}},{{"score":{{"name":"#completed_round","objective":"{ns}.data"}},"color":"gold","bold":true}},{{"text":" complete! +500 points. Next round in 10 seconds...","color":"green"}}]

# Schedule next round after 10 seconds
schedule function {ns}:v{version}/zombies/start_round 200t
""")

	# Grenade Replenishment (appended to start_round) ───────────

	write_versioned_function("zombies/start_round", f"""
# Replenish grenades for all alive players (+2, cap at 4)
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:v{version}/zombies/inventory/replenish_grenades
""")

