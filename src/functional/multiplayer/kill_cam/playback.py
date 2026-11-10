""" Playback: the viewers on a camera at the final killer's eyes, one mannequin per other player, the deaths, the shots and the cleanup.

Each sample writes its position and rotation onto the probe, and its entity is teleported to the probe.
"""
# Imports
from stewbeet import JsonDict, Mem, Predicate, set_json_encoder, write_load_file, write_versioned_function

from ...helpers.text import Text
from ...helpers.titles import TitleTimes
from ...shaders.flash import FLASH_TINT, OBSERVER_MUZZLE
from .shared import EYE_HEIGHT, INTRO_TICKS, POST_ROLL, PRE_ROLL, PROBE_UUID, SNEAK_EYE_HEIGHT


# Functions
def write_kill_cam_playback() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	kc: str = f"{ns}:v{version}/multiplayer/kill_cam"
	camera: str = f"@n[type=minecraft:item_display,tag={ns}.kc_camera]"
	viewers: str = f"@a[tag={ns}.kc_viewer]"

	## The player id a puppet or home marker stands for, matched against #kc_sid.
	write_load_file(f"scoreboard objectives add {ns}.mp.kc_id dummy")
	sid_ref: JsonDict = {"type": "minecraft:score", "target": {"type": "minecraft:fixed", "name": "#kc_sid"}, "score": f"{ns}.data"}
	Mem.ctx.data[ns].predicates[f"v{version}/multiplayer/kill_cam/id_match"] = set_json_encoder(Predicate({
		"type": "minecraft:entity_scores",
		"entity": "this",
		"scores": {f"{ns}.mp.kc_id": {"min": sid_ref, "max": sid_ref}},
	}), max_level=-1)
	id_match: str = f"predicate={ns}:v{version}/multiplayer/kill_cam/id_match"
	puppet: str = f"@e[type=minecraft:mannequin,tag={ns}.kc_puppet,{id_match}]"

	## Run by multiplayer/end with the state already "ended": returns 1 once the replay is set up, fails when the match has none.
	write_versioned_function("multiplayer/kill_cam/start", f"""
# A Search and Destroy wipe ends on its last death, logged on the deciding tick.
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} store result score #kc_t {ns}.data run data get storage {ns}:kill_cam deaths[-1].t
execute if data storage {ns}:multiplayer game{{gamemode:"snd"}} if score #kc_t {ns}.data = #mp_end_tick {ns}.data run scoreboard players set #kc_final {ns}.data 2
execute unless score #kc_final {ns}.data matches 2 run return fail
execute unless data storage {ns}:kill_cam deaths[-1].killer run return fail
execute unless data storage {ns}:kill_cam frames[0] run return fail
scoreboard players set #kc_window {ns}.data 0

function {kc}/resolve_chain

# From PRE_ROLL before the first kill, and never on a frame without the killer: the camera is their eyes.
scoreboard players operation #kc_cut {ns}.data = #kc_chain_start {ns}.data
scoreboard players remove #kc_cut {ns}.data {PRE_ROLL}
function {kc}/drop_early_frames
execute store result storage {ns}:temp _kc.killer int 1 run scoreboard players get #kc_killer {ns}.data
function {kc}/drop_frames_without_killer with storage {ns}:temp _kc
execute unless data storage {ns}:kill_cam frames[0] run return fail
execute store result score #kc_oldest {ns}.data run data get storage {ns}:kill_cam frames[0].t
execute if data storage {ns}:kill_cam deaths[0] run function {kc}/trim_deaths

tag @a[scores={{{ns}.mp.in_game=1}}] add {ns}.kc_viewer
execute as {viewers} if score @s bs.id = #kc_killer {ns}.data run tag @s add {ns}.kc_killer
execute unless entity {PROBE_UUID} at @r[tag={ns}.kc_viewer] run function {kc}/summon_probe
function {kc}/place_camera with storage {ns}:temp _kc
execute as {viewers} at @s run function {kc}/add_viewer

{TitleTimes.KILL_CAM.cmd(viewers)}
title {viewers} title {{"text":"KILLCAM","bold":true}}
title {viewers} subtitle [{Text.player(ns, f"@a[tag={ns}.kc_killer]")},{{"text":" x","color":"gold"}},{{"score":{{"name":"#kc_chain_len","objective":"{ns}.data"}},"color":"gold"}}]

scoreboard players set #kc_hold {ns}.data {INTRO_TICKS}
scoreboard players operation #kc_end_t {ns}.data = #kc_final_t {ns}.data
scoreboard players add #kc_end_t {ns}.data {POST_ROLL}
return 1
""")

	write_versioned_function("multiplayer/kill_cam/drop_early_frames", f"""
execute store result score #kc_t {ns}.data run data get storage {ns}:kill_cam frames[0].t
execute if score #kc_t {ns}.data >= #kc_cut {ns}.data run return 0
data remove storage {ns}:kill_cam frames[0]
execute if data storage {ns}:kill_cam frames[0] run function {kc}/drop_early_frames
""")

	write_versioned_function("multiplayer/kill_cam/drop_frames_without_killer", f"""
$execute if data storage {ns}:kill_cam frames[0].s[{{id:$(killer)}}] run return 0
data remove storage {ns}:kill_cam frames[0]
execute if data storage {ns}:kill_cam frames[0] run function {kc}/drop_frames_without_killer with storage {ns}:temp _kc
""")

	## The camera starts at the killer's first sample, where the intro holds.
	write_versioned_function("multiplayer/kill_cam/place_camera", f"""
$data modify entity {PROBE_UUID} Pos set from storage {ns}:kill_cam frames[0].s[{{id:$(killer)}}].p
$data modify entity {PROBE_UUID} Rotation set from storage {ns}:kill_cam frames[0].s[{{id:$(killer)}}].r
execute at {PROBE_UUID} run summon minecraft:item_display ~ ~{EYE_HEIGHT} ~ {{teleport_duration:2,Tags:["{ns}.kc_camera","{ns}.kill_cam","{ns}.multiplayer_entity"]}}
execute at {PROBE_UUID} run tp {camera} ~ ~{EYE_HEIGHT} ~ ~ ~
""")

	## Run as a viewer, at them: a home marker keeps where they stood for kill_cam/cleanup.
	write_versioned_function("multiplayer/kill_cam/add_viewer", f"""
scoreboard players operation #kc_sid {ns}.data = @s bs.id
execute summon minecraft:marker run function {kc}/home_marker
gamemode spectator @s
spectate {camera} @s
""")
	write_versioned_function("multiplayer/kill_cam/home_marker", f"""
tag @s add {ns}.kc_home
tag @s add {ns}.kill_cam
tag @s add {ns}.multiplayer_entity
scoreboard players operation @s {ns}.mp.kc_id = #kc_sid {ns}.data
tp @s ~ ~ ~ ~ ~
""")

	## Every tick in the "ended" state, from the tick file.
	write_versioned_function("multiplayer/kill_cam/tick", f"""
# Sneaking stops spectating, so every viewer is put back on the camera; setCamera ignores the camera a viewer already has.
execute as {viewers} run spectate {camera} @s
execute if score #kc_hold {ns}.data matches 1.. run return run scoreboard players remove #kc_hold {ns}.data 1
execute unless data storage {ns}:kill_cam frames[0] run return run function {kc}/post_roll

data modify storage {ns}:kill_cam frame set from storage {ns}:kill_cam frames[0]
data remove storage {ns}:kill_cam frames[0]
execute store result score #kc_now {ns}.data run data get storage {ns}:kill_cam frame.t

execute unless entity {PROBE_UUID} at {camera} run function {kc}/summon_probe
execute if data storage {ns}:kill_cam frame.s[0] run function {kc}/play_sample

# After the samples, as a death outside the function tick (a command, an advancement reward) comes after its tick's frame.
# Before the vanish, so the victim falls on screen.
execute if data storage {ns}:kill_cam deaths[0] run function {kc}/play_deaths
execute as @e[type=minecraft:mannequin,tag={ns}.kc_puppet,tag=!{ns}.kc_seen] at @s run function {kc}/vanish
tag @e[type=minecraft:mannequin,tag={ns}.kc_seen] remove {ns}.kc_seen
execute if data storage {ns}:kill_cam frame.shots[0] run function {kc}/play_shot
""")

	## Past the last frame the scene holds until POST_ROLL after the final kill.
	write_versioned_function("multiplayer/kill_cam/post_roll", f"""
scoreboard players add #kc_now {ns}.data 1
execute if score #kc_now {ns}.data >= #kc_end_t {ns}.data run function {ns}:v{version}/multiplayer/stop
""")

	write_versioned_function("multiplayer/kill_cam/play_deaths", f"""
execute store result score #kc_t {ns}.data run data get storage {ns}:kill_cam deaths[0].t
execute if score #kc_t {ns}.data > #kc_now {ns}.data run return 0
execute store result score #kc_sid {ns}.data run data get storage {ns}:kill_cam deaths[0].victim
kill {puppet}
data remove storage {ns}:kill_cam deaths[0]
execute if data storage {ns}:kill_cam deaths[0] run function {kc}/play_deaths
""")

	write_versioned_function("multiplayer/kill_cam/play_sample", f"""
execute store result score #kc_sid {ns}.data run data get storage {ns}:kill_cam frame.s[0].id
data modify entity {PROBE_UUID} Pos set from storage {ns}:kill_cam frame.s[0].p
data modify entity {PROBE_UUID} Rotation set from storage {ns}:kill_cam frame.s[0].r
execute store success score #kc_sneak {ns}.data if data storage {ns}:kill_cam frame.s[0].sneak

execute if score #kc_sid {ns}.data = #kc_killer {ns}.data if score #kc_sneak {ns}.data matches 0 at {PROBE_UUID} run tp {camera} ~ ~{EYE_HEIGHT} ~ ~ ~
execute if score #kc_sid {ns}.data = #kc_killer {ns}.data if score #kc_sneak {ns}.data matches 1 at {PROBE_UUID} run tp {camera} ~ ~{SNEAK_EYE_HEIGHT} ~ ~ ~
execute unless score #kc_sid {ns}.data = #kc_killer {ns}.data run function {kc}/drive_puppet

data remove storage {ns}:kill_cam frame.s[0]
execute if data storage {ns}:kill_cam frame.s[0] run function {kc}/play_sample
""")

	## A player whose samples resume after a death gets a new puppet: the dead one cannot be selected any more.
	write_versioned_function("multiplayer/kill_cam/drive_puppet", f"""
execute as {puppet} at {PROBE_UUID} run return run function {kc}/move_puppet
execute at {PROBE_UUID} summon minecraft:mannequin run function {kc}/init_puppet
""")

	## Run as a new mannequin, at the probe. A player who left gives a plain one.
	write_versioned_function("multiplayer/kill_cam/init_puppet", f"""
data merge entity @s {{NoGravity:true,immovable:true,hide_description:true,Invulnerable:true,Tags:["{ns}.kc_puppet","{ns}.kill_cam","{ns}.multiplayer_entity","{ns}.kc_new"]}}
scoreboard players operation @s {ns}.mp.kc_id = #kc_sid {ns}.data
execute as @a if score @s bs.id = #kc_sid {ns}.data run function {kc}/dress_puppet
tag @s remove {ns}.kc_new
function {kc}/move_puppet
""")

	## Run as the player, at their new puppet: armor, skin and held item, as multiplayer/death_animation dresses its copy.
	new_puppet: str = f"@n[type=minecraft:mannequin,tag={ns}.kc_new]"
	write_versioned_function("multiplayer/kill_cam/dress_puppet", f"""
data modify entity {new_puppet} equipment set from entity @s equipment
loot replace entity {new_puppet} weapon.mainhand loot {ns}:get_username
data modify entity {new_puppet} profile set from entity {new_puppet} equipment.mainhand.components."minecraft:profile"
item replace entity {new_puppet} weapon.mainhand from entity @s weapon.mainhand
""")

	## Run as a puppet, at the probe.
	write_versioned_function("multiplayer/kill_cam/move_puppet", f"""
tag @s add {ns}.kc_seen
tp @s ~ ~ ~ ~ ~
execute if score #kc_sneak {ns}.data matches 1 unless entity @s[tag={ns}.kc_crouch] run data modify entity @s pose set value "crouching"
execute if score #kc_sneak {ns}.data matches 0 if entity @s[tag={ns}.kc_crouch] run data modify entity @s pose set value "standing"
execute if score #kc_sneak {ns}.data matches 1 run tag @s add {ns}.kc_crouch
execute if score #kc_sneak {ns}.data matches 0 run tag @s remove {ns}.kc_crouch
""")

	## A puppet whose player has no sample and no death left the match: it dies out of sight.
	write_versioned_function("multiplayer/kill_cam/vanish", """
tp @s ~ -10000 ~
kill @s
""")

	write_versioned_function("multiplayer/kill_cam/play_shot", f"""
execute store result score #kc_sid {ns}.data run data get storage {ns}:kill_cam frame.shots[0].id
execute if score #kc_sid {ns}.data = #kc_killer {ns}.data at {camera} run particle flash{{color:{[*FLASH_TINT, 1.0]}}} {OBSERVER_MUZZLE} 0 0 0 0 1 force {viewers}
execute if data storage {ns}:kill_cam frame.shots[0].snd if score #kc_sid {ns}.data = #kc_killer {ns}.data at {camera} run function {kc}/shot_sound with storage {ns}:kill_cam frame.shots[0]
execute if data storage {ns}:kill_cam frame.shots[0].snd unless score #kc_sid {ns}.data = #kc_killer {ns}.data at {puppet} anchored eyes positioned ^ ^ ^ run function {kc}/shot_sound with storage {ns}:kill_cam frame.shots[0]
data remove storage {ns}:kill_cam frame.shots[0]
execute if data storage {ns}:kill_cam frame.shots[0] run function {kc}/play_shot
""")
	write_versioned_function("multiplayer/kill_cam/shot_sound", f"""
$playsound {ns}:$(snd) player {viewers} ~ ~ ~ 0.35 1 0.10
""")

	## Run first by multiplayer/stop, so a replay cut short ends like a finished one.
	write_versioned_function("multiplayer/kill_cam/cleanup", f"""
execute as {viewers} run function {kc}/return_home
tag @a remove {ns}.kc_viewer
tag @a remove {ns}.kc_killer
execute as @e[type=minecraft:mannequin,tag={ns}.kc_puppet] at @s run function {kc}/vanish
kill @e[tag={ns}.kill_cam]
function {kc}/close
scoreboard players set #kc_final {ns}.data 0
data remove storage {ns}:kill_cam frame
""")

	## The teleport also stops the spectating.
	write_versioned_function("multiplayer/kill_cam/return_home", f"""
scoreboard players operation #kc_sid {ns}.data = @s bs.id
execute at @e[type=minecraft:marker,tag={ns}.kc_home,{id_match}] run tp @s ~ ~ ~ ~ ~
""")

