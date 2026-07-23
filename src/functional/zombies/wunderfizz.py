
# ruff: noqa: E501
# Der Wunderfizz — a Mystery-Box-style machine that grants a RANDOM perk.
# Like the Mystery Box, a map can hold SEVERAL Wunderfizz spots but only ONE is active at a time; the
# rest show a grayed-out "disabled" cabinet (der_wunderfizz_disabled) marking where it might roam to.
# After a few uses the active machine can roam to another spot (teddy-bear move easter egg, shared with
# the Mystery Box via zombies/roaming.py). The roam is a model-swap (old spot → disabled, new spot →
# live) rather than physically flying the big cabinet, with the bear as the visual cue.
# On use it cycles perk bottles, lands on a random perk the buyer doesn't own, and leaves it
# collectable by the buyer only for 10s. The pool is the shared "available perk pool" helper
# (zombies/perks/pool/*): perks with a machine on this map, widened to every perk when the editor
# `all_perks` flag is set (BO2 Origins behaviour).
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from .common import deny_not_enough_points_body, deny_requires_power_body, game_active_guard_cmd
from .perks import PERK_DEFINITIONS

# Roam move animation length (ticks). The bear rises, the machine relocates (model swap) at the
# midpoint, then settles. In-engine timing polish is a HUMAN eyeball pass.
WF_MOVE_TICKS: int = 100
WF_MOVE_RELOCATE: int = 55		# tick the active spot actually changes (model swap + visibility)
WF_MOVE_BEAR_POOF: int = 48		# tick the bear despawns
# Uses on the active machine before it may roll to roam (mirrors the Mystery Box's 4-pull threshold)
WF_MOVE_THRESHOLD: int = 4


def generate_wunderfizz() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	perk_ids: list[str] = list(PERK_DEFINITIONS)
	num_perks: int = len(perk_ids)

	## State objectives
	write_load_file(f"""
# Der Wunderfizz machine + spin state
scoreboard objectives add {ns}.zb.wf.id dummy
scoreboard objectives add {ns}.zb.wf.price dummy
scoreboard objectives add {ns}.zb.wf.power dummy
scoreboard objectives add {ns}.zb.wf.allperks dummy
# Spin display (orb): countdown timer (>0 spinning, <=0 ready window), buyer pid, chosen perk index
scoreboard objectives add {ns}.zb.wf.anim dummy
scoreboard objectives add {ns}.zb.wf.buyer dummy
scoreboard objectives add {ns}.zb.wf.perk dummy
# 1 when the buyer owns Timeslip (this orb spins 2x faster, like the Mystery Box)
scoreboard objectives add {ns}.zb.wf.timeslip dummy
# 1 when this pull will roam the machine (teddy bear) instead of granting a perk
scoreboard objectives add {ns}.zb.wf.willmove dummy
# Points paid for this pull, so a roam (bear) can refund the buyer
scoreboard objectives add {ns}.zb.wf.paid dummy
# Stable per-player buyer id (lazy)
scoreboard objectives add {ns}.zb.wf_pid dummy
""")

	## Setup: iterate wunderfizz compounds, summon interaction + a persistent machine display each,
	## then pick ONE active spot (prefer can_start_on markers), light it up and park the rest.
	write_versioned_function("zombies/wunderfizz/setup", f"""
scoreboard players set #wf_counter {ns}.data 0
data modify storage {ns}:temp _wf_iter set from storage {ns}:zombies game.map.wunderfizz
execute if data storage {ns}:temp _wf_iter[0] run function {ns}:v{version}/zombies/wunderfizz/setup_iter

# Pick the active spot: a random can_start_on marker, else any marker
execute as @n[tag={ns}.wunderfizz_machine,tag={ns}.wf_can_start,sort=random] run tag @s add {ns}.wf_active
execute unless entity @e[tag={ns}.wf_active] as @n[tag={ns}.wunderfizz_machine,sort=random] run tag @s add {ns}.wf_active

scoreboard players set #wf_uses {ns}.data 0
scoreboard players set #wf_move_timer {ns}.data 0

# Live model on the active cabinet, grayed disabled model on the rest, and park inactive interactions
function {ns}:v{version}/zombies/wunderfizz/sync_displays
function {ns}:v{version}/zombies/wunderfizz/sync_visibility
""")

	write_versioned_function("zombies/wunderfizz/setup_iter", f"""
scoreboard players add #wf_counter {ns}.data 1

# Relative -> absolute position
execute store result score #wfx {ns}.data run data get storage {ns}:temp _wf_iter[0].pos[0]
execute store result score #wfy {ns}.data run data get storage {ns}:temp _wf_iter[0].pos[1]
execute store result score #wfz {ns}.data run data get storage {ns}:temp _wf_iter[0].pos[2]
scoreboard players operation #wfx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #wfy {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #wfz {ns}.data += #gm_base_z {ns}.data
execute store result storage {ns}:temp _wf.x int 1 run scoreboard players get #wfx {ns}.data
execute store result storage {ns}:temp _wf.y int 1 run scoreboard players get #wfy {ns}.data
execute store result storage {ns}:temp _wf.z int 1 run scoreboard players get #wfz {ns}.data
data modify storage {ns}:temp _wf.rotation set from storage {ns}:temp _wf_iter[0].rotation

# Summon interaction entity
function {ns}:v{version}/zombies/wunderfizz/place_at with storage {ns}:temp _wf

# Metadata on the interaction entity
scoreboard players operation @n[tag={ns}.wf_new] {ns}.zb.wf.id = #wf_counter {ns}.data
execute store result score @n[tag={ns}.wf_new] {ns}.zb.wf.price run data get storage {ns}:temp _wf_iter[0].price
execute store result score @n[tag={ns}.wf_new] {ns}.zb.wf.power run data get storage {ns}:temp _wf_iter[0].power
execute store result score @n[tag={ns}.wf_new] {ns}.zb.wf.allperks run data get storage {ns}:temp _wf_iter[0].all_perks

# Roam start-eligibility (default eligible when the field is absent, like the Mystery Box)
execute unless data storage {ns}:temp _wf_iter[0].can_start_on run tag @n[tag={ns}.wf_new] add {ns}.wf_can_start
data modify storage {ns}:temp _wf_cso set value 0b
execute if data storage {ns}:temp _wf_iter[0].can_start_on run data modify storage {ns}:temp _wf_cso set from storage {ns}:temp _wf_iter[0].can_start_on
execute if data storage {ns}:temp {{_wf_cso:1b}} run tag @n[tag={ns}.wf_new] add {ns}.wf_can_start

# Bookshelf events
execute as @n[tag={ns}.wf_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/wunderfizz/on_right_click",executor:"source"}}
execute as @n[tag={ns}.wf_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/wunderfizz/on_hover",executor:"source"}}

# Machine display (perk-machine pipeline, custom Wunderfizz model unless the map overrode it).
# Summoned as the DEFAULT (disabled) model; sync_displays lights up the active one afterwards.
data modify storage {ns}:temp _wf_disp.tag set value "{ns}.wf_display"
data modify storage {ns}:temp _wf_disp.item_id set value ""
data modify storage {ns}:temp _wf_disp.item_model set value ""
data modify storage {ns}:temp _wf_disp.yaw set value 0.0
execute if data storage {ns}:temp _wf_iter[0].display_item run data modify storage {ns}:temp _wf_disp.item_id set from storage {ns}:temp _wf_iter[0].display_item
execute if data storage {ns}:temp _wf_iter[0].item_model run data modify storage {ns}:temp _wf_disp.item_model set from storage {ns}:temp _wf_iter[0].item_model
execute if data storage {ns}:temp _wf_disp{{item_id:""}} run data modify storage {ns}:temp _wf_disp.item_id set value "minecraft:potion"
execute if data storage {ns}:temp _wf_disp{{item_model:""}} run data modify storage {ns}:temp _wf_disp.item_model set value "{ns}:der_wunderfizz"
execute if data storage {ns}:temp _wf_iter[0].rotation[0] run data modify storage {ns}:temp _wf_disp.yaw set from storage {ns}:temp _wf_iter[0].rotation[0]
execute as @n[tag={ns}.wf_new] at @s align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _wf_disp

# Link the freshly summoned display to this position id (there is exactly one unlinked display now)
scoreboard players operation @e[tag={ns}.wf_display,tag=!{ns}.wf_linked] {ns}.zb.wf.id = @n[tag={ns}.wf_new] {ns}.zb.wf.id
tag @e[tag={ns}.wf_display,tag=!{ns}.wf_linked] add {ns}.wf_linked

execute as @n[tag={ns}.wf_new] at @s run tp @s ~ ~2 ~
tag @n[tag={ns}.wf_new] add {ns}.wunderfizz_machine
tag @n[tag={ns}.wf_new] remove {ns}.wf_new

data remove storage {ns}:temp _wf_iter[0]
execute if data storage {ns}:temp _wf_iter[0] run function {ns}:v{version}/zombies/wunderfizz/setup_iter
""")

	write_versioned_function("zombies/wunderfizz/place_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.2f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["{ns}.wunderfizz_machine","{ns}.gm_entity","bs.entity.interaction","{ns}.wf_new"]}}
""")

	## Light up the active cabinet (live model), gray out every other (disabled model). Displays are
	## persistent and id-linked to their spot, so roaming is just a model swap.
	write_versioned_function("zombies/wunderfizz/sync_displays", f"""
execute as @e[tag={ns}.wf_display] run function {ns}:v{version}/zombies/wunderfizz/set_display_disabled
scoreboard players set #wf_active_id {ns}.data -1
execute as @n[tag={ns}.wf_active] run scoreboard players operation #wf_active_id {ns}.data = @s {ns}.zb.wf.id
execute as @e[tag={ns}.wf_display] if score @s {ns}.zb.wf.id = #wf_active_id {ns}.data run function {ns}:v{version}/zombies/wunderfizz/set_display_live
""")

	write_versioned_function("zombies/wunderfizz/set_display_live", f"""
data modify entity @s item.components."minecraft:item_model" set value "{ns}:der_wunderfizz"
""")
	write_versioned_function("zombies/wunderfizz/set_display_disabled", f"""
data modify entity @s item.components."minecraft:item_model" set value "{ns}:der_wunderfizz_disabled"
""")

	## Keep only the active machine's interaction entity reachable; park the rest ±512 out of reach
	## (shared roaming primitive) so an inactive cabinet can't be hovered/clicked.
	write_versioned_function("zombies/wunderfizz/sync_visibility", f"""
execute as @e[tag={ns}.wunderfizz_machine] at @s run function {ns}:v{version}/zombies/wunderfizz/sync_visibility_one
""")
	write_versioned_function("zombies/wunderfizz/sync_visibility_one", f"""
execute if entity @s[tag={ns}.wf_active] if entity @s[tag={ns}.roam_hidden] run function {ns}:v{version}/zombies/roaming/interaction_show
execute unless entity @s[tag={ns}.wf_active] unless entity @s[tag={ns}.roam_hidden] run function {ns}:v{version}/zombies/roaming/interaction_hide
""")

	## Right-click (executor "source" = player)
	write_versioned_function("zombies/wunderfizz/on_right_click", f"""
{game_active_guard_cmd(ns)}

# Usable only on the active machine, or a machine that still has an orb here to collect
scoreboard players set #wf_usable {ns}.data 0
execute if entity @e[tag=bs.interaction.target,tag={ns}.wf_active] run scoreboard players set #wf_usable {ns}.data 1
execute at @n[tag=bs.interaction.target] if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] run scoreboard players set #wf_usable {ns}.data 1
execute if score #wf_usable {ns}.data matches 0 run return fail

# The active machine can be mid-roam: deny
execute if score #wf_move_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.wf_active] run return run function {ns}:v{version}/zombies/wunderfizz/deny_moving

# Power requirement
execute store result score #wf_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wf.power
execute if score #wf_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run function {ns}:v{version}/zombies/wunderfizz/deny_requires_power

# Capture this machine's config (scores persist into the dispatched function)
scoreboard players operation #wf_mid {ns}.data = @n[tag=bs.interaction.target] {ns}.zb.wf.id
scoreboard players operation #wf_price {ns}.data = @n[tag=bs.interaction.target] {ns}.zb.wf.price
scoreboard players operation #wf_allperks {ns}.data = @n[tag=bs.interaction.target] {ns}.zb.wf.allperks

execute at @n[tag=bs.interaction.target] run function {ns}:v{version}/zombies/wunderfizz/machine_click
""")

	## Dispatch a click at a specific machine (@s = player, positioned at the machine)
	write_versioned_function("zombies/wunderfizz/machine_click", f"""
# Spinning here → in use
execute if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3,scores={{{ns}.zb.wf.anim=1..}}] run return run function {ns}:v{version}/zombies/wunderfizz/deny_in_use

# A ready orb here → only the buyer may collect
execute if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] if score @s {ns}.zb.wf_pid = @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] {ns}.zb.wf.buyer run return run function {ns}:v{version}/zombies/wunderfizz/collect
execute if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] run return run function {ns}:v{version}/zombies/wunderfizz/deny_not_your_result

# Nothing here yet: start a spin
function {ns}:v{version}/zombies/wunderfizz/try_use
""")

	## Start a spin (@s = player, positioned at the machine; #wf_price / #wf_allperks / #wf_mid set)
	write_versioned_function("zombies/wunderfizz/try_use", f"""
execute unless score @s {ns}.zb.points >= #wf_price {ns}.data run return run function {ns}:v{version}/zombies/wunderfizz/deny_not_enough_points
scoreboard players operation @s {ns}.zb.points -= #wf_price {ns}.data

# Stable buyer id
execute unless score @s {ns}.zb.wf_pid matches 1.. run function {ns}:v{version}/zombies/wunderfizz/assign_pid

# Pick a random available perk via the shared pool (all_perks widens it to every perk)
tag @s add {ns}.pool_target
scoreboard players operation #pool_all_perks {ns}.data = #wf_allperks {ns}.data
function {ns}:v{version}/zombies/perks/pool/choose
tag @s remove {ns}.pool_target

# No perk available → refund + notify
execute if score #pool_chosen {ns}.data matches ..-1 run scoreboard players operation @s {ns}.zb.points += #wf_price {ns}.data
execute if score #pool_chosen {ns}.data matches ..-1 run return run function {ns}:v{version}/zombies/wunderfizz/deny_all_owned

# Decide whether this pull roams the machine (teddy bear) instead of granting a perk. Shared rule
# with the Mystery Box (roaming/roll_move): after WF_MOVE_THRESHOLD uses, 1-in-3 chance. Needs >=2
# placed spots to have somewhere to go.
scoreboard players add #wf_uses {ns}.data 1
scoreboard players operation #roam_uses {ns}.data = #wf_uses {ns}.data
scoreboard players set #roam_threshold {ns}.data {WF_MOVE_THRESHOLD}
function {ns}:v{version}/zombies/roaming/roll_move
scoreboard players operation #wf_will_move {ns}.data = #roam_will_move {ns}.data
execute store result score #wf_pos_count {ns}.data run data get storage {ns}:zombies game.map.wunderfizz
execute if score #wf_pos_count {ns}.data matches ..1 run scoreboard players set #wf_will_move {ns}.data 0
execute if score #wf_will_move {ns}.data matches 1 run scoreboard players set #wf_uses {ns}.data 0

# Spawn the spinning orb above the machine and stamp it
function {ns}:v{version}/zombies/wunderfizz/spawn_orb
scoreboard players operation @n[tag={ns}.wf_orb_new] {ns}.zb.wf.buyer = @s {ns}.zb.wf_pid
scoreboard players operation @n[tag={ns}.wf_orb_new] {ns}.zb.wf.perk = #pool_chosen {ns}.data
scoreboard players operation @n[tag={ns}.wf_orb_new] {ns}.zb.wf.paid = #wf_price {ns}.data
scoreboard players operation @n[tag={ns}.wf_orb_new] {ns}.zb.wf.willmove = #wf_will_move {ns}.data
scoreboard players set @n[tag={ns}.wf_orb_new] {ns}.zb.wf.anim 100
# Timeslip: this buyer's spin runs 2x faster (see orb_tick)
scoreboard players set @n[tag={ns}.wf_orb_new] {ns}.zb.wf.timeslip 0
execute if score @s {ns}.special.timeslip matches 1.. run scoreboard players set @n[tag={ns}.wf_orb_new] {ns}.zb.wf.timeslip 1
tag @e[tag={ns}.wf_orb_new] remove {ns}.wf_orb_new

playsound minecraft:block.conduit.activate ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.2
playsound minecraft:block.beacon.activate ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.6 1.6
tellraw @s [{MGS_TAG},{{"text":"Der Wunderfizz spinning...","color":"gold"}}]
""")

	write_versioned_function("zombies/wunderfizz/assign_pid", f"""
scoreboard players add #wf_pid_counter {ns}.data 1
scoreboard players operation @s {ns}.zb.wf_pid = #wf_pid_counter {ns}.data
""")

	## Spawn the orb display inside the machine's open middle alcove (@s = player, at machine).
	## NOTE the orb spawns `at` the interaction entity, which setup_iter tp'd UP by 2 (line ~83)
	## AFTER placing the machine display. So the orb origin sits ~2 blocks above the model. The
	## alcove centre (model y≈15.5, display at interaction_orig+0.63, scale 1.25) lands at roughly
	## interaction_final - 0.78, hence the negative Y. scale 0.4 keeps the bottle clear of the
	## alcove walls. Nudge Y ±0.15 if it drifts.
	write_versioned_function("zombies/wunderfizz/spawn_orb", f"""
summon minecraft:item_display ~ ~-0.78 ~ {{Tags:["{ns}.wunderfizz_orb","{ns}.wf_orb_new","{ns}.gm_entity"],Glowing:true,billboard:"vertical",item_display:"fixed",item:{{id:"minecraft:potion",count:1}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.2f,0.2f,0.2f]}}}}
""")

	## Per-tick orb processing (hooked into game_tick)
	write_versioned_function("zombies/wunderfizz/orb_tick", f"""
particle minecraft:end_rod ~ ~ ~ 0.25 0.25 0.25 0.02 1 force @a[distance=..48]
particle minecraft:electric_spark ~ ~0.3 ~ 0.3 0.3 0.3 0.05 1 force @a[distance=..48]

scoreboard players remove @s {ns}.zb.wf.anim 1
# Timeslip: 2x spin speed. The extra -1 only fires while still spinning (anim>0), and anim starts
# even (100) so the doubled step always lands exactly on the anim==0 landing and never overshoots
# into the ready window (which still counts down at normal speed, so the pickup window is unchanged).
execute if score @s {ns}.zb.wf.timeslip matches 1 if score @s {ns}.zb.wf.anim matches 1.. run scoreboard players remove @s {ns}.zb.wf.anim 1
execute if score @s {ns}.zb.wf.anim matches 1.. run function {ns}:v{version}/zombies/wunderfizz/spin_cycle
execute if score @s {ns}.zb.wf.anim matches 0 run function {ns}:v{version}/zombies/wunderfizz/land
execute if score @s {ns}.zb.wf.anim matches ..-200 run function {ns}:v{version}/zombies/wunderfizz/orb_expire
""")

	## Cycle the displayed perk bottle every 3 ticks during the spin (@s = orb)
	roll_dispatch: str = "\n".join(
		f"execute if score #wf_roll {ns}.data matches {i} run function {ns}:v{version}/zombies/wunderfizz/set_model/{pid}"
		for i, pid in enumerate(perk_ids)
	)
	write_versioned_function("zombies/wunderfizz/spin_cycle", f"""
scoreboard players operation #wf_mod {ns}.data = @s {ns}.zb.wf.anim
scoreboard players operation #wf_mod {ns}.data %= #3 {ns}.data
execute unless score #wf_mod {ns}.data matches 0 run return 0
execute store result score #wf_roll {ns}.data run random value 0..{num_perks - 1}
{roll_dispatch}
# Electric spin feedback (vanilla sounds): a spark + a short conduit zap each cycle
particle minecraft:electric_spark ~ ~ ~ 0.25 0.3 0.25 0.05 3 force @a[distance=..32]
playsound minecraft:block.conduit.ambient.short ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.5 1.4
""")

	## Landing (@s = orb): a roam pull turns into a teddy bear; otherwise show the chosen perk bottle.
	land_dispatch: str = "\n".join(
		f"execute if score @s {ns}.zb.wf.perk matches {i} run function {ns}:v{version}/zombies/wunderfizz/set_model/{pid}"
		for i, pid in enumerate(perk_ids)
	)
	write_versioned_function("zombies/wunderfizz/land", f"""
# Roam pull: the machine is about to move — show the bear, refund the buyer, no perk
execute if score @s {ns}.zb.wf.willmove matches 1 run return run function {ns}:v{version}/zombies/wunderfizz/land_bear

{land_dispatch}
particle minecraft:totem_of_undying ~ ~ ~ 0.3 0.4 0.3 0.2 10 force @a[distance=..48]
particle minecraft:electric_spark ~ ~ ~ 0.4 0.5 0.4 0.15 10 force @a[distance=..48]
playsound minecraft:block.beacon.deactivate ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.8 1.4
playsound minecraft:entity.lightning_bolt.impact ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.5 1.7
function {ns}:v{version}/zombies/feedback/sound_announce
scoreboard players operation #wf_b {ns}.data = @s {ns}.zb.wf.buyer
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.zb.wf_pid = #wf_b {ns}.data run tellraw @s [{MGS_TAG},{{"text":"Perk ready! ","color":"gold"}},{{"text":"Right-click Der Wunderfizz to collect!","color":"green","bold":true}}]
""")

	## Roam landing (@s = orb, positioned at the active machine): refund the buyer, then start the move.
	write_versioned_function("zombies/wunderfizz/land_bear", f"""
# Refund the buyer (the machine roams away instead of granting a perk — Black Ops teddy-bear rule)
scoreboard players operation #wf_b {ns}.data = @s {ns}.zb.wf.buyer
scoreboard players operation #wf_refund {ns}.data = @s {ns}.zb.wf.paid
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.zb.wf_pid = #wf_b {ns}.data run scoreboard players operation @s {ns}.zb.points += #wf_refund {ns}.data

tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Der Wunderfizz is moving!","color":"yellow","bold":true}}]
function {ns}:v{version}/zombies/feedback/sound_box_bye_bye

# Spawn the teddy bear at the active machine and start the roam timer, then remove the orb
execute as @n[tag={ns}.wf_active] at @s run function {ns}:v{version}/zombies/wunderfizz/move_start
kill @s
""")

	## Begin the roam (@s = active interaction entity, at @s). Spawn a rising teddy bear near the
	## cabinet and start the move timer.
	write_versioned_function("zombies/wunderfizz/move_start", f"""
execute positioned ~ ~-1.5 ~ run summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.wf_bear","{ns}.gm_entity","{ns}.wf_bear_new"],item_display:"fixed",billboard:"fixed",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}}}
loot replace entity @n[tag={ns}.wf_bear_new] contents loot {ns}:zombies/roaming_bear
data merge entity @n[tag={ns}.wf_bear_new] {{teleport_duration:2}}
tag @e[tag={ns}.wf_bear_new] remove {ns}.wf_bear_new
scoreboard players set #wf_move_timer {ns}.data {WF_MOVE_TICKS}
""")

	## Roam tick (hooked into game_tick while #wf_move_timer > 0)
	write_versioned_function("zombies/wunderfizz/move_tick", f"""
scoreboard players remove #wf_move_timer {ns}.data 1

# Bear rises before the swap
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_RELOCATE + 1}.. as @e[tag={ns}.wf_bear] at @s run tp @s ~ ~0.06 ~

# Midpoint: relocate the active spot (model swap + interaction visibility)
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_RELOCATE} run function {ns}:v{version}/zombies/wunderfizz/do_relocate

# Bear poofs shortly after
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_BEAR_POOF} as @e[tag={ns}.wf_bear] at @s run particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.02 15 force @a[distance=..48]
execute if score #wf_move_timer {ns}.data matches {WF_MOVE_BEAR_POOF} run kill @e[tag={ns}.wf_bear]

# Arrival
execute if score #wf_move_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/wunderfizz/move_land
""")

	## Swap the active spot to a new random position (@s not required). Old cabinet grays out, new one
	## lights up, interaction reachability follows.
	write_versioned_function("zombies/wunderfizz/do_relocate", f"""
tag @e[tag={ns}.wf_active] add {ns}.wf_prev_active
tag @e[tag={ns}.wf_active] remove {ns}.wf_active
execute as @n[tag={ns}.wunderfizz_machine,tag=!{ns}.wf_prev_active,sort=random] run tag @s add {ns}.wf_active
tag @e[tag={ns}.wf_prev_active] remove {ns}.wf_prev_active

function {ns}:v{version}/zombies/wunderfizz/sync_displays
function {ns}:v{version}/zombies/wunderfizz/sync_visibility

# Arrival particles/sound at the new active cabinet
execute as @n[tag={ns}.wf_active] at @s run particle minecraft:end_rod ~ ~-1 ~ 0.3 1.5 0.3 0.05 25 force @a[distance=..64]
execute as @n[tag={ns}.wf_active] at @s run playsound minecraft:entity.lightning_bolt.impact ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.6 1.6
""")

	write_versioned_function("zombies/wunderfizz/move_land", f"""
scoreboard players set #wf_move_timer {ns}.data 0
kill @e[tag={ns}.wf_bear]
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Der Wunderfizz has arrived at a new location!","color":"yellow"}}]
execute as @n[tag={ns}.wf_active] at @s run function {ns}:v{version}/zombies/feedback/sound_announce
""")

	## Orb model setters + grant functions, one per perk
	for pid in perk_ids:
		write_versioned_function(f"zombies/wunderfizz/set_model/{pid}", f"""
data modify entity @s item set value {{id:"minecraft:potion",count:1,components:{{"minecraft:item_model":"{ns}:perk_machine_{pid}"}}}}
""")
		write_versioned_function(f"zombies/wunderfizz/grant/{pid}", f"""
data modify storage {ns}:temp _wf_grant.perk_id set value "{pid}"
function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _wf_grant
function #{ns}:zombies/on_new_perk
""")

	## Uncollected after the 10s window (@s = orb): despawn (no refund — the spin already happened)
	write_versioned_function("zombies/wunderfizz/orb_expire", """
particle minecraft:smoke ~ ~ ~ 0.2 0.2 0.2 0.02 10 force @a[distance=..48]
kill @s
""")

	## Collect (@s = player, at machine): apply the orb's chosen perk, then despawn the orb
	collect_dispatch: str = "\n".join(
		f"execute if score #wf_pick {ns}.data matches {i} run function {ns}:v{version}/zombies/wunderfizz/grant/{pid}"
		for i, pid in enumerate(perk_ids)
	)
	write_versioned_function("zombies/wunderfizz/collect", f"""
scoreboard players operation #wf_pick {ns}.data = @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] {ns}.zb.wf.perk
{collect_dispatch}
kill @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3]
function {ns}:v{version}/zombies/feedback/sound_success
""")

	## Hover
	write_versioned_function("zombies/wunderfizz/on_hover", f"""
# If this player's perk is ready to collect here, prompt the pick-up (with the perk name) instead of the cost
execute at @n[tag=bs.interaction.target] if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3,scores={{{ns}.zb.wf.anim=..0}}] if score @s {ns}.zb.wf_pid = @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] {ns}.zb.wf.buyer run return run function {ns}:v{version}/zombies/wunderfizz/hover_result

execute store result score #wf_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wf.price
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🎰 Der Wunderfizz","color":"gold"}},{{"text":" - Cost: ","color":"gray"}},{{"score":{{"name":"#wf_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points  (random perk)","color":"gray"}}],priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	## Ready-orb hover: name the perk waiting to be collected, e.g. "✋ Pick-up Juggernog"
	## (@s = player, positioned at the machine so the nearby orb resolves)
	hover_result_dispatch: str = "\n".join(
		f'execute if score #wf_pick {ns}.data matches {i} run data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🎰 ","color":"gold"}},{{"text":"Pick-up ","color":"green"}},{{"text":"{PERK_DEFINITIONS[pid]["display_name"]}","color":"{PERK_DEFINITIONS[pid]["text_color"]}","bold":true}}],priority:"conditional",freeze:5}}'
		for i, pid in enumerate(perk_ids)
	)
	write_versioned_function("zombies/wunderfizz/hover_result", f"""
scoreboard players operation #wf_pick {ns}.data = @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] {ns}.zb.wf.perk
{hover_result_dispatch}
function #smithed.actionbar:message
""")

	## Deny messages
	write_versioned_function("zombies/wunderfizz/deny_requires_power", f"""
{deny_requires_power_body(ns, version, "Der Wunderfizz")}
""")
	write_versioned_function("zombies/wunderfizz/deny_not_enough_points", f"""
{deny_not_enough_points_body(ns, version, "#wf_price")}
""")
	write_versioned_function("zombies/wunderfizz/deny_in_use", f"""
tellraw @s [{MGS_TAG},{{"text":"Der Wunderfizz is already spinning.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")
	write_versioned_function("zombies/wunderfizz/deny_moving", f"""
tellraw @s [{MGS_TAG},{{"text":"Der Wunderfizz is moving...","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")
	write_versioned_function("zombies/wunderfizz/deny_not_your_result", f"""
tellraw @s [{MGS_TAG},{{"text":"Wait for the buyer to collect their perk.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")
	write_versioned_function("zombies/wunderfizz/deny_all_owned", f"""
tellraw @s [{MGS_TAG},{{"text":"You already own every available perk. Points refunded.","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	## Hook: setup at preload_complete
	write_versioned_function("zombies/preload_complete", f"""
execute if data storage {ns}:zombies game.map.wunderfizz[0] run function {ns}:v{version}/zombies/wunderfizz/setup
""")

	## Hook: tick orbs + any active roam
	write_versioned_function("zombies/game_tick", f"""
execute as @e[type=item_display,tag={ns}.wunderfizz_orb] at @s run function {ns}:v{version}/zombies/wunderfizz/orb_tick
execute if score #wf_move_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/wunderfizz/move_tick
""")

	## Hook: clean up machines/orbs/bears on game start/stop
	write_versioned_function("zombies/start", f"""
kill @e[type=item_display,tag={ns}.wunderfizz_orb]
kill @e[tag={ns}.wf_display]
kill @e[tag={ns}.wf_bear]
scoreboard players set #wf_uses {ns}.data 0
scoreboard players set #wf_move_timer {ns}.data 0
""")
	write_versioned_function("zombies/stop", f"""
kill @e[type=item_display,tag={ns}.wunderfizz_orb]
kill @e[tag={ns}.wf_display]
kill @e[tag={ns}.wf_bear]
scoreboard players set #wf_uses {ns}.data 0
scoreboard players set #wf_move_timer {ns}.data 0
""")
