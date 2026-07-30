""" Black Ops 2 zombie vocals: the four sound channels and the per-player budget that keeps them readable.

Round zombies are summoned Silent, so every sound they make is played by hand from here. BO2 splits its
zombie vocals into ambient / attack / sprint (plus a separate set for crawlers) and picks the set from
the zombie's gait, which is what the sound files themselves confirm: sprint clips run 3.0-4.9s while
every other bark is 0.4-2.2s.

Each channel carries its own per-player budget rather than one shared one, because a shared budget
would let a wall of death groans starve the scream that tells you a sprinter is behind you. Budgets are
timestamps compared against #total_tick, so no per-tick decrement is needed and an unset score reads as
"ready".
"""
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

# Constants
VOCAL_AMBIENT: str = "zombies/entity/ambient"
""" 6 short groans, the walking/running horde. """
VOCAL_BEHIND: str = "zombies/entity/behind"
""" 6 groans reserved for a zombie directly behind the player. World at War / Black Ops treats these as
their own category, deliberately quiet and rare "so that zombies are still likely to surprise the
player", which is why they are barely recognisable from normal play. Mapping the downloaded say20-25 to
this category is INFERRED, not confirmed: they are a contiguous block of 6 that reads as a separate set.
If they turn out to be plain ambients, fold them back into [[VOCAL_AMBIENT]] and drop the behind channel. """
VOCAL_ATTACK: str = "zombies/entity/attack"
""" 16 melee grunts (the downloaded set's hurt* files plus say7-8, all swing sounds). """
VOCAL_SPRINT: str = "zombies/entity/sprint"
""" 7 screams, 3.0-4.9s, the sprint gait. """
VOCAL_DEATH: str = "zombies/entity/death"
""" 11 death groans. """

VOCAL_CRAWLER_AMBIENT: str = "zombies/entity/crawler_ambient"
""" 18 legless groans. Staged for a future crawler enemy; nothing plays it yet. """
VOCAL_CRAWLER_SPRINT: str = "zombies/entity/crawler_sprint"
""" 2 legless screams. Staged alongside [[VOCAL_CRAWLER_AMBIENT]]. """

SPRINT_LOCKOUT: int = 70
""" Ticks a player's sprint channel stays held after a scream, so a sprinter owns the soundscape while
it closes instead of the horde drowning it. Clips run 60-99 ticks, so at 70 the longest ones still
overlap the next scream by up to 29 ticks — raise this to 100 for strictly one at a time. """
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
""" Fixed and deliberately quiet — the point is a sound you half-notice. Safe below 1.0 here, unlike the
horde ambience: 0.6 still reaches 9.6 blocks, well past the ~6 blocks this channel can fire from. """

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
""" Added per nearby zombie. Past 1.0 playsound extends reach rather than loudness, so a big horde is
heard from further out instead of louder — which is the effect worth having anyway. """
HORDE_VOLUME_CAP: int = 200
""" 2.0 = audible out to exactly [[VOCAL_RANGE]], the radius the zombie is picked from. """


# Functions
def generate_vocals() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Managed horde ambience.
	# Round zombies are Silent, so a 50-zombie horde can't stack into a wall of groans on its own.
	# Instead each player hears ONE controlled vocal at a time, scheduled off the zombie count near THEM.
	# Rate is capped at 1/s (HORDE_MIN_INTERVAL), so a chase reads through volume and reach instead: an empty room is a rare distant groan, a horde on your heels is a loud one every second from all around you.
	write_versioned_function("zombies/horde_ambient", f"""
# @s = an in-game player. Count zombies within earshot.
execute store result score #horde_count {ns}.data if entity @e[tag={ns}.zombie_round,distance=..{VOCAL_RANGE}]

# Nothing nearby: wait a full cycle before paying for another entity scan.
execute if score #horde_count {ns}.data matches ..0 run scoreboard players set @s {ns}.zb.horde_cd {HORDE_MAX_INTERVAL}
execute if score #horde_count {ns}.data matches ..0 run return 0

# Volume (hundredths) = 1.00 + count*0.05, capped at 2.00 (20+ zombies all reach the full 32 blocks).
scoreboard players set #horde_vol {ns}.data {HORDE_VOLUME_BASE}
scoreboard players operation #horde_tmp {ns}.data = #horde_count {ns}.data
scoreboard players operation #horde_tmp {ns}.data *= #{HORDE_VOLUME_PER_ZOMBIE} {ns}.data
scoreboard players operation #horde_vol {ns}.data += #horde_tmp {ns}.data
execute if score #horde_vol {ns}.data matches {HORDE_VOLUME_CAP}.. run scoreboard players set #horde_vol {ns}.data {HORDE_VOLUME_CAP}
execute store result storage {ns}:temp _horde.vol double 0.01 run scoreboard players get #horde_vol {ns}.data

# Sprint channel first. BO2 leads with the sprinter that is closing on you rather than a random member
# of the horde, and the channel lockout is what keeps it to one scream at a time (see SPRINT_LOCKOUT).
# The scream is NOT pitch-shifted: bending a 4-second human scream is instantly audible as a gimmick.
scoreboard players set #horde_sprint {ns}.data 0
execute unless score @s {ns}.zb.vox_sprint > #total_tick {ns}.data store success score #horde_sprint {ns}.data at @n[tag={ns}.zb_sprint,tag={ns}.zombie_round,distance=..{VOCAL_RANGE},sort=random] run function {ns}:v{version}/zombies/vocals/horde_sprint with storage {ns}:temp _horde
execute if score #horde_sprint {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.vox_sprint = #total_tick {ns}.data
execute if score #horde_sprint {ns}.data matches 1 run scoreboard players add @s {ns}.zb.vox_sprint {SPRINT_LOCKOUT}

# Behind channel, next. `rotated ~180 0` flips the player's yaw and flattens the pitch, so ^ ^ ^{BEHIND_DISTANCE}
# lands {BEHIND_DISTANCE} blocks straight back from them at their own height — which is what makes this "same floor,
# actually behind" rather than "anywhere within N blocks". Rolled, because the whole point of the
# category is to be missed most of the time.
execute if score #horde_sprint {ns}.data matches 0 store result score #horde_behind_roll {ns}.data run random value 1..100
scoreboard players set #horde_behind {ns}.data 0
execute if score #horde_sprint {ns}.data matches 0 if score #horde_behind_roll {ns}.data matches ..{BEHIND_CHANCE} store success score #horde_behind {ns}.data rotated ~180 0 positioned ^ ^ ^{BEHIND_DISTANCE} at @n[tag={ns}.zombie_round,distance=..{BEHIND_RADIUS}] run function {ns}:v{version}/zombies/vocals/horde_behind

# Otherwise the short groan set, from a random nearby zombie so the horde comes from the right
# direction and distance rather than being centred on the player. Random pitch 0.70..1.05 keeps a
# 6-clip set from sounding metronomic over a long round.
execute if score #horde_sprint {ns}.data matches 0 if score #horde_behind {ns}.data matches 0 store result score #horde_pitch {ns}.data run random value 70..105
execute if score #horde_sprint {ns}.data matches 0 if score #horde_behind {ns}.data matches 0 store result storage {ns}:temp _horde.pitch double 0.01 run scoreboard players get #horde_pitch {ns}.data
execute if score #horde_sprint {ns}.data matches 0 if score #horde_behind {ns}.data matches 0 at @e[tag={ns}.zombie_round,distance=..{VOCAL_RANGE},sort=random,limit=1] run function {ns}:v{version}/zombies/vocals/horde_ambient with storage {ns}:temp _horde

# Schedule this player's next vocal: {HORDE_MAX_INTERVAL} ticks divided by the nearby count, so a lone
# zombie groans every {HORDE_MAX_INTERVAL / 20:.1f}s and {-(-HORDE_MAX_INTERVAL // HORDE_MIN_INTERVAL)}+ zombies sit at the {HORDE_MIN_INTERVAL}-tick ({HORDE_MIN_INTERVAL / 20:.1f}s) floor.
# Density then shows up as volume/reach rather than as rate, which is the point of the floor.
scoreboard players operation #horde_next {ns}.data = #{HORDE_MAX_INTERVAL} {ns}.data
scoreboard players operation #horde_next {ns}.data /= #horde_count {ns}.data
execute if score #horde_next {ns}.data matches ..{HORDE_MIN_INTERVAL} run scoreboard players set #horde_next {ns}.data {HORDE_MIN_INTERVAL}
scoreboard players operation @s {ns}.zb.horde_cd = #horde_next {ns}.data
""")

	# @s = the player; execution position = a nearby zombie, so the sound is directional.
	write_versioned_function("zombies/vocals/horde_ambient", f"$playsound {ns}:{VOCAL_AMBIENT} hostile @s ~ ~ ~ $(vol) $(pitch)")

	## @s = the player; execution position = a zombie directly behind them.
	## Fixed quiet volume, no horde scaling and no pitch shift: this channel is one specific zombie at
	## your back, not a read on how many there are. `return 1` is what the caller's `store success` reads.
	write_versioned_function("zombies/vocals/horde_behind", f"""
playsound {ns}:{VOCAL_BEHIND} hostile @s ~ ~ ~ {BEHIND_VOLUME} 1.0
return 1
""")

	## @s = the player; execution position = a nearby sprinting zombie.
	## `return 1` is what the caller's `store success` reads, so the lockout is only taken when a
	## sprinter was actually found and the scream actually started.
	write_versioned_function("zombies/vocals/horde_sprint", f"""
$playsound {ns}:{VOCAL_SPRINT} hostile @s ~ ~ ~ $(vol) 1.0
return 1
""")

	## Melee grunt. @s = the player who was just hit (called from hurt_player/on_hurt).
	## Played from the attacker's position rather than the player's, so a hit from behind sounds like one.
	## Dogs are excluded: they are not Silent and already have their own wolf vocals.
	write_versioned_function("zombies/vocals/attack", f"""
scoreboard players operation @s {ns}.zb.vox_attack = #total_tick {ns}.data
scoreboard players add @s {ns}.zb.vox_attack {ATTACK_LOCKOUT}
execute at @n[tag={ns}.zombie_round,tag=!{ns}.zb_dog,distance=..{ATTACK_REACH}] run playsound {ns}:{VOCAL_ATTACK} hostile @s ~ ~ ~ 1.0 1.0
""")

	## Death groan. @s = the zombie on the tick its Health reached 0, execution position = the zombie
	## (dispatched from death_watch_tick).
	## The budget is per-player rather than per-death, so one kill always sounds while a Nuke thins out.
	write_versioned_function("zombies/vocals/death", f"""
# Health stays 0 for the whole death animation, so this tag is what makes the groan fire exactly once.
# It also drops this zombie out of the Health read in death_watch_tick for the rest of its existence.
tag @s add {ns}.zb_dying

execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..{VOCAL_RANGE}] unless score @s {ns}.zb.vox_death > #total_tick {ns}.data run function {ns}:v{version}/zombies/vocals/death_for
""")

	## @s = a listening player, execution position = the dying zombie (inherited, `as` does not move it).
	write_versioned_function("zombies/vocals/death_for", f"""
scoreboard players operation @s {ns}.zb.vox_death = #total_tick {ns}.data
scoreboard players add @s {ns}.zb.vox_death {DEATH_LOCKOUT}
playsound {ns}:{VOCAL_DEATH} hostile @s ~ ~ ~ 2.0 1.0
""")

