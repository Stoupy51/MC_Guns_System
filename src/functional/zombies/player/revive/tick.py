""" The downed tick: crawling, the single mannequin pass and solo Quick Revive. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from .shared import CRAWL_SPEED, SOLO_QR_MAX, SOLO_QR_TICKS, revive_body_detect, revive_body_progress


# Functions
def write_downed_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Tick: process all downed spectating players
	write_versioned_function("zombies/revive/tick", f"""
# Process each spectating (downed) player
execute as @a[tag={ns}.downed_spectator,scores={{{ns}.zb.in_game=1}}] at @s run function {ns}:v{version}/zombies/revive/downed_tick
""")

	## Downed tick: per-player (run as the spectating downed player)
	write_versioned_function("zombies/revive/downed_tick", f"""
# Identify THIS player's downed entities for the id-matching predicate, then tag the mannequin ONCE
# as downed_mine_temp. Every per-mannequin command below reuses that tag (or a single dispatch into
# move_mannequin) instead of re-selecting the mannequin ~11x per tick.
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
tag @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] add {ns}.downed_mine_temp

# Read crawl inputs into scratch scores while @s is still the player (predicate self-checks on @s,
# no entity scan). These drive the mannequin's local velocity inside move_mannequin.
# Also snapshot the owner's yaw (x100): move_mannequin must not use a "nearest downed spectator"
# lookup, which binds to the wrong owner when several mannequins are close together.
execute store result score #rv_yaw {ns}.data run data get entity @s Rotation[0] 100
scoreboard players set #crawl_vx {ns}.data 0
scoreboard players set #crawl_vz {ns}.data 0
execute if entity @s[predicate={ns}:v{version}/input/forward] run scoreboard players set #crawl_vz {ns}.data {int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/backward] run scoreboard players set #crawl_vz {ns}.data -{int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/left] run scoreboard players set #crawl_vx {ns}.data {int(CRAWL_SPEED * 1000)}
execute if entity @s[predicate={ns}:v{version}/input/right] run scoreboard players set #crawl_vx {ns}.data -{int(CRAWL_SPEED * 1000)}

# Third-person camera: position the cam item_display 2 up / 3 behind the mannequin (using the
# mannequin's CURRENT rotation, i.e. before this tick's yaw sync — same order as before), then
# re-mount the player onto the cam so the view follows it.
execute at @n[tag={ns}.downed_mine_temp] as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run tp @s ^ ^2 ^-3
ride @s mount @n[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match]

# All remaining per-mannequin work (yaw sync, crawl motion, HUD anchor) in ONE pass over the tagged
# mannequin instead of re-selecting it for each command.
execute as @n[tag={ns}.downed_mine_temp] at @s run function {ns}:v{version}/zombies/revive/move_mannequin

# Done with the per-tick mannequin tag
tag @e[tag={ns}.downed_mine_temp] remove {ns}.downed_mine_temp

{revive_body_detect()}

# Solo Quick Revive auto-revive: if no teammates in-game and player has quick_revive + uses left
execute if score #zb_reviving {ns}.data matches 0 if entity @s[tag={ns}.perk.quick_revive] unless score #zb_solo_revive_block {ns}.data matches 1 run function {ns}:v{version}/zombies/revive/check_solo_qr

# Show bleed timer on downed player's actionbar ONLY when not in solo QR (which has its own actionbar)
# Compute display: whole seconds and tenths digit (sec = bleed/20, tenth = (bleed%20)/2)
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_sec {ns}.data = @s {ns}.zb.bleed
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_sec {ns}.data /= #20 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data = @s {ns}.zb.bleed
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data %= #20 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run scoreboard players operation #rv_disp_tenth {ns}.data /= #2 {ns}.data
execute if score #zb_reviving {ns}.data matches ..1 run data modify storage smithed.actionbar:input message set value {{json:[{{"text":"☠ Bleeding out: ","color":"red"}},{{"score":{{"name":"#rv_disp_sec","objective":"{ns}.data"}},"color":"gray"}},{{"text":".","color":"gray"}},{{"score":{{"name":"#rv_disp_tenth","objective":"{ns}.data"}},"color":"gray"}},{{"text":"s","color":"dark_gray"}}],priority:"override",freeze:2}}
execute if score #zb_reviving {ns}.data matches ..1 run function #smithed.actionbar:message

{revive_body_progress(f"{ns}:v{version}/zombies/revive/revive_complete")}

# Bleed out: time's up
execute if score @s {ns}.zb.bleed matches ..0 run function {ns}:v{version}/zombies/revive/bleed_out

# Instant bleed out: if no healthy players remain and no solo QR auto-revive is active,
# there is no hope of revive — end the suspense immediately
execute if score #zb_reviving {ns}.data matches 0 unless entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/revive/bleed_out
""")

	## All per-mannequin downed work in one pass.
	## @s = the downed player's mannequin, executed at it (dispatched once per downed player from downed_tick after tagging the mannequin downed_mine_temp).
	## Folds the former ~11 separate `@e[tag=downed_mannequin,predicate=...]` selections into a single entity selection; everything here is @s (the mannequin) or a local @p/@n lookup.
	## Crawl direction arrives via #crawl_vx/#crawl_vz (set on the player before dispatch).
	## Order matches the old inline version: yaw sync first, then velocity, then local->canonical, then motion, then HUD anchor.
	write_versioned_function("zombies/revive/move_mannequin", f"""
# Sync mannequin yaw from the owner's look direction (snapshotted into #rv_yaw x100 by downed_tick)
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #rv_yaw {ns}.data
data modify entity @s Rotation[1] set value 0.0f

# Crawl motion via Bookshelf physics. XZ from the crawl-input scratch scores (0 when no input is held);
# Y a constant downward pull so the mannequin doesn't float off ledges (set_motion overrides gravity).
scoreboard players operation @s bs.vel.x = #crawl_vx {ns}.data
scoreboard players set @s bs.vel.y -400
scoreboard players operation @s bs.vel.z = #crawl_vz {ns}.data
function #bs.move:local_to_canonical
function #bs.move:set_motion {{scale:0.001}}

# Keep the HUD text_display anchored 2 blocks above the mannequin (id-matched via #my_downed_id)
tp @n[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] ~ ~2 ~
""")

	# Solo Quick Revive check: auto-revive if alone in game
	write_versioned_function("zombies/revive/check_solo_qr", f"""
# Only trigger in a TRUE solo game: @s must be the only in-game player. Teammates being
# downed or bled-out does NOT make the game solo — in co-op, a downed player with Quick
# Revive must never self-revive (all players down with no reviver = game over instead).
execute store result score #zb_ingame_total {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}}]
execute if score #zb_ingame_total {ns}.data matches 2.. run return 0
function {ns}:v{version}/zombies/revive/solo_qr_tick
""")

	## Solo QR tick: auto-increment revive progress (uses {SOLO_QR_TICKS} ticks total)
	write_versioned_function("zombies/revive/solo_qr_tick", f"""
# Check player has uses remaining
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run return 0

# Signal solo reviving so decay logic is skipped (set #zb_reviving=2)
scoreboard players set #zb_reviving {ns}.data 2

# Increment revive_p at normal speed (real-time via #tick_delta)
scoreboard players operation @s {ns}.zb.revive_p += #tick_delta {ns}.data

# Show solo QR auto-revive actionbar with seconds display
scoreboard players operation #rv_qr_sec {ns}.data = @s {ns}.zb.revive_p
scoreboard players operation #rv_qr_sec {ns}.data /= #20 {ns}.data
scoreboard players operation #rv_qr_tenth {ns}.data = @s {ns}.zb.revive_p
scoreboard players operation #rv_qr_tenth {ns}.data %= #20 {ns}.data
scoreboard players operation #rv_qr_tenth {ns}.data /= #2 {ns}.data
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"⚡ Solo Quick Revive: ","color":"aqua"}},{{"score":{{"name":"#rv_qr_sec","objective":"{ns}.data"}},"color":"green"}},{{"text":".","color":"green"}},{{"score":{{"name":"#rv_qr_tenth","objective":"{ns}.data"}},"color":"green"}},{{"text":"s / {SOLO_QR_TICKS // 20}.{(SOLO_QR_TICKS % 20) // 2}s","color":"gray"}}],priority:"override",freeze:2}}
function #smithed.actionbar:message

# Auto-revive once threshold reached
execute if score @s {ns}.zb.revive_p matches {SOLO_QR_TICKS}.. run function {ns}:v{version}/zombies/revive/solo_qr_complete
""")

	## Solo QR complete: consume one use then revive
	write_versioned_function("zombies/revive/solo_qr_complete", f"""
# Consume one Quick Revive use
scoreboard players add @s {ns}.zb.qr_uses 1

# Always remove the QR tag so the player must rebuy each time
tag @s remove {ns}.perk.quick_revive

# If all {SOLO_QR_MAX} uses are exhausted, keep the perk score at 1 to permanently block rebuy
# Otherwise reset to 0 so the machine allows a new purchase
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 1
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {ns}.zb.perk.quick_revive 0
execute if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive exhausted! ({SOLO_QR_MAX}/{SOLO_QR_MAX}) No more self-revives this game.","color":"dark_red"}}]
execute unless score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run tellraw @s [{MGS_TAG},{{"text":"Quick Revive used! ({SOLO_QR_MAX - 1 if SOLO_QR_MAX > 1 else 0}/{SOLO_QR_MAX}) Rebuy for another self-revive.","color":"gray"}}]

# Proceed with revive
function {ns}:v{version}/zombies/revive/revive_complete
""")

