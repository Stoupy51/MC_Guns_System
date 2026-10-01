""" Turning the dropped item into the managed display, and its lifetime and blink. """
# Imports
from stewbeet import Mem, write_versioned_function

from .types import POWERUP_BLINK_START, POWERUP_LIFETIME, POWERUP_TYPES, pu_snd


# Functions
def write_powerup_spawn() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Replace the loot-spawned item entity with the managed power-up visuals.
	write_versioned_function("zombies/powerups/intercept_item", f"""
execute unless data entity @s Item.components."minecraft:custom_data".{ns}.powerup run return 0

scoreboard players add #pu_uid {ns}.data 1
data modify storage {ns}:temp _pu_spawn.type set from entity @s Item.components."minecraft:custom_data".{ns}.powerup.type
execute store result storage {ns}:temp _pu_spawn.x int 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pu_spawn.y int 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pu_spawn.z int 1 run data get entity @s Pos[2]
execute store result storage {ns}:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid {ns}.data

kill @s

function {ns}:v{version}/zombies/powerups/spawn_display with storage {ns}:temp _pu_spawn
""", tags=["common_signals:signals/on_new_item"])

	# Per-type values go as macro arguments. The label stays a quoted text component so auto.lang_file still translates it;
	# the argument is `label`, not `text`, or the outer quoted value would be translated instead.
	dispatch_lines: str = "\n".join(
		f'$execute if data storage {ns}:temp _pu_spawn{{"type":"{pu_id}"}} run function {ns}:v{version}/zombies/powerups/spawn_type '
		f'{{x:$(x),y:$(y),z:$(z),uid:$(uid),item:"{v.item}",type_num:{v.type_num},'
		f'label:\'{{"text":"{v.display}","color":"{v.color}","bold":true}}\'}}'
		for pu_id, v in POWERUP_TYPES.items()
	)
	write_versioned_function("zombies/powerups/spawn_display", dispatch_lines)

	# Macro arguments: x, y, z, uid, item, type_num, label.
	write_versioned_function("zombies/powerups/spawn_type", f"""
$summon minecraft:item $(x) $(y) $(z) {{Tags:["{ns}.pu_item","{ns}.pu_item_new","{ns}.gm_entity"],PickupDelay:32767,Invulnerable:1b,Item:{{id:"$(item)",count:1,components:{{"minecraft:custom_data":{{{ns}:{{powerup_uid:$(uid)}}}}}}}}}}
$scoreboard players set @n[type=minecraft:item,tag={ns}.pu_item_new] {ns}.zb.pu.type $(type_num)
scoreboard players set @n[type=minecraft:item,tag={ns}.pu_item_new] {ns}.zb.pu.timer {POWERUP_LIFETIME}
tag @n[type=minecraft:item,tag={ns}.pu_item_new] remove {ns}.pu_item_new

# Live count gating the per-item scans in game_tick. pu_item is Invulnerable, so it only dies through tracked paths.
scoreboard players add #pu_active {ns}.data 1
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {{Tags:["{ns}.pu_text","{ns}.gm_entity"],text:$(label),billboard:"vertical",background:0,shadow:true,view_range:64.0f,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}}}

{pu_snd(ns, "item/spawn", 0.7)}
""")

	write_versioned_function("zombies/powerups/entity_tick", f"""
scoreboard players operation @s {ns}.zb.pu.timer -= #tick_delta {ns}.data

execute if score @s {ns}.zb.pu.timer matches ..0 run return run function {ns}:v{version}/zombies/powerups/expire

# Blinks in the last {POWERUP_BLINK_START // 20} s.
execute if score @s {ns}.zb.pu.timer matches 1..{POWERUP_BLINK_START - 1} run function {ns}:v{version}/zombies/powerups/blink_tick

# loop_2s every 40 ticks.
scoreboard players operation #pu_loop_phase {ns}.data = @s {ns}.zb.pu.timer
scoreboard players operation #pu_loop_phase {ns}.data %= #40 {ns}.data
execute if score #pu_loop_phase {ns}.data matches 0 run playsound {ns}:zombies/powerups/item/loop_2s ambient @a[scores={{{ns}.zb.in_game=1}},distance=..24] ~ ~ ~ 0.5 1.0

# do_pickup kills @s, so this stays last.
execute if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5,tag=!{ns}.pu_collecting] run function {ns}:v{version}/zombies/powerups/do_pickup

# Downed players pick up by crawling their mannequin over it (Black Ops rule), when no alive player is in range.
execute unless entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..1.5] if entity @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,distance=..1.5] run function {ns}:v{version}/zombies/powerups/do_pickup
""")

	write_versioned_function("zombies/powerups/expire", f"""
kill @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3]
kill @s
scoreboard players remove #pu_active {ns}.data 1
""")

	# BO2's 0.4 s cycle: 4 ticks on, 4 off.
	write_versioned_function("zombies/powerups/blink_tick", f"""
execute if score #zb_blink_state {ns}.data matches 0 run data modify entity @s Item.components."minecraft:custom_data".{ns}.powerup_model set from entity @s Item.components."minecraft:item_model"
execute if score #zb_blink_state {ns}.data matches 0 run data modify entity @s Item.components."minecraft:item_model" set value "minecraft:air"
execute if score #zb_blink_state {ns}.data matches 1 run data modify entity @s Item.components."minecraft:item_model" set from entity @s Item.components."minecraft:custom_data".{ns}.powerup_model
# text_display has no visibility tag, so view_range toggles it.
execute if score #zb_blink_state {ns}.data matches 0 as @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3] run data merge entity @s {{view_range:0.0f}}
execute if score #zb_blink_state {ns}.data matches 1 as @n[type=minecraft:text_display,tag={ns}.pu_text,distance=..3] run data merge entity @s {{view_range:64.0f}}
""")

