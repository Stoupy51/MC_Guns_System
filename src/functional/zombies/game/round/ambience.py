""" Managed horde groans and the watchdog that rebuilds a frozen round. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_function, write_versioned_function

from ....helpers import MGS_TAG

# Constants
HORDE_MAX_INTERVAL: int = 40
""" Ticks between groans with a single zombie nearby; the interval is this divided by the count. """
HORDE_MIN_INTERVAL: int = 4
""" Floor on that interval, so a huge horde stays a wall of groans rather than a buzz. """


# Functions
def write_ambience() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Managed horde ambience.
	# Round zombies are summoned Silent, so a 50-zombie horde can't stack into a wall of groans.
	# Instead each player hears ONE controlled groan at a time, and both its volume and how often it repeats scale with the zombie count near THEM.
	# The rate is what sells a chase: ten zombies on your heels groan several times a second, an empty room barely at all.
	write_versioned_function("zombies/horde_ambient", f"""
# @s = an in-game player. Count zombies within earshot.
execute store result score #horde_count {ns}.data if entity @e[tag={ns}.zombie_round,distance=..32]

# Nothing nearby: wait a full cycle before paying for another entity scan.
execute if score #horde_count {ns}.data matches ..0 run scoreboard players set @s {ns}.zb.horde_cd {HORDE_MAX_INTERVAL}
execute if score #horde_count {ns}.data matches ..0 run return 0

# Volume (hundredths) = 0.25 + count*0.03, hard-capped at 0.80 (so ~18+ zombies all sound the same).
scoreboard players set #horde_vol {ns}.data 25
scoreboard players operation #horde_tmp {ns}.data = #horde_count {ns}.data
scoreboard players operation #horde_tmp {ns}.data *= #3 {ns}.data
scoreboard players operation #horde_vol {ns}.data += #horde_tmp {ns}.data
execute if score #horde_vol {ns}.data matches 80.. run scoreboard players set #horde_vol {ns}.data 80

# Random pitch 0.70..1.05 for variety so the loop doesn't sound metronomic.
execute store result score #horde_pitch {ns}.data run random value 70..105

# Hand volume/pitch to the macro as doubles (value/100).
execute store result storage {ns}:temp _horde.vol double 0.01 run scoreboard players get #horde_vol {ns}.data
execute store result storage {ns}:temp _horde.pitch double 0.01 run scoreboard players get #horde_pitch {ns}.data

# Play the groan FROM a random nearby zombie's position (positional audio), so the player hears
# the horde coming from the right direction/distance rather than centred on themselves.
execute at @e[tag={ns}.zombie_round,distance=..32,sort=random,limit=1] run function {ns}:v{version}/zombies/horde_ambient_play with storage {ns}:temp _horde

# Schedule this player's next groan: {HORDE_MAX_INTERVAL} ticks divided by the nearby count, so 1 zombie
# groans every {HORDE_MAX_INTERVAL / 20:.1f}s and 10 groan {20 * 10 // HORDE_MAX_INTERVAL} times a second.
# The floor keeps a huge horde from turning into a buzz.
scoreboard players operation #horde_next {ns}.data = #{HORDE_MAX_INTERVAL} {ns}.data
scoreboard players operation #horde_next {ns}.data /= #horde_count {ns}.data
execute if score #horde_next {ns}.data matches ..{HORDE_MIN_INTERVAL} run scoreboard players set #horde_next {ns}.data {HORDE_MIN_INTERVAL}
scoreboard players operation @s {ns}.zb.horde_cd = #horde_next {ns}.data
""")

	# @s = the player; execution position = a nearby zombie, so the sound is directional.
	write_versioned_function("zombies/horde_ambient_play", "$playsound minecraft:entity.zombie.ambient hostile @s ~ ~ ~ $(vol) $(pitch)")

	# Freeze watchdog.
	# A round advances through one handoff chain: spawn -> die -> round_complete -> (5s) -> start_round.
	# Any link can go missing (function that failed to load, schedule dropped on /reload, desynced counter, spawn pass that tagged nothing) and the match then sits at "0 zombies" forever.
	# Rather than enumerating those, watch the property they all share: nothing alive, nothing queued, nothing changing — impossible during real play, where the longest legitimate pause is the 5s handoff.
	write_versioned_function("zombies/watchdog_tick", f"""
# Progress fingerprint: any spawn, kill, or portal strike moves it.
scoreboard players operation #zb_wd_fp {ns}.data = #zb_alive {ns}.data
scoreboard players operation #zb_wd_fp {ns}.data += #zb_to_spawn {ns}.data
scoreboard players operation #zb_wd_fp {ns}.data += #zb_dog_pending {ns}.data

# Anything alive counts as progress on its own: kiting a horde is a normal, arbitrarily long state,
# and unreachable zombies are already handled by the stuck escort/glow system.
scoreboard players set #zb_wd_moved {ns}.data 0
execute if score #zb_alive {ns}.data matches 1.. run scoreboard players set #zb_wd_moved {ns}.data 1
execute unless score #zb_wd_fp {ns}.data = #zb_wd_last {ns}.data run scoreboard players set #zb_wd_moved {ns}.data 1
scoreboard players operation #zb_wd_last {ns}.data = #zb_wd_fp {ns}.data

execute if score #zb_wd_moved {ns}.data matches 1 run scoreboard players set #zb_wd_ticks {ns}.data 0
execute if score #zb_wd_moved {ns}.data matches 0 run scoreboard players add #zb_wd_ticks {ns}.data 1

# 400 ticks = 20s, well past the 5s handoff so a healthy round can't trip it.
execute if score #zb_wd_ticks {ns}.data matches 400.. run function {ns}:zombies/recover
""")

	## Rebuild a frozen round.
	## Also the manual escape hatch (admin button / typed in chat), so a stuck game never needs a restart — version-less so it stays typeable without the pack version.
	write_function(f"{ns}:zombies/recover", f"""
execute unless data storage {ns}:zombies game{{state:"active"}} run return run tellraw @s [{MGS_TAG},{{"text":"No zombies game is active.","color":"red"}}]

scoreboard players set #zb_wd_ticks {ns}.data 0

# Blockers that hold a round open without showing in the sidebar: a desynced dog-portal counter,
# and portals that never struck (their dogs are lost either way).
scoreboard players set #zb_dog_pending {ns}.data 0
kill @e[tag={ns}.dog_portal]

# Drop any handoff still in flight so recovery can't race a schedule landing a tick later
schedule clear {ns}:v{version}/zombies/start_round

tellraw @a [{MGS_TAG},{{"text":"Round was frozen — recovering.","color":"yellow"}}]

# Case A: round_complete ran (it parks #zb_to_spawn at -1) but start_round never landed
execute if score #zb_to_spawn {ns}.data matches ..-1 run return run function {ns}:v{version}/zombies/start_round

# Case B: map empty and nothing queued, but the round never closed — close it
kill @e[tag={ns}.zombie_round]
scoreboard players set #zb_to_spawn {ns}.data 0
function {ns}:v{version}/zombies/round_complete
""")

