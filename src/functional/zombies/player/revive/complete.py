""" Reviver feedback, completing a revive, bleeding out and hiding the body. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.text import Text
from ....progression import Xp
from .shared import QUICK_REVIVE_TICKS, REVIVE_TICKS


# Functions
def write_revive_completion() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Reviver actionbar (run as the reviving player, context @s = reviver, nearest downed = target)
	write_versioned_function("zombies/revive/show_reviver_bar", f"""
# #rv_reviver_disp holds the downed player's revive progress (snapshotted in downed_tick while
# @s was the downed player — the reviver cannot re-select them: they spectate a camera entity
# that sits outside the revive range, which used to make this display a stuck "0").
# Convert ticks to seconds for display: sec = p/20, tenth = (p%20)/2
scoreboard players operation #rv_rev_sec {ns}.data = #rv_reviver_disp {ns}.data
scoreboard players operation #rv_rev_sec {ns}.data /= #20 {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data = #rv_reviver_disp {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data %= #20 {ns}.data
scoreboard players operation #rv_rev_tenth {ns}.data /= #2 {ns}.data

# Marked for revive_complete, which runs as the DOWNED player and cannot re-select the revivers
tag @s add {ns}.zb_reviver

# Check if reviver has Quick Revive perk
execute if entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag={ns}.perk.quick_revive] run function {ns}:v{version}/zombies/revive/show_reviver_bar_normal
""")

	write_versioned_function("zombies/revive/show_reviver_bar_normal", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"Reviving... ","color":"yellow"}},{{"score":{{"name":"#rv_rev_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_rev_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {REVIVE_TICKS // 20}.{(REVIVE_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/revive/show_reviver_bar_quick", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚡ Reviving... ","color":"aqua"}},{{"score":{{"name":"#rv_rev_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_rev_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {QUICK_REVIVE_TICKS // 20}.{(QUICK_REVIVE_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message
""")

	# HUD color update helpers (run as downed spectator, update nearest downed_hud) Recolor only: the name was written once as a literal string in on_down (set_hud_name) and must never be replaced by a "nearest" selector (wrong-owner ties, see on_down)
	for hud_color in ("white", "yellow", "gold", "red"):
		write_versioned_function(f"zombies/revive/hud_{hud_color}", f"""
data modify entity @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] text[0].color set value "{hud_color}"
data modify entity @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] text[1].color set value "{hud_color}"
""")

	# Revive complete: restore the downed player (run as downed spectator)
	write_versioned_function("zombies/revive/revive_complete", f"""
# Remove downed state
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Identify THIS player's mannequin by downed_id — with several downed players,
# a 'nearest mannequin' lookup could consume someone else's mannequin and revive at the wrong place
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp

# Store mannequin position before hiding it. Track read success: if the mannequin is missing,
# the storage would keep a stale position (this is how players ended up respawning at 0 0 0)
scoreboard players set #rv_pos_ok {ns}.data 0
execute store success score #rv_pos_ok {ns}.data run data get entity @n[tag={ns}.downed_mine_temp] Pos
execute store result storage {ns}:temp rv_x double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[0] 1000
execute store result storage {ns}:temp rv_y double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[1] 1000
execute store result storage {ns}:temp rv_z double 0.001 run data get entity @n[tag={ns}.downed_mine_temp] Pos[2] 1000
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

# Hide mannequin + HUD and kill the camera
function {ns}:v{version}/zombies/revive/hide_body

# Dismount from camera entity and restore adventure mode
ride @s dismount
gamemode adventure @s

# Teleport player to where the mannequin was; if it couldn't be found, fall back to a safe
# spawn point near a teammate instead of teleporting to a stale position (e.g. 0 0 0)
execute if score #rv_pos_ok {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/tp_revive_pos with storage {ns}:temp
execute unless score #rv_pos_ok {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/respawn_near_player

# Restore max health (check for Juggernog perk)
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Heal to full and reset stamina to full (the stamina system owns the hunger bar)
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

# Tombstone: revived → discard the pending marker + perk snapshot (nothing to recover)
function {ns}:v{version}/zombies/perks/tombstone_on_revived

# Announce
title @s title ["❤"]
title @s subtitle [{{"text":"You have been revived!","color":"green"}}]
{Xp.announce("zb", "revive", f'{MGS_TAG},{Text.player(ns, "@s", side="zb", color="green")},{{"text":" has been revived!","color":"gray"}}', earner=f"@a[tag={ns}.zb_reviver]", audience=f"@a[scores={{{ns}.zb.in_game=1}}]")}
""")

	# Bleed out: player couldn't be revived in time (run as downed spectator)
	write_versioned_function("zombies/revive/bleed_out", f"""
# Remove downed state
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Hide THIS player's mannequin and HUD (id-matched: a "nearest" lookup could hide another downed
# player's mannequin when both went down together)
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id

# Tombstone: snapshot the inventory now (still intact) if a marker is waiting for this player
function {ns}:v{version}/zombies/perks/tombstone_on_bleed_out

function {ns}:v{version}/zombies/revive/hide_body

# Dismount then enter full spectator mode to watch until next round
ride @s dismount
gamemode spectator @s

# Spectate a random alive in-game player
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] run spectate @s
# Fallback if no alive players: teleport spectator somewhere reasonable
execute unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run tp @s ~ ~ ~

# Announce
title @s title ["☠"]
title @s subtitle [{{"text":"You bled out. Respawning next round...","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="dark_red")},{{"text":" has bled out.","color":"gray"}}]
""")

	## Hide @s's body (mannequin + HUD, id-matched via #my_downed_id) by teleporting it far below the world (avoids the kill animation/drops), strip the tags, and kill the camera if any.
	## Shared by revive_complete, bleed_out and the Who's Who paths (no camera there — no-op).
	write_versioned_function("zombies/revive/hide_body", f"""
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp
tp @n[tag={ns}.downed_mine_temp] ~ -10000 ~
execute as @e[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tp @s ~ -10000 ~
tag @n[tag={ns}.downed_mine_temp] remove {ns}.downed_mannequin
execute as @e[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tag @s remove {ns}.downed_hud
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp
execute as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
""")

