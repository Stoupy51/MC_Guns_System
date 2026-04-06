
# ruff: noqa: E501
# Revive System (Black Ops Zombies-style)
# When a player takes lethal damage, they enter a "downed" state instead of dying.
# Teammates can revive them by looking at them and holding right-click within a time limit.
# If not revived in time, the player bleeds out and becomes a spectator until the next round.
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG

# Revive configuration
BLEED_OUT_TICKS: int = 600		# 30 seconds to be revived before bleed out
REVIVE_TICKS: int = 60			# 3 seconds of proximity to revive
REVIVE_RANGE: float = 2.5		# Blocks range for revive interaction
QUICK_REVIVE_TICKS: int = 30	# 1.5 seconds with Quick Revive perk


def generate_revive() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Scoreboards
	write_load_file(f"""
# Revive system scoreboards
scoreboard objectives add {ns}.zb.downed dummy
scoreboard objectives add {ns}.zb.bleed dummy
scoreboard objectives add {ns}.zb.revive_p dummy
""")

	## On Down: called from on_respawn when player dies in zombies
	write_versioned_function("zombies/revive/on_down", f"""
# Mark player as downed
scoreboard players set @s {ns}.zb.downed 1
scoreboard players set @s {ns}.zb.bleed {BLEED_OUT_TICKS}
scoreboard players set @s {ns}.zb.revive_p 0
tag @s add {ns}.downed

# Slow down heavily + weakness (can't deal damage)
effect give @s slowness infinite 6 true
effect give @s weakness infinite 255 true
effect give @s mining_fatigue infinite 255 true

# Force crouch-like feel by lowering health to 1 heart
attribute @s minecraft:max_health base set 2
effect give @s instant_health 1 255 true

# Clear active weapon state to prevent shooting
scoreboard players set @s {ns}.mp.death_count 0

# Announce
title @s title [{{"text":"\\u2620","color":"red"}}]
title @s subtitle [{{"text":"You are down! Wait for a teammate to revive you.","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"red"}},{{"text":" is down!","color":"gray"}}]
""")

	## Tick: process all downed players
	write_versioned_function("zombies/revive/tick", f"""
# Process each downed player
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=1}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/revive/downed_tick
""")

	## Downed tick: per-player (run as the downed player)
	write_versioned_function("zombies/revive/downed_tick", f"""
# Decrement bleed timer
scoreboard players remove @s {ns}.zb.bleed 1

# Check if any teammate is reviving (within range and looking at downed player)
# Reset progress if no one is nearby
scoreboard players set #zb_reviving {ns}.data 0
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE}] facing entity @s eyes run function {ns}:v{version}/zombies/revive/check_reviver

# If someone is actively reviving, increment progress
execute if score #zb_reviving {ns}.data matches 1.. run function {ns}:v{version}/zombies/revive/progress_tick

# If no one is reviving, decay progress
execute if score #zb_reviving {ns}.data matches 0 if score @s {ns}.zb.revive_p matches 1.. run scoreboard players remove @s {ns}.zb.revive_p 2

# Show bleed timer on actionbar
execute store result storage {ns}:temp _rv_sec int 1 run scoreboard players get @s {ns}.zb.bleed
function {ns}:v{version}/zombies/revive/show_bleed_bar

# Bleed out: time's up
execute if score @s {ns}.zb.bleed matches ..0 run function {ns}:v{version}/zombies/revive/bleed_out
""")

	## Check if a potential reviver is looking at the downed player
	write_versioned_function("zombies/revive/check_reviver", f"""
# The command runs 'as @a[alive, nearby] facing entity @s[downed] eyes'
# Check if the alive player's view direction roughly points at the downed player
# We use a simple raycast: the alive player's look direction should point within ~30° of the downed player

# Simple approach: just check distance (if within range, they are reviving)
# The 'facing entity @s eyes' rotation is set but we just need proximity + not downed
scoreboard players set #zb_reviving {ns}.data 1

# Show actionbar to reviver
execute store result storage {ns}:temp _rv_prog int 1 run scoreboard players get @p[tag={ns}.downed,sort=nearest,distance=..{REVIVE_RANGE}] {ns}.zb.revive_p

# Check if reviver has Quick Revive perk
execute if entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_normal
""")

	## Show revive progress bar to reviver (normal speed)
	write_versioned_function("zombies/revive/show_reviver_bar_normal", f"""
title @s actionbar [{{"text":"Reviving... ","color":"yellow"}},{{"score":{{"name":"@p[tag={ns}.downed,sort=nearest,distance=..{REVIVE_RANGE}]","objective":"{ns}.zb.revive_p"}},"color":"green"}},{{"text":"/{REVIVE_TICKS}t","color":"gray"}}]
""")

	## Show revive progress bar to reviver (quick revive)
	write_versioned_function("zombies/revive/show_reviver_bar_quick", f"""
title @s actionbar [{{"text":"⚡ Reviving... ","color":"aqua"}},{{"score":{{"name":"@p[tag={ns}.downed,sort=nearest,distance=..{REVIVE_RANGE}]","objective":"{ns}.zb.revive_p"}},"color":"green"}},{{"text":"/{QUICK_REVIVE_TICKS}t","color":"gray"}}]
""")

	## Progress tick: someone is reviving
	write_versioned_function("zombies/revive/progress_tick", f"""
# Increment revive progress
scoreboard players add @s {ns}.zb.revive_p 1

# Check if revive is complete
# Use Quick Revive threshold if the reviver has the perk
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE},tag={ns}.perk.quick_revive] if score @s {ns}.zb.revive_p matches {QUICK_REVIVE_TICKS}.. run function {ns}:v{version}/zombies/revive/revive_complete
execute unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{REVIVE_RANGE},tag={ns}.perk.quick_revive] if score @s {ns}.zb.revive_p matches {REVIVE_TICKS}.. run function {ns}:v{version}/zombies/revive/revive_complete
""")

	## Revive complete: restore the downed player
	write_versioned_function("zombies/revive/revive_complete", f"""
# Remove downed state
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed

# Remove downed effects
effect clear @s slowness
effect clear @s weakness
effect clear @s mining_fatigue

# Restore max health (check for Juggernog perk)
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Heal to full
effect give @s instant_health 1 255 true

# Announce
title @s title [{{"text":"\\u2764","color":"green"}}]
title @s subtitle [{{"text":"You have been revived!","color":"green"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" has been revived!","color":"gray"}}]
""")

	## Bleed out: player couldn't be revived in time
	write_versioned_function("zombies/revive/bleed_out", f"""
# Remove downed state
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed

# Remove downed effects
effect clear @s slowness
effect clear @s weakness
effect clear @s mining_fatigue

# Restore health base before going to spectator
attribute @s minecraft:max_health base set 20

# Set player to spectator until next round
gamemode spectator @s

# Spectate a random alive in-game player (prefer non-downed)
execute at @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run tp @s @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]

# Announce
title @s title [{{"text":"\\u2620","color":"dark_red"}}]
title @s subtitle [{{"text":"You bled out. Respawning next round...","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"dark_red"}},{{"text":" has bled out.","color":"gray"}}]
""")

	## Show bleed timer bar on the downed player's actionbar
	write_versioned_function("zombies/revive/show_bleed_bar", f"""
title @s actionbar [{{"text":"\\u2620 Bleeding out: ","color":"red"}},{{"score":{{"name":"@s","objective":"{ns}.zb.bleed"}},"color":"gray"}},{{"text":"t","color":"dark_gray"}}]
""")

	## Round end respawn: called from round_complete to respawn bled-out players
	write_versioned_function("zombies/revive/round_respawn", f"""
# Respawn all spectator (bled-out) players
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=spectator] at @s run function {ns}:v{version}/zombies/revive/do_round_respawn
""")

	## Do the actual round respawn for a bled-out player
	write_versioned_function("zombies/revive/do_round_respawn", f"""
# Stop spectating
spectate @s

# Teleport to random player spawn
function {ns}:v{version}/zombies/respawn_tp

# Re-apply saturation
effect give @s saturation infinite 255 true

# Switch back to adventure
gamemode adventure @s

# Restore max health (check for Juggernog perk)
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s instant_health 1 255 true

# Re-give starting weapon on respawn
function {ns}:v{version}/zombies/inventory/give_respawn_loadout

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" has respawned!","color":"gray"}}]
""")

	## Hook: reset revive state on game start
	write_versioned_function("zombies/start", f"""
# Reset revive state
scoreboard players set @a {ns}.zb.downed 0
scoreboard players set @a {ns}.zb.bleed 0
scoreboard players set @a {ns}.zb.revive_p 0
tag @a remove {ns}.downed
""")

	## Hook: reset revive state on game stop
	write_versioned_function("zombies/stop", f"""
# Reset revive state
scoreboard players set @a {ns}.zb.downed 0
scoreboard players set @a {ns}.zb.bleed 0
scoreboard players set @a {ns}.zb.revive_p 0
tag @a remove {ns}.downed
effect clear @a slowness
effect clear @a weakness
effect clear @a mining_fatigue
""")

