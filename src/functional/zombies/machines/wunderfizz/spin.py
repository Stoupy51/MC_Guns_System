""" Buying a spin: the guards, the orb and the perk it rolls. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon
from .shared import NUM_PERKS, PERK_IDS, WF_MOVE_THRESHOLD, orb_model_cmd


# Functions
def write_wunderfizz_spin() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_requires_power: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This Der Wunderfizz requires power.","color":"red"}')
	deny_in_use: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Der Wunderfizz is already spinning.","color":"red"}')
	deny_moving: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Der Wunderfizz is moving...","color":"yellow"}')
	deny_not_your_result: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Wait for the buyer to collect their perk.","color":"red"}')
	deny_all_owned: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"You already own every available perk. Points refunded.","color":"yellow"}')
	deny_not_enough_points: str = ZombiesCommon.deny_not_enough_points_cmd(ns, version, "#wf_price")

	## Right-click (executor "source" = player)
	write_versioned_function("zombies/wunderfizz/on_right_click", f"""
{ZombiesCommon.game_active_guard_cmd(ns)}

# Usable only on the active machine, or a machine that still has an orb here to collect
scoreboard players set #wf_usable {ns}.data 0
execute if entity @e[tag=bs.interaction.target,tag={ns}.wf_active] run scoreboard players set #wf_usable {ns}.data 1
execute at @n[tag=bs.interaction.target] if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] run scoreboard players set #wf_usable {ns}.data 1
execute if score #wf_usable {ns}.data matches 0 run return fail

# The active machine can be mid-roam: deny
execute if score #wf_move_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.wf_active] run return run {deny_moving}

# Power requirement
execute store result score #wf_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wf.power
execute if score #wf_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run {deny_requires_power}

# Capture this machine's config (scores persist into the dispatched function)
scoreboard players operation #wf_mid {ns}.data = @n[tag=bs.interaction.target] {ns}.zb.wf.id
scoreboard players operation #wf_price {ns}.data = @n[tag=bs.interaction.target] {ns}.zb.wf.price
scoreboard players operation #wf_allperks {ns}.data = @n[tag=bs.interaction.target] {ns}.zb.wf.allperks

execute at @n[tag=bs.interaction.target] run function {ns}:v{version}/zombies/wunderfizz/machine_click
""")

	## Dispatch a click at a specific machine (@s = player, positioned at the machine)
	write_versioned_function("zombies/wunderfizz/machine_click", f"""
# Spinning here → in use
execute if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3,scores={{{ns}.zb.wf.anim=1..}}] run return run {deny_in_use}

# A ready orb here → only the buyer may collect
execute if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] if score @s {ns}.zb.wf_pid = @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] {ns}.zb.wf.buyer run return run function {ns}:v{version}/zombies/wunderfizz/collect
execute if entity @n[type=item_display,tag={ns}.wunderfizz_orb,distance=..3] run return run {deny_not_your_result}

# Nothing here yet: start a spin
function {ns}:v{version}/zombies/wunderfizz/try_use
""")

	## Start a spin (@s = player, positioned at the machine; #wf_price / #wf_allperks / #wf_mid set)
	write_versioned_function("zombies/wunderfizz/try_use", f"""
execute unless score @s {ns}.zb.points >= #wf_price {ns}.data run return run {deny_not_enough_points}
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
execute if score #pool_chosen {ns}.data matches ..-1 run return run {deny_all_owned}

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
	## NOTE the orb spawns `at` the interaction entity, which setup_iter tp'd UP by 2 (line ~83) AFTER placing the machine display.
	## So the orb origin sits ~2 blocks above the model.
	## The alcove centre (model y≈15.5, display at interaction_orig+0.63, scale 1.25) lands at roughly interaction_final - 0.78, hence the negative Y. scale 0.4 keeps the bottle clear of the alcove walls.
	## Nudge Y ±0.15 if it drifts.
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
		f"execute if score #wf_roll {ns}.data matches {i} run {orb_model_cmd(ns, pid)}"
		for i, pid in enumerate(PERK_IDS)
	)
	write_versioned_function("zombies/wunderfizz/spin_cycle", f"""
scoreboard players operation #wf_mod {ns}.data = @s {ns}.zb.wf.anim
scoreboard players operation #wf_mod {ns}.data %= #3 {ns}.data
execute unless score #wf_mod {ns}.data matches 0 run return 0
execute store result score #wf_roll {ns}.data run random value 0..{NUM_PERKS - 1}
{roll_dispatch}
# Electric spin feedback (vanilla sounds): a spark + a short conduit zap each cycle
particle minecraft:electric_spark ~ ~ ~ 0.25 0.3 0.25 0.05 3 force @a[distance=..32]
playsound minecraft:block.conduit.ambient.short ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.5 1.4
""")

	## Landing (@s = orb): a roam pull turns into a teddy bear; otherwise show the chosen perk bottle.
	land_dispatch: str = "\n".join(
		f"execute if score @s {ns}.zb.wf.perk matches {i} run {orb_model_cmd(ns, pid)}"
		for i, pid in enumerate(PERK_IDS)
	)
	write_versioned_function("zombies/wunderfizz/land", f"""
# Roam pull: the machine is about to move — show the bear, refund the buyer, no perk
execute if score @s {ns}.zb.wf.willmove matches 1 run return run function {ns}:v{version}/zombies/wunderfizz/land_bear

{land_dispatch}
particle minecraft:totem_of_undying ~ ~ ~ 0.3 0.4 0.3 0.2 10 force @a[distance=..48]
particle minecraft:electric_spark ~ ~ ~ 0.4 0.5 0.4 0.15 10 force @a[distance=..48]
playsound minecraft:block.beacon.deactivate ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.8 1.4
playsound minecraft:entity.lightning_bolt.impact ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.5 1.7
{ZombiesFeedback.zb_sound('announce')}
scoreboard players operation #wf_b {ns}.data = @s {ns}.zb.wf.buyer
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.zb.wf_pid = #wf_b {ns}.data run tellraw @s [{MGS_TAG},{{"text":"Perk ready! ","color":"gold"}},{{"text":"Right-click Der Wunderfizz to collect!","color":"green","bold":true}}]
""")

