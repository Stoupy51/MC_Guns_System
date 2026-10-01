""" Reviver feedback, completing a revive, bleeding out and hiding the body. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.text import Text
from ....helpers.titles import TitleTimes
from ....progression import Xp
from .shared import QUICK_REVIVE_TICKS, REVIVE_TICKS


# Functions
def write_revive_completion() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Run as the reviving player.
	write_versioned_function("zombies/revive/show_reviver_bar", f"""
# #rv_reviver_disp is the progress snapshotted in downed_tick: the reviver cannot select the downed player,
# who spectates a camera outside the revive range. Seconds = p / 20, tenths = (p % 20) / 2.
scoreboard players operation #rv_rev_sec {ns}.data = #rv_reviver_disp {ns}.data
scoreboard players operation #rv_rev_sec {ns}.data /= #20 {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data = #rv_reviver_disp {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data %= #20 {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data /= #2 {ns}.data

# revive_complete runs as the downed player and cannot select the revivers.
tag @s add {ns}.zb_reviver

execute if entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_normal
""")

	write_versioned_function("zombies/revive/show_reviver_bar_normal", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"Reviving... ","color":"yellow"}},{{"score":{{"name":"#rv_rev_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_rev_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {REVIVE_TICKS // 20}.{(REVIVE_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/revive/show_reviver_bar_quick", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚡ ","color":"white"}},{{"text":"Reviving... ","color":"aqua"}},{{"score":{{"name":"#rv_rev_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_rev_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {QUICK_REVIVE_TICKS // 20}.{(QUICK_REVIVE_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message
""")

	# Run as the downed spectator. Recolor only: the name was written once in on_down (set_hud_name).
	for hud_color in ("white", "yellow", "gold", "red"):
		write_versioned_function(f"zombies/revive/hud_{hud_color}", f"""
data modify entity @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] text[0].color set value "{hud_color}"
data modify entity @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] text[1].color set value "{hud_color}"
""")

	# Run as the downed spectator.
	write_versioned_function("zombies/revive/revive_complete", f"""
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# By downed_id: with several downed players, the nearest mannequin can be someone else's.
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp

# The read can fail when the mannequin is missing, which would keep a stale position (players respawned at 0 0 0).
scoreboard players set #rv_pos_ok {ns}.data 0
execute store success score #rv_pos_ok {ns}.data run data get entity @n[tag={ns}.downed_mine_temp] Pos
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[2] 1000
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

function {ns}:v{version}/zombies/revive/hide_body

ride @s dismount
gamemode adventure @s

# Mannequin not found: a safe spawn near a teammate instead of a stale position.
execute if score #rv_pos_ok {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/tp_revive_pos with storage {ns}:temp
execute unless score #rv_pos_ok {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/respawn_near_player

execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# The stamina system owns the hunger bar.
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

# Tombstone: revived, so nothing to recover.
function {ns}:v{version}/zombies/perks/tombstone_on_revived

{TitleTimes.EVENT.cmd()}
title @s title ["❤"]
title @s subtitle [{{"text":"You have been revived!","color":"green"}}]
{Xp.announce("zb", "revive", f'{MGS_TAG},{Text.player(ns, "@s", side="zb", color="green")},{{"text":" has been revived!","color":"gray"}}', earner=f"@a[tag={ns}.zb_reviver]", audience=f"@a[scores={{{ns}.zb.in_game=1}}]")}
""")

	# Run as the downed spectator who was not revived in time.
	write_versioned_function("zombies/revive/bleed_out", f"""
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Id-matched: two players downed together can be each other's nearest mannequin.
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id

# Tombstone: snapshot the inventory while it is intact.
function {ns}:v{version}/zombies/perks/tombstone_on_bleed_out

function {ns}:v{version}/zombies/revive/hide_body

# Full spectator until the next round.
ride @s dismount
gamemode spectator @s

execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] run spectate @s
# No alive player: stay where the camera was.
execute unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run tp @s ~ ~ ~

{TitleTimes.BAD_NEWS.cmd()}
title @s title ["☠"]
title @s subtitle [{{"text":"You bled out. Respawning next round...","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="dark_red")},{{"text":" has bled out.","color":"gray"}}]
""")

	## Hide the body of @s (id-matched through #my_downed_id) far below the world, which avoids the death animation and drops.
	## Shared by revive_complete, bleed_out and Who's Who (which has no camera).
	write_versioned_function("zombies/revive/hide_body", f"""
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp
tp @n[tag={ns}.downed_mine_temp] ~ -10000 ~
execute as @e[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tp @s ~ -10000 ~
tag @n[tag={ns}.downed_mine_temp] remove {ns}.downed_mannequin
execute as @e[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tag @s remove {ns}.downed_hud
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp
execute as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
""")

