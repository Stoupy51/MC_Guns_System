""" The game tick, the compass pointing at the nearest enemy and the victory check. """
# Imports
from stewbeet import Mem, write_tick_file, write_versioned_function

from ...core.respawn_countdown import respawn_countdown_tick_lines
from ...core.weapon_drop import WeaponDrop
from ...helpers.probes import Probe
from ...helpers.text import Text
from ...helpers.titles import TitleTimes
from ...progression import Advancements
from ..xp import MissionsXp


# Functions
def write_missions_tick() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_tick_file(f"""
execute if data storage {ns}:missions game{{state:"active"}} run function {ns}:v{version}/missions/game_tick
execute if data storage {ns}:missions game{{state:"preparing"}} run function {ns}:v{version}/missions/prep_tick
""")

	write_versioned_function("missions/game_tick", f"""
{respawn_countdown_tick_lines(ns, "mi", f"{ns}:v{version}/missions/actual_respawn")}

scoreboard players operation #mi_timer {ns}.data += #tick_delta {ns}.data

# Bounds and OOB for enemies, when the map has a boundary.
execute if score #mi_has_boundary {ns}.data matches 1 as @e[tag={ns}.mission_enemy] at @s run function {ns}:v{version}/shared/check_bounds
execute if score #mi_has_boundary {ns}.data matches 1 as @e[type=player,scores={{{ns}.mi.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s run function {ns}:v{version}/shared/check_bounds
execute as @e[type=player,scores={{{ns}.mi.in_game=1}},gamemode=!creative,gamemode=!spectator] at @s if entity @e[tag={ns}.oob_point,distance=..5] run damage @s 10000 out_of_world

# Enemies drop their weapon at the corpse; drops live for 30 s.
function {ns}:v{version}/missions/death_watch_tick
{WeaponDrop.weapon_drop_tick_lines(ns)}

# Kills = total enemies - alive enemies.
execute store result score #alive {ns}.data if entity @e[tag={ns}.mission_enemy]
scoreboard players operation #mi_kills {ns}.data = #mi_total_enemies {ns}.data
scoreboard players operation #mi_kills {ns}.data -= #alive {ns}.data

# Every 10 ticks: each update is an item write and a macro parse per player, and a lodestone compass does not need 20 Hz.
scoreboard players operation #mi_compass_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #mi_compass_phase {ns}.data %= #10 {ns}.data
execute if score #alive {ns}.data matches 1.. if score #mi_compass_phase {ns}.data matches 0 as @a[scores={{{ns}.mi.in_game=1}}] at @s run function {ns}:v{version}/missions/update_compass

# Around one in-game player (@r would pay a random sort every tick).
execute at @a[scores={{{ns}.mi.in_game=1}},limit=1] run kill @e[type=experience_orb,distance=..200]

function {ns}:v{version}/shared/maps/call_script_at_base {{script:"tick"}}

# Reuses #alive from above (a kill from the map tick script is caught a tick later); at least one enemy must have spawned,
# so a broken spawn never ends the game at once.
execute if score #mi_total_enemies {ns}.data matches 1.. if score #alive {ns}.data matches 0 run return run function {ns}:v{version}/missions/victory
""")

	## Run as the player, at them; the caller guarantees #alive >= 1.
	target: str = f"@n[tag={ns}.mission_enemy]"
	write_versioned_function("missions/update_compass", f"""
# Only players carrying the mission compass.
execute unless items entity @s hotbar.3 minecraft:compass run return fail

# One sorted scan; a marker carries the position out instead of serializing the mob.
{Probe.pos(target)}
execute store result storage {ns}:temp _compass.x int 1 run data get storage {ns}:temp _probe_pos[0]
execute store result storage {ns}:temp _compass.y int 1 run data get storage {ns}:temp _probe_pos[1]
execute store result storage {ns}:temp _compass.z int 1 run data get storage {ns}:temp _probe_pos[2]

function {ns}:v{version}/missions/set_compass_target with storage {ns}:temp _compass
""")

	write_versioned_function("missions/set_compass_target", f"""
$item replace entity @s hotbar.3 with compass[lodestone_tracker={{target:{{pos:[I;$(x),$(y),$(z)],dimension:"minecraft:overworld"}},tracked:false}},custom_data={{{ns}:{{compass:true}}}}]
""")

	write_versioned_function("missions/victory", f"""
# Mission kills from the totalKillCount delta.
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mi.kills = @s {ns}.mi.kill_total
execute as @a[scores={{{ns}.mi.in_game=1}}] run scoreboard players operation @s {ns}.mi.kills -= @s {ns}.mi.kill_base

# Missions have no XP award to ride, so the challenge counters are fed here, where mi.kills is final.
{Advancements.mission_victory_lines()}

scoreboard players operation #mi_seconds {ns}.data = #mi_timer {ns}.data
scoreboard players operation #mi_seconds {ns}.data /= #20 {ns}.data

scoreboard players operation #mi_minutes {ns}.data = #mi_seconds {ns}.data
scoreboard players operation #mi_minutes {ns}.data /= #60 {ns}.data
scoreboard players operation #mi_rem_sec {ns}.data = #mi_seconds {ns}.data
scoreboard players operation #mi_rem_sec {ns}.data %= #60 {ns}.data

{TitleTimes.BANNER.cmd(f'@a[scores={{{ns}.mi.in_game=1}}]')}
title @a[scores={{{ns}.mi.in_game=1}}] title {{"text":"MISSION COMPLETE","color":"gold","bold":true}}
title @a[scores={{{ns}.mi.in_game=1}}] subtitle {{"text":"All enemies eliminated!","color":"green"}}

tellraw @a ["","\\n",{{"text":"MISSION COMPLETE","color":"gold","bold":true}}]
tellraw @a ["","  ","⏱ ",{{"text":"Time: ","color":"gray"}},{{"score":{{"name":"#mi_minutes","objective":"{ns}.data"}},"color":"yellow"}},"m ",{{"score":{{"name":"#mi_rem_sec","objective":"{ns}.data"}},"color":"yellow"}},"s"]
tellraw @a ["","  ","💀 ",{{"text":"Enemies killed: ","color":"gray"}},{{"score":{{"name":"#mi_total_enemies","objective":"{ns}.data"}},"color":"red"}}]

# Each line carries the completion XP.
execute as @a[scores={{{ns}.mi.in_game=1}}] run tellraw @a ["","  ","🎖 ",{Text.player(ns, "@s", color="yellow")}," | Kills: ",{{"score":{{"name":"@s","objective":"{ns}.mi.kills"}},"color":"green"}}," | Deaths: ",{{"score":{{"name":"@s","objective":"{ns}.mi.deaths"}},"color":"red"}},{MissionsXp.victory_suffix()}]
{MissionsXp.victory_lines()}

tellraw @a ""

function {ns}:v{version}/missions/stop
""")

