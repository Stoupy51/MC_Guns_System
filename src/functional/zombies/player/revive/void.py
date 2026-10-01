""" Falling out of the world, and the Who's Who / solo QR saves for it. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.probes import Probe
from ....helpers.text import Text
from ....helpers.titles import TitleTimes
from .shared import SOLO_QR_MAX


# Functions
def write_void_deaths() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Instant elimination with no mannequin (falling out of the world): straight to bled-out spectator until the round ends.
	write_versioned_function("zombies/revive/full_death", f"""
# A doppelganger forfeits their unrevived body, as when going down again.
execute if entity @s[tag={ns}.ww_active] run function {ns}:v{version}/zombies/whos_who/forfeit

# A revive perk saves the player instead, checked before lose_all. Who's Who first (as in on_down): the body drops at a spawn;
# then solo Quick Revive with uses left: spend one and respawn at a spawn.
execute if score @s {ns}.zb.perk.whos_who matches 1 run return run function {ns}:v{version}/zombies/revive/void_revive_whos_who
execute store result score #zb_ingame_total {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute if entity @s[tag={ns}.perk.quick_revive] if score #zb_ingame_total {ns}.data matches ..1 unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run return run function {ns}:v{version}/zombies/revive/void_revive_solo_qr

# Counts as a down and strips perks.
scoreboard players add @s {ns}.zb.downs 1
function {ns}:v{version}/zombies/perks/lose_all

# No mannequin exists on this path.
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Respawned at round end.
gamemode spectator @s
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] run spectate @s
execute unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run tp @s ~ ~ ~

{TitleTimes.BAD_NEWS.cmd()}
title @s title ["☠"]
title @s subtitle [{{"text":"You fell out of the world!","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="dark_red")},{{"text":" fell out of the world.","color":"gray"}}]
""")

	## Run as the falling player, perks intact: respawn at a safe spawn first, then the normal Who's Who down with the body there.
	## The doppelganger then moves 10+ blocks away.
	write_versioned_function("zombies/revive/void_revive_whos_who", f"""
gamemode adventure @s
function {ns}:v{version}/zombies/revive/respawn_near_player
{Probe.pos()}
data modify storage {ns}:temp _body_at set from storage {ns}:temp _probe_pos
function {ns}:v{version}/zombies/whos_who/on_down
""")

	## Run as the falling player, solo with uses left. Perks are still stripped, as on any down.
	write_versioned_function("zombies/revive/void_revive_solo_qr", f"""
# Same bookkeeping as solo_qr_complete.
scoreboard players add @s {ns}.zb.qr_uses 1
tag @s remove {ns}.perk.quick_revive
scoreboard players set @s {ns}.zb.perk.quick_revive 0
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive exhausted! ({SOLO_QR_MAX}/{SOLO_QR_MAX}) No more self-revives this game.","color":"dark_red"}}]
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive used! ({SOLO_QR_MAX - 1 if SOLO_QR_MAX > 1 else 0}/{SOLO_QR_MAX}) Rebuy for another self-revive.","color":"gray"}}]

scoreboard players add @s {ns}.zb.downs 1
function {ns}:v{version}/zombies/perks/lose_all
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

gamemode adventure @s
function {ns}:v{version}/zombies/revive/respawn_near_player
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

{TitleTimes.EVENT.cmd()}
title @s title ["⚡"]
title @s subtitle [{{"text":"Quick Revive pulled you back from the void!","color":"aqua"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="aqua")},{{"text":" fell out, but Quick Revive pulled them back!","color":"gray"}}]
""")

