""" Black Ops 2 zombie vocals: the four sound channels and the per-player budgets that keep them readable.

Round zombies are summoned Silent, so every sound they make is played from here.
BO2 splits zombie vocals into ambient, attack and sprint (plus crawlers) and picks the set from the zombie's gait.
The files confirm it: sprint clips run 3.0-5.3 s, every other bark 0.4-2.2 s.

Each channel has its own budget per player, so a wall of death groans cannot starve the scream of a sprinter behind you.
Budgets are #total_tick timestamps: no per-tick decrement, and an unset score reads as ready.
"""
# Imports
from stewbeet import Mem, write_versioned_function

# Constants
VOCAL_AMBIENT: str = "zombies/entity/ambient"
""" 6 short groans, the walking/running horde. """
VOCAL_BEHIND: str = "zombies/entity/behind"
""" 6 groans for a zombie right behind the player.
World at War and Black Ops keep these quiet and rare "so that zombies are still likely to surprise the player".
Mapping the downloaded say20-25 here is inferred, not confirmed: they are a contiguous block of 6 that reads as a separate set.
If they are plain ambients, fold them into [[VOCAL_AMBIENT]] and drop the behind channel.
"""
VOCAL_ATTACK: str = "zombies/entity/attack"
""" 16 melee grunts (the downloaded set's hurt* files plus say7-8, all swing sounds). """
VOCAL_SPRINT: str = "zombies/entity/sprint"
""" 7 screams of 3.0-5.3 s for the sprint gait: World at War's `new_zombie_vox/sprint2` set.
The short `sprint` set (0.7-2.5 s) does not read as a sprinter in game.
/playsound plays from a fixed point, so a 5 s scream stays where the zombie was while it crosses the room; that drift is accepted.
"""
VOCAL_DEATH: str = "zombies/entity/death"
""" 11 death groans. """

VOCAL_CRAWLER_AMBIENT: str = "zombies/entity/crawler_ambient"
""" 18 legless groans. Staged for a future crawler enemy; nothing plays it yet. """
VOCAL_CRAWLER_SPRINT: str = "zombies/entity/crawler_sprint"
""" 2 legless screams. Staged alongside [[VOCAL_CRAWLER_AMBIENT]]. """

SPRINT_LOCKOUT: int = 110
""" Ticks a player's sprint channel stays held after a scream, so a sprinter owns the soundscape while
it closes instead of the horde drowning it. Clips run 59-107 ticks, so this holds strictly one scream at
a time even after the longest. """
ATTACK_LOCKOUT: int = 20
""" Ticks between melee grunts for one player. A surrounded player is hit by up to eight zombies, and
eight overlapping grunts is mush; one per second still reads as "something is hitting me". """
DEATH_LOCKOUT: int = 10
""" Ticks between death groans for one player. """

BEHIND_CHANCE: int = 25
""" Percent chance a qualifying behind-zombie actually gets a behind vocal. The behind check is already
situational, so this is what turns "situational" into "startling". """
BEHIND_DISTANCE: int = 3
""" Blocks straight back from the player where the behind-check sphere is centred. """
BEHIND_RADIUS: float = 3.0
""" Radius of that sphere. Together with [[BEHIND_DISTANCE]] this covers roughly 0-6 blocks directly
behind the player and nothing in front, which is the "actually directly behind" the category wants. """
BEHIND_VOLUME: float = 0.6
""" Fixed and quiet: a sound you half-notice.
Below 1.0 is safe here, unlike the horde ambience: 0.6 still reaches 9.6 blocks, past the 6 blocks this channel fires from.
"""

VOCAL_RANGE: int = 32
""" Blocks a vocal carries. Volume 2.0 gives full loudness inside 16 blocks and fades out to this. """
ATTACK_REACH: float = 3.5
""" Blocks searched for the zombie that landed the hit. Melee reach is ~2-3, so this finds the attacker
without picking up a bystander across the room. """

HORDE_MAX_INTERVAL: int = 60
""" Ticks between vocals with a single zombie nearby; the interval is this divided by the count. """
HORDE_MIN_INTERVAL: int = 40
""" Floor on that interval, so the rate stops scaling once the horde is big: at 40 that is one ambient
vocal every 2s per player. Anything faster stops reading as individual zombies and turns into a texture. """

HORDE_VOLUME_BASE: int = 100
""" Volume in hundredths for a single nearby zombie. 1.0 is a deliberate floor: playsound below 1.0
shrinks the audible radius to 16*volume, so anything less meant a zombie picked from the 32-block
radius was often inaudible and the groan simply did not happen. """
HORDE_VOLUME_PER_ZOMBIE: int = 5
""" Added per nearby zombie.
Past 1.0 playsound extends reach rather than loudness, so a big horde is heard from further away.
"""
HORDE_VOLUME_CAP: int = 200
""" 2.0 = audible out to exactly [[VOCAL_RANGE]], the radius the zombie is picked from. """


# Functions
def generate_vocals() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Round zombies are Silent, so each player hears one controlled vocal at a time, scheduled off the zombie count near them.
	# HORDE_MIN_INTERVAL caps the rate: a bigger horde is louder and reaches further, not more frequent.
	write_versioned_function("zombies/horde_ambient", f"""
# Run as an in-game player.
execute store result score #horde_count {ns}.data if entity @e[tag={ns}.zombie_round,distance=..{VOCAL_RANGE}]

# Nothing nearby: wait a full cycle before the next entity scan.
execute if score #horde_count {ns}.data matches ..0 run scoreboard players set @s {ns}.zb.horde_cd {HORDE_MAX_INTERVAL}
execute if score #horde_count {ns}.data matches ..0 run return 0

# Volume (hundredths) 1.00 + count x 0.05, capped at 2.00 (20+ zombies reach the full 32 blocks).
scoreboard players set #horde_vol {ns}.data {HORDE_VOLUME_BASE}
scoreboard players operation #horde_tmp {ns}.data = #horde_count {ns}.data
scoreboard players operation #horde_tmp {ns}.data *= #{HORDE_VOLUME_PER_ZOMBIE} {ns}.data
scoreboard players operation #horde_vol {ns}.data += #horde_tmp {ns}.data
execute if score #horde_vol {ns}.data matches {HORDE_VOLUME_CAP}.. run scoreboard players set #horde_vol {ns}.data {HORDE_VOLUME_CAP}
execute store result storage {ns}:temp _horde.vol double 0.01 run scoreboard players get #horde_vol {ns}.data

# Sprint channel first, like BO2: the sprinter closing in, one scream at a time (SPRINT_LOCKOUT), never pitch-shifted.
scoreboard players set #horde_sprint {ns}.data 0
execute unless score @s {ns}.zb.vox_sprint > #total_tick {ns}.data store success score #horde_sprint {ns}.data at @n[tag={ns}.zb_sprint,tag={ns}.zombie_round,distance=..{VOCAL_RANGE},sort=random] run function {ns}:v{version}/zombies/vocals/horde_sprint with storage {ns}:temp _horde
execute if score #horde_sprint {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.vox_sprint = #total_tick {ns}.data
execute if score #horde_sprint {ns}.data matches 1 run scoreboard players add @s {ns}.zb.vox_sprint {SPRINT_LOCKOUT}

# Behind channel: `rotated ~180 0` puts ^ ^ ^{BEHIND_DISTANCE} straight behind the player at their height. Rolled, so it is rare.
execute if score #horde_sprint {ns}.data matches 0 store result score #horde_behind_roll {ns}.data run random value 1..100
scoreboard players set #horde_behind {ns}.data 0
execute if score #horde_sprint {ns}.data matches 0 if score #horde_behind_roll {ns}.data matches ..{BEHIND_CHANCE} store success score #horde_behind {ns}.data rotated ~180 0 positioned ^ ^ ^{BEHIND_DISTANCE} at @n[tag={ns}.zombie_round,distance=..{BEHIND_RADIUS}] run function {ns}:v{version}/zombies/vocals/horde_behind

# Otherwise a short groan from a random nearby zombie, so it comes from the right direction;
# random pitch 0.70 to 1.05 keeps 6 clips from sounding repetitive.
execute if score #horde_sprint {ns}.data matches 0 if score #horde_behind {ns}.data matches 0 store result score #horde_pitch {ns}.data run random value 70..105
execute if score #horde_sprint {ns}.data matches 0 if score #horde_behind {ns}.data matches 0 store result storage {ns}:temp _horde.pitch double 0.01 run scoreboard players get #horde_pitch {ns}.data
execute if score #horde_sprint {ns}.data matches 0 if score #horde_behind {ns}.data matches 0 at @e[tag={ns}.zombie_round,distance=..{VOCAL_RANGE},sort=random,limit=1] run function {ns}:v{version}/zombies/vocals/horde_ambient with storage {ns}:temp _horde

# Next vocal in {HORDE_MAX_INTERVAL} ticks / nearby count: a lone zombie every {HORDE_MAX_INTERVAL / 20:.1f} s,
# {-(-HORDE_MAX_INTERVAL // HORDE_MIN_INTERVAL)}+ zombies at the {HORDE_MIN_INTERVAL / 20:.1f} s floor.
scoreboard players operation #horde_next {ns}.data = #{HORDE_MAX_INTERVAL} {ns}.data
scoreboard players operation #horde_next {ns}.data /= #horde_count {ns}.data
execute if score #horde_next {ns}.data matches ..{HORDE_MIN_INTERVAL} run scoreboard players set #horde_next {ns}.data {HORDE_MIN_INTERVAL}
scoreboard players operation @s {ns}.zb.horde_cd = #horde_next {ns}.data
""")

	# Run as the player, at a nearby zombie, so the sound is directional.
	write_versioned_function("zombies/vocals/horde_ambient", f"$playsound {ns}:{VOCAL_AMBIENT} hostile @s ~ ~ ~ $(vol) $(pitch)")

	## Run as the player, at a zombie right behind them: fixed quiet volume, no pitch shift.
	## The caller's `store success` reads `return 1`.
	write_versioned_function("zombies/vocals/horde_behind", f"""
playsound {ns}:{VOCAL_BEHIND} hostile @s ~ ~ ~ {BEHIND_VOLUME} 1.0
return 1
""")

	## Run as the player, at a nearby sprinting zombie. The caller's `store success` reads `return 1`,
	## so the lockout is only taken when a scream started.
	write_versioned_function("zombies/vocals/horde_sprint", f"""
$playsound {ns}:{VOCAL_SPRINT} hostile @s ~ ~ ~ $(vol) 1.0
return 1
""")

	## Melee grunt, run as the player just hit, played from the attacker so a hit from behind sounds like one. Not for dogs.
	write_versioned_function("zombies/vocals/attack", f"""
scoreboard players operation @s {ns}.zb.vox_attack = #total_tick {ns}.data
scoreboard players add @s {ns}.zb.vox_attack {ATTACK_LOCKOUT}
execute at @n[tag={ns}.zombie_round,tag=!{ns}.zb_dog,distance=..{ATTACK_REACH}] run playsound {ns}:{VOCAL_ATTACK} hostile @s ~ ~ ~ 1.0 1.0
""")

	## Death groan, run as the zombie on the tick its Health reached 0. Budgeted per player, so a Nuke thins out.
	write_versioned_function("zombies/vocals/death", f"""
# Health stays 0 for the whole death animation, so this tag makes the groan fire once.
tag @s add {ns}.zb_dying

execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..{VOCAL_RANGE}] unless score @s {ns}.zb.vox_death > #total_tick {ns}.data run function {ns}:v{version}/zombies/vocals/death_for
""")

	## Run as a listening player, at the dying zombie.
	write_versioned_function("zombies/vocals/death_for", f"""
scoreboard players operation @s {ns}.zb.vox_death = #total_tick {ns}.data
scoreboard players add @s {ns}.zb.vox_death {DEATH_LOCKOUT}
playsound {ns}:{VOCAL_DEATH} hostile @s ~ ~ ~ 2.0 1.0
""")

