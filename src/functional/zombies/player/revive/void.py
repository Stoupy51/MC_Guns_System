""" Falling out of the world, and the Who's Who / solo QR saves for it. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.text import Text
from ....helpers.titles import TitleTimes
from .shared import SOLO_QR_MAX


# Functions
def write_void_deaths() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Full death: instant elimination with NO mannequin (e.g. falling out of the world).
	# The player goes straight to bled-out spectator and is respawned at the next round end.
	write_versioned_function("zombies/revive/full_death", f"""
# A doppelganger's unrevived body is forfeited (same rule as going down again)
execute if entity @s[tag={ns}.ww_active] run function {ns}:v{version}/zombies/whos_who/forfeit

# A revive perk saves you from the void instead of a full elimination. Checked BEFORE lose_all
# strips the perks. Who's Who takes priority over solo Quick Revive (same order as revive/on_down):
# - Who's Who: keep playing as a doppelganger; the body can't live in the void, so it drops at a spawn.
# - Solo Quick Revive: in a solo game with uses left, spend one and respawn at a spawn point.
execute if score @s {ns}.zb.perk.whos_who matches 1 run return run function {ns}:v{version}/zombies/revive/void_revive_whos_who
execute store result score #zb_ingame_total {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute if entity @s[tag={ns}.perk.quick_revive] if score #zb_ingame_total {ns}.data matches ..1 unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run return run function {ns}:v{version}/zombies/revive/void_revive_solo_qr

# Count it as a down and strip perks (same as a normal down/bleed-out)
scoreboard players add @s {ns}.zb.downs 1
function {ns}:v{version}/zombies/perks/lose_all

# Defensively clear any downed state (no mannequin is created on this path)
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Enter spectator and watch a random alive teammate (respawn handled at round end)
gamemode spectator @s
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] run spectate @s
execute unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run tp @s ~ ~ ~

# Announce
{TitleTimes.BAD_NEWS.cmd()}
title @s title ["☠"]
title @s subtitle [{{"text":"You fell out of the world!","color":"gray"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="dark_red")},{{"text":" fell out of the world.","color":"gray"}}]
""")

	## Who's Who saved you from the void (@s = the falling player, perks still intact).
	## Respawn at a safe spawn first (the death spot is the void), then run the normal Who's Who down with the body anchored at that spawn — the doppelganger flow then relocates itself ≥10 blocks from the body.
	write_versioned_function("zombies/revive/void_revive_whos_who", f"""
gamemode adventure @s
function {ns}:v{version}/zombies/revive/respawn_near_player
data modify storage {ns}:temp _body_at set from entity @s Pos
function {ns}:v{version}/zombies/whos_who/on_down
""")

	## Solo Quick Revive saved you from the void (@s = the falling player, solo game, uses left).
	## Spend one use and respawn at a spawn point.
	## Perks are still stripped (any down loses them), consistent with a normal solo QR self-revive; the QR rebuy bookkeeping mirrors solo_qr_complete.
	write_versioned_function("zombies/revive/void_revive_solo_qr", f"""
# Consume one Quick Revive use (same rebuy bookkeeping as solo_qr_complete)
scoreboard players add @s {ns}.zb.qr_uses 1
tag @s remove {ns}.perk.quick_revive
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 1
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 0
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive exhausted! ({SOLO_QR_MAX}/{SOLO_QR_MAX}) No more self-revives this game.","color":"dark_red"}}]
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive used! ({SOLO_QR_MAX - 1 if SOLO_QR_MAX > 1 else 0}/{SOLO_QR_MAX}) Rebuy for another self-revive.","color":"gray"}}]

# Count the down and strip perks (any down loses them), then clear any downed state defensively
scoreboard players add @s {ns}.zb.downs 1
function {ns}:v{version}/zombies/perks/lose_all
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator

# Respawn at a safe spawn, healthy
gamemode adventure @s
function {ns}:v{version}/zombies/revive/respawn_near_player
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s minecraft:instant_health 1 255 true
scoreboard players set @s {ns}.stam_seen 0

# Announce
{TitleTimes.EVENT.cmd()}
title @s title ["⚡"]
title @s subtitle [{{"text":"Quick Revive pulled you back from the void!","color":"aqua"}}]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="aqua")},{{"text":" fell out — but Quick Revive pulled them back!","color":"gray"}}]
""")

