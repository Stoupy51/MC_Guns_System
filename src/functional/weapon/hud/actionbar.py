""" Actionbar HUD: fire-mode indicator and ammo counter. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....config.stats.colors import END_HEX, START_HEX
from ....config.stats.keys import CAPACITY, FIRE_MODE, REMAINING_BULLETS


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("actionbar/show", f"""
# Everything on the bar only changes while the weapon is in use, so idle refreshes every 10 ticks instead of every tick
# (~50 commands and a macro parse); ab_force (fire-mode toggle) forces a refresh the use detection cannot see.
scoreboard players set #ab_active {ns}.data 0
execute if score @s {ns}.cooldown > #total_tick {ns}.data run scoreboard players set #ab_active {ns}.data 1
execute if score @s {ns}.pending_clicks matches 0.. run scoreboard players set #ab_active {ns}.data 1
execute if score @s {ns}.previous_dps matches 1.. run scoreboard players set #ab_active {ns}.data 1
execute if score @s {ns}.ab_force matches 1 run scoreboard players set #ab_active {ns}.data 1
scoreboard players operation #ab_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #ab_phase {ns}.data %= #10 {ns}.data
execute if score #ab_active {ns}.data matches 0 unless score #ab_phase {ns}.data matches 0 run return 0
scoreboard players set @s {ns}.ab_force 0

function {ns}:v{version}/actionbar/build_fire_mode_indicator

function {ns}:v{version}/actionbar/add_cooldown_indicator

execute store result score #capacity {ns}.data run data get storage {ns}:gun all.stats.{CAPACITY}
execute store result score #remaining {ns}.data run scoreboard players get @s {ns}.{REMAINING_BULLETS}

data modify storage {ns}:temp actionbar.list append value " "

# Above 15 bullets, numbers; otherwise icons.
execute if score #capacity {ns}.data matches 16.. run function {ns}:v{version}/actionbar/add_numeric_ammo
execute if score #capacity {ns}.data matches ..15 run function {ns}:v{version}/actionbar/add_icon_ammo

function {ns}:v{version}/actionbar/add_dps

function {ns}:v{version}/actionbar/display with storage {ns}:temp actionbar
""")

	# [S | B | A]
	write_versioned_function("actionbar/build_fire_mode_indicator", f"""
data modify storage {ns}:temp actionbar set value {{list:[]}}

data modify storage {ns}:temp actionbar.list append value {{"text":"","color":"#{START_HEX}"}}
data modify storage {ns}:temp actionbar.list append value {{"text":"[ ","color":"#{END_HEX}"}}

execute store result score #has_auto {ns}.data if data storage {ns}:gun all.stats.can_auto
execute store result score #has_burst {ns}.data if data storage {ns}:gun all.stats.can_burst

# auto and burst: [S | B | A]; auto only: [S | A]; burst only: [S | B]; neither: [S].

execute if data storage {ns}:gun all.stats{{{FIRE_MODE}:"semi"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"S","color":"yellow","bold":true}}
execute unless data storage {ns}:gun all.stats{{{FIRE_MODE}:"semi"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"S"}}

execute if score #has_burst {ns}.data matches 1 run data modify storage {ns}:temp actionbar.list append value {{"text":" | "}}

execute if score #has_burst {ns}.data matches 1 if data storage {ns}:gun all.stats{{{FIRE_MODE}:"burst"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"B","color":"yellow"}}
execute if score #has_burst {ns}.data matches 1 unless data storage {ns}:gun all.stats{{{FIRE_MODE}:"burst"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"B"}}

execute if score #has_auto {ns}.data matches 1 run data modify storage {ns}:temp actionbar.list append value {{"text":" | "}}

execute if score #has_auto {ns}.data matches 1 if data storage {ns}:gun all.stats{{{FIRE_MODE}:"auto"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"A","color":"yellow","bold":true}}
execute if score #has_auto {ns}.data matches 1 unless data storage {ns}:gun all.stats{{{FIRE_MODE}:"auto"}} run data modify storage {ns}:temp actionbar.list append value {{"text":"A"}}

data modify storage {ns}:temp actionbar.list append value {{"text":" ] ","color":"#{END_HEX}"}}
""")

	# Above 15 bullets: "remaining | reserve".
	write_versioned_function("actionbar/add_numeric_ammo", f"""
data modify storage {ns}:temp actionbar.list append value {{"score":{{"name":"#remaining","objective":"{ns}.data"}}}}
data modify storage {ns}:temp actionbar.list append value {{"text":"x "}}
data modify storage {ns}:temp actionbar.list append value {{"text":"A","font":"{ns}:icons","shadow_color":[0,0,0,0],"color":"white"}}
data modify storage {ns}:temp actionbar.list append value {{"text":" | ","color":"#{END_HEX}"}}
execute store result score #reserve {ns}.data run scoreboard players get @s {ns}.reserve_ammo
data modify storage {ns}:temp actionbar.list append value {{"score":{{"name":"#reserve","objective":"{ns}.data"}}}}
data modify storage {ns}:temp actionbar.list append value {{"text":"x "}}
data modify storage {ns}:temp actionbar.list append value {{"text":"A","font":"{ns}:icons","shadow_color":[0,0,0,0],"color":"gray"}}
""")

	# Up to 15 bullets: icons, then the reserve.
	write_versioned_function("actionbar/add_icon_ammo", f"""
scoreboard players set #i {ns}.data 0
execute if score #i {ns}.data < #capacity {ns}.data run function {ns}:v{version}/actionbar/build_icon_loop

data modify storage {ns}:temp actionbar.list append value {{"text":" | ","color":"#{END_HEX}"}}
execute store result score #reserve {ns}.data run scoreboard players get @s {ns}.reserve_ammo
data modify storage {ns}:temp actionbar.list append value {{"score":{{"name":"#reserve","objective":"{ns}.data"}}}}
data modify storage {ns}:temp actionbar.list append value {{"text":"x ","color":"gray"}}
data modify storage {ns}:temp actionbar.list append value {{"text":"A","font":"{ns}:icons","shadow_color":[0,0,0,0],"color":"gray"}}
""")

	write_versioned_function("actionbar/build_icon_loop", f"""
# Full by default.
data modify storage {ns}:temp actionbar.list append value {{"text":"A","font":"{ns}:icons","shadow_color":[0,0,0,0]}}

# Empty bullets are outlines.
execute if score #i {ns}.data >= #remaining {ns}.data run data modify storage {ns}:temp actionbar.list[-1] set value {{"text":"B","font":"{ns}:icons","color":"gray","shadow_color":[0,0,0,0]}}

scoreboard players add #i {ns}.data 1

execute if score #i {ns}.data < #capacity {ns}.data run function {ns}:v{version}/actionbar/build_icon_loop
""")

	# Green ● when ready to fire, dark red ● on cooldown.
	write_versioned_function("actionbar/add_cooldown_indicator", f"""
execute if score @s {ns}.cooldown <= #total_tick {ns}.data run data modify storage {ns}:temp actionbar.list append value {{"text":" ● ","color":"green"}}
execute if score @s {ns}.cooldown > #total_tick {ns}.data run data modify storage {ns}:temp actionbar.list append value {{"text":" ● ","color":"dark_red"}}
""")

	# Through Smithed Actionbar, with persistent priority.
	write_versioned_function("actionbar/display", """
$data modify storage smithed.actionbar:input message set value {json:$(list),priority:'persistent',freeze:1}
function #smithed.actionbar:message
""")

	# previous_dps: damage x10 per second, snapshotted every 20 ticks.
	write_versioned_function("actionbar/add_dps", f"""
execute store result score #dps_raw {ns}.data run scoreboard players get @s {ns}.previous_dps

scoreboard players operation #dps_int {ns}.data = #dps_raw {ns}.data
scoreboard players operation #dps_int {ns}.data /= #10 {ns}.data
scoreboard players operation #dps_dec {ns}.data = #dps_raw {ns}.data
scoreboard players operation #dps_dec {ns}.data %= #10 {ns}.data

data modify storage {ns}:temp actionbar.list append value "    "
data modify storage {ns}:temp actionbar.list append value {{"text":"⚡","color":"#{END_HEX}"}}
data modify storage {ns}:temp actionbar.list append value " "
data modify storage {ns}:temp actionbar.list append value {{"score":{{"name":"#dps_int","objective":"{ns}.data"}}}}
data modify storage {ns}:temp actionbar.list append value {{"text":"."}}
data modify storage {ns}:temp actionbar.list append value {{"score":{{"name":"#dps_dec","objective":"{ns}.data"}}}}
data modify storage {ns}:temp actionbar.list append value " "
data modify storage {ns}:temp actionbar.list append value {{"text":"dps","color":"#{END_HEX}"}}
""")

