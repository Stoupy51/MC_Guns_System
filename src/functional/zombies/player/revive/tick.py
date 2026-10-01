""" The downed tick: crawling, the single mannequin pass and solo Quick Revive. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from .shared import (
	CRAWL_SPEED,
	SOLO_QR_MAX,
	SOLO_QR_TICKS,
	revive_body_detect,
	revive_body_progress,
)


# Functions
def write_downed_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/revive/tick", f"""
execute as @a[tag={ns}.downed_spectator,scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/revive/downed_tick
""")

	## Run as the downed spectating player.
	write_versioned_function("zombies/revive/downed_tick", f"""
# Tag this player's mannequin once; everything below reuses that tag.
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp

# Crawl inputs and yaw (x100) are read here, while @s is the player, because move_mannequin cannot
# find its owner reliably when several mannequins are close.
execute store result score #rv_yaw {ns}.data run data get entity @s Rotation[0] 100
scoreboard players set #crawl_vx {ns}.data 0
scoreboard players set #crawl_vz {ns}.data 0
execute if entity @s[predicate={ns}:v{version}/input/forward] run scoreboard players set #crawl_vz {ns}.data {int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/backward] run scoreboard players set #crawl_vz {ns}.data -{int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/left] run scoreboard players set #crawl_vx {ns}.data {int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/right] run scoreboard players set #crawl_vx {ns}.data -{int(CRAWL_SPEED * 1000)}

# Camera 2 up and 3 behind the mannequin's rotation from before this tick's yaw sync, then the player re-mounts it.
execute at @n[tag={ns}.downed_mine_temp] as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tp @s ^ ^2 ^-3
ride @s mount @n[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match]

execute as @n[tag={ns}.downed_mine_temp] at @s run function {ns}:v{version}/zombies/revive/move_mannequin

tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

{revive_body_detect()}

# Solo Quick Revive: gated on the zb_qr_armed snapshot, since lose_all already removed the perk (see on_down).
execute if score #zb_reviving {ns}.data matches 0 if entity @s[tag={ns}.zb_qr_armed] run function {ns}:v{version}/zombies/revive/check_solo_qr

# Bleed timer, except during the solo Quick Revive (which has its own actionbar): seconds = bleed / 20, tenths = (bleed % 20) / 2.
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_sec {ns}.data = @s {ns}.zb.bleed
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_sec {ns}.data /= #20 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data = @s {ns}.zb.bleed
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data %= #20 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data /= #2 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run data modify storage smithed.actionbar:input message set value {{json:[{{"text":"☠ ","color":"white"}},{{"text":"Bleeding out: ","color":"red"}},{{"score":{{"name":"#rv_disp_sec","objective":"{ns}.data"}},"color":"gray"}},{{"text":".","color":"gray"}},{{"score":{{"name":"#rv_disp_tenth","objective":"{ns}.data"}},"color":"gray"}},{{"text":"s","color":"dark_gray"}}],priority:"override",freeze:2}}
execute if score #zb_reviving {ns}.data matches ..1 run function #smithed.actionbar:message

{revive_body_progress(f"{ns}:v{version}/zombies/revive/revive_complete")}

execute if score @s {ns}.zb.bleed matches ..0 run function {ns}:v{version}/zombies/revive/bleed_out

# No healthy player left and no solo revive running: bleed out now.
execute if score #zb_reviving {ns}.data matches 0 unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/revive/bleed_out
""")

	## Run as the downed player's mannequin, at it; #crawl_vx and #crawl_vz come from downed_tick.
	## Order: yaw sync, velocity, local to world, motion, HUD anchor.
	write_versioned_function("zombies/revive/move_mannequin", f"""
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #rv_yaw {ns}.data
data modify entity @s Rotation[1] set value 0.0f

# Bookshelf physics: XZ from the crawl inputs, and a constant downward Y because set_motion overrides gravity.
scoreboard players operation @s bs.vel.x = #crawl_vx {ns}.data
scoreboard players set @s bs.vel.y -400
scoreboard players operation @s bs.vel.z = #crawl_vz {ns}.data
function #bs.move:local_to_canonical
function #bs.move:set_motion {{scale:0.001}}

tp @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] ~ ~2 ~
""")

	write_versioned_function("zombies/revive/check_solo_qr", f"""
# Only when @s is the only in-game player: in co-op a downed Quick Revive owner never self-revives.
execute store result score #zb_ingame_total {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute if score #zb_ingame_total {ns}.data matches 2.. run return 0
function {ns}:v{version}/zombies/revive/solo_qr_tick
""")

	## Fills over {SOLO_QR_TICKS} ticks.
	write_versioned_function("zombies/revive/solo_qr_tick", f"""
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run return 0

# #zb_reviving 2 skips the decay logic.
scoreboard players set #zb_reviving {ns}.data 2

scoreboard players operation @s {ns}.zb.revive_p += #tick_delta {ns}.data

scoreboard players operation #rv_qr_sec {ns}.data = @s {ns}.zb.revive_p
scoreboard players operation #rv_qr_sec {ns}.data /= #20 {ns}.data
scoreboard players operation #rv_qr_tenth {ns}.data = @s {ns}.zb.revive_p
scoreboard players operation #rv_qr_tenth {ns}.data %= #20 {ns}.data
scoreboard players operation #rv_qr_tenth {ns}.data /= #2 {ns}.data
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚡ ","color":"white"}},{{"text":"Solo Quick Revive: ","color":"aqua"}},{{"score":{{"name":"#rv_qr_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_qr_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {SOLO_QR_TICKS // 20}.{(SOLO_QR_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message

execute if score @s {ns}.zb.revive_p matches {SOLO_QR_TICKS}.. run function {ns}:v{version}/zombies/revive/solo_qr_complete
""")

	write_versioned_function("zombies/revive/solo_qr_complete", f"""
scoreboard players add @s {ns}.zb.qr_uses 1

# The perk must be rebought after each use; lose_all already took perk.quick_revive.
tag @s remove {ns}.perk.quick_revive
tag @s remove {ns}.zb_qr_armed

# {ns}.zb.qr_uses caps the uses (see perks/on_right_click).
scoreboard players set @s {ns}.zb.perk.quick_revive 0
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive exhausted! ({SOLO_QR_MAX}/{SOLO_QR_MAX}) No more self-revives this game.","color":"dark_red"}}]
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive used! ({SOLO_QR_MAX - 1 if SOLO_QR_MAX > 1 else 0}/{SOLO_QR_MAX}) Rebuy for another self-revive.","color":"gray"}}]

function {ns}:v{version}/zombies/revive/revive_complete
""")

