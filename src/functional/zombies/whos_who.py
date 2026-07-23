
# ruff: noqa: E501
# Who's Who — instead of going down, the owner keeps playing as a "doppelganger" with only a knife +
# pistol, while their body drops as a revivable mannequin. Any alive player (including the
# doppelganger themselves) can revive that body: on revive the owner gets everything back minus
# Who's Who; if the body bleeds out, the doppelganger fights on with just the pistol (perks stay
# lost). Down again as a doppelganger → normal down (Who's Who was already lost). Disabled solo
# (a solo doppelganger down is game over). Priority above Tombstone. Called from revive/on_down.
#
# This is a self-contained subsystem (not the spectator-based normal downed flow): a Who's Who owner
# stays a normal ALIVE player (never zb.downed), tagged {ns}.ww_active, ticked from game_tick.
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .perks import PERK_DEFINITIONS
from .revive import BLEED_OUT_TICKS, REVIVE_RANGE, REVIVE_TICKS


def generate_whos_who() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	perk_ids: list[str] = list(PERK_DEFINITIONS)

	ww_snapshot: str = "\n".join(f"scoreboard players operation @s {ns}.zb.wwp.{pid} = @s {ns}.zb.perk.{pid}" for pid in perk_ids)
	ww_clear: str = "\n".join(f"scoreboard players set @s {ns}.zb.wwp.{pid} 0" for pid in perk_ids)
	ww_restore_lines: list[str] = []
	for pid, pdata in PERK_DEFINITIONS.items():
		if pid == "whos_who":
			continue  # Who's Who is not restored on revive (BO rule) — must be rebought
		ww_restore_lines.append(f"execute if score @s {ns}.zb.wwp.{pid} matches 1 run scoreboard players set @s {ns}.zb.perk.{pid} 1")
		if pdata.get("commands"):
			# reapply/<pid> (effect-only, no chat) is generated in perks.py's Tombstone section
			ww_restore_lines.append(f"execute if score @s {ns}.zb.wwp.{pid} matches 1 run function {ns}:v{version}/zombies/perks/reapply/{pid}")
	ww_restore: str = "\n".join(ww_restore_lines)

	## State objectives
	write_load_file(f"""
# Who's Who: doppelganger bleed timer + revive progress (on the owner), perk snapshot for recovery.
# The body mannequin carries the owner's zb.downed_id (reuses the revive downed_id_match predicate).
scoreboard objectives add {ns}.zb.ww.bleed dummy
scoreboard objectives add {ns}.zb.ww.rev dummy
{chr(10).join(f"scoreboard objectives add {ns}.zb.wwp.{pid} dummy" for pid in perk_ids)}
""")

	## Called from revive/on_down (@s = player, death pos in temp rv_x/rv_y/rv_z). Only reached in
	## co-op when the owner has Who's Who. Takes over the down entirely.
	write_versioned_function("zombies/whos_who/on_down", f"""
# Read the death location (branch runs before the normal flow computes it)
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @s LastDeathLocation.pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @s LastDeathLocation.pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @s LastDeathLocation.pos[2] 1000

# Snapshot perks + inventory (for recovery on revive) — BEFORE anything is stripped
{ww_snapshot}

# Assign a fresh downed_id for the body mannequin (same counter as the revive system)
scoreboard players add #downed_id_next {ns}.data 1
scoreboard players operation @s {ns}.zb.downed_id = #downed_id_next {ns}.data
execute store result storage {ns}:temp _ww_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/whos_who/snapshot_inv with storage {ns}:temp _ww_id

# Summon the body mannequin wearing the owner's armor/skin, and a HUD above it, at the death spot
summon minecraft:mannequin ~ ~.5 ~ {{Invulnerable:1b,pose:"swimming",hide_description:true,Tags:["{ns}.ww_body","{ns}.ww_body_new","{ns}.gm_entity"]}}
scoreboard players operation @n[tag={ns}.ww_body_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id
data modify entity @n[tag={ns}.ww_body_new] equipment set from entity @s equipment
loot replace entity @n[tag={ns}.ww_body_new] weapon.mainhand loot {ns}:get_username
data modify entity @n[tag={ns}.ww_body_new] profile set from entity @n[tag={ns}.ww_body_new] equipment.mainhand.components."minecraft:profile"
data modify storage {ns}:temp rv_name set from entity @n[tag={ns}.ww_body_new] equipment.mainhand.components."minecraft:profile".name
execute unless data storage {ns}:temp rv_name run data modify storage {ns}:temp rv_name set value "???"
item replace entity @n[tag={ns}.ww_body_new] weapon.mainhand with minecraft:air
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.ww_hud","{ns}.ww_hud_new","{ns}.gm_entity"],billboard:"vertical",shadow:1b,see_through:0b,teleport_duration:1,transformation:{{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},text:[{{"text":"...","color":"dark_aqua"}},{{"text":" ↓","color":"dark_aqua"}}]}}
scoreboard players operation @n[tag={ns}.ww_hud_new] {ns}.zb.downed_id = @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/whos_who/set_hud_name with storage {ns}:temp
function {ns}:v{version}/zombies/whos_who/tp_body with storage {ns}:temp
tag @e[tag={ns}.ww_body_new] remove {ns}.ww_body_new
tag @e[tag={ns}.ww_hud_new] remove {ns}.ww_hud_new

# Strip perks (the doppelganger starts fresh)
function {ns}:v{version}/zombies/perks/lose_all

# Doppelganger loadout: wipe everything and hand back only the starting knife + pistol kit
clear @s
gamemode adventure @s
function {ns}:v{version}/zombies/inventory/give_respawn_loadout

# Keep the player where they respawned near a teammate is jarring — put them at their body so they
# can choose to self-revive or fight on
function {ns}:v{version}/zombies/revive/tp_revive_pos with storage {ns}:temp

# Enter doppelganger state
tag @s add {ns}.ww_active
scoreboard players set @s {ns}.zb.ww.bleed {BLEED_OUT_TICKS}
scoreboard players set @s {ns}.zb.ww.rev 0

# Announce
title @s times 5 40 15
title @s title ["👥"]
title @s subtitle [{{"text":"Who's Who — revive your body, or fight on!","color":"dark_aqua"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"aqua"}},{{"text":" went down — but plays on as a doppelganger!","color":"gray"}}]
""")

	## Macro: write the owner's literal name into the HUD (avoids "nearest" ties, same as revive)
	write_versioned_function("zombies/whos_who/set_hud_name", f"""
$data modify entity @n[tag={ns}.ww_hud_new] text set value [{{"text":"$(rv_name)","color":"dark_aqua"}},{{"text":" ↓","color":"dark_aqua"}}]
""")

	## Macro: teleport the freshly-summoned body + HUD to the death location
	write_versioned_function("zombies/whos_who/tp_body", f"""
$tp @n[tag={ns}.ww_body_new] $(rv_x) $(rv_y) $(rv_z)
$tp @n[tag={ns}.ww_hud_new] $(rv_x) $(rv_y) $(rv_z)
tp @n[tag={ns}.ww_hud_new] ~ ~2 ~
""")

	## Macro: store @s Inventory keyed by downed_id (for recovery on revive)
	write_versioned_function("zombies/whos_who/snapshot_inv", f"""
$data modify storage {ns}:zombies ww_inv."$(id)" set from entity @s Inventory
""")

	## Per-tick, per doppelganger (hooked into game_tick). @s = the ww_active owner.
	write_versioned_function("zombies/whos_who/tick", f"""
execute as @a[tag={ns}.ww_active,scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/whos_who/owner_tick
""")

	write_versioned_function("zombies/whos_who/owner_tick", f"""
# Bleed timer on the body
scoreboard players operation @s {ns}.zb.ww.bleed -= #tick_delta {ns}.data

# Identify this owner's body/HUD
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id

# Any alive in-game player (including the doppelganger themselves) within range of the body = reviving
scoreboard players set #ww_reviving {ns}.data 0
execute as @e[tag={ns}.ww_body,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..{REVIVE_RANGE}] run scoreboard players set #ww_reviving {ns}.data 1

# Progress / decay
scoreboard players operation #ww_decay {ns}.data = #tick_delta {ns}.data
scoreboard players operation #ww_decay {ns}.data *= #2 {ns}.data
execute if score #ww_reviving {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.ww.rev += #tick_delta {ns}.data
execute if score #ww_reviving {ns}.data matches 0 if score @s {ns}.zb.ww.rev matches 1.. run scoreboard players operation @s {ns}.zb.ww.rev -= #ww_decay {ns}.data

# Body particles + keep the HUD anchored above the body
execute as @e[tag={ns}.ww_body,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s run particle minecraft:soul ~ ~1 ~ 0.2 0.4 0.2 0.01 2 force @a[distance=..48]

# Reviving actionbar for the doppelganger
execute if score #ww_reviving {ns}.data matches 1 run data modify storage smithed.actionbar:input message set value {{json:[{{"text":"Reviving your body...","color":"dark_aqua"}}],priority:"override",freeze:2}}
execute if score #ww_reviving {ns}.data matches 1 run function #smithed.actionbar:message

# Revive complete
execute if score @s {ns}.zb.ww.rev matches {REVIVE_TICKS}.. run function {ns}:v{version}/zombies/whos_who/revive_complete

# Body bled out: doppelganger fights on with just the pistol (perks stay lost)
execute if score @s {ns}.zb.ww.bleed matches ..0 run function {ns}:v{version}/zombies/whos_who/bleed_out
""")

	## Revive complete (@s = doppelganger owner): restore perks (minus Who's Who) + inventory + health
	write_versioned_function("zombies/whos_who/revive_complete", f"""
{ww_restore}
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40

# Restore the snapshotted inventory
execute store result storage {ns}:temp _ww_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/whos_who/restore_inv with storage {ns}:temp _ww_id
function {ns}:v{version}/zombies/inventory/refresh_perk_items
effect give @s minecraft:instant_health 1 255 true

# Clear doppelganger state + snapshot, remove the body
{ww_clear}
tag @s remove {ns}.ww_active
scoreboard players set @s {ns}.zb.ww.bleed 0
scoreboard players set @s {ns}.zb.ww.rev 0
function {ns}:v{version}/zombies/whos_who/despawn_body

title @s times 5 40 15
title @s title ["❤"]
title @s subtitle [{{"text":"Body revived — you are whole again!","color":"green"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"green"}},{{"text":" revived their own body!","color":"gray"}}]
function {ns}:v{version}/zombies/feedback/sound_success
""")

	## Body bled out (@s = doppelganger owner): keep playing with the pistol, perks stay lost
	write_versioned_function("zombies/whos_who/bleed_out", f"""
{ww_clear}
execute store result storage {ns}:temp _ww_id.id int 1 run scoreboard players get @s {ns}.zb.downed_id
function {ns}:v{version}/zombies/whos_who/drop_inv with storage {ns}:temp _ww_id
tag @s remove {ns}.ww_active
scoreboard players set @s {ns}.zb.ww.bleed 0
scoreboard players set @s {ns}.zb.ww.rev 0
function {ns}:v{version}/zombies/whos_who/despawn_body

title @s title ["☠"]
title @s subtitle [{{"text":"Your body bled out — fight on with your pistol.","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s","color":"dark_aqua"}},{{"text":"'s body bled out.","color":"gray"}}]
""")

	## Despawn this owner's body + HUD (id-matched)
	write_versioned_function("zombies/whos_who/despawn_body", f"""
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
kill @e[tag={ns}.ww_body,predicate={ns}:v{version}/zombies/revive/downed_id_match]
kill @e[tag={ns}.ww_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match]
""")

	## Macros: restore / drop the inventory snapshot by id
	write_versioned_function("zombies/whos_who/restore_inv", f"""
$data modify entity @s Inventory set from storage {ns}:zombies ww_inv."$(id)"
$data remove storage {ns}:zombies ww_inv."$(id)"
""")
	write_versioned_function("zombies/whos_who/drop_inv", f"""
$data remove storage {ns}:zombies ww_inv."$(id)"
""")

	## Hook: tick doppelgangers
	write_versioned_function("zombies/game_tick", f"""
execute if data storage {ns}:zombies game{{state:"active"}} run function {ns}:v{version}/zombies/whos_who/tick
""")

	## Hook: cleanup on game start/stop
	write_versioned_function("zombies/start", f"""
kill @e[tag={ns}.ww_body]
kill @e[tag={ns}.ww_hud]
tag @a remove {ns}.ww_active
data modify storage {ns}:zombies ww_inv set value {{}}
""")
	write_versioned_function("zombies/stop", f"""
kill @e[tag={ns}.ww_body]
kill @e[tag={ns}.ww_hud]
tag @a remove {ns}.ww_active
data modify storage {ns}:zombies ww_inv set value {{}}
""")
