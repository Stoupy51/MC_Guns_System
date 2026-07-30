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
""" 12 short groans, the walking/running horde. """
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

SPRINT_LOCKOUT: int = 100
""" Ticks a player's sprint channel stays held after a scream. The longest clip is 4.94s (99 ticks), so
one scream at a time is exactly what this buys — the BO2 sprinter that owns the soundscape while it closes. """
ATTACK_LOCKOUT: int = 20
""" Ticks between melee grunts for one player. A surrounded player is hit by up to eight zombies, and
eight overlapping grunts is mush; one per second still reads as "something is hitting me". """
DEATH_LOCKOUT: int = 4
""" Ticks between death groans for one player. A Nuke kills the whole round in a single tick, which
without this is 50 simultaneous groans that drop every other sound in the mix. """

VOCAL_RANGE: int = 32
""" Blocks a vocal carries. Volume 2.0 gives full loudness inside 16 blocks and fades out to this. """
ATTACK_REACH: float = 3.5
""" Blocks searched for the zombie that landed the hit. Melee reach is ~2-3, so this finds the attacker
without picking up a bystander across the room. """

HORDE_MAX_INTERVAL: int = 40
""" Ticks between vocals with a single zombie nearby; the interval is this divided by the count. """
HORDE_MIN_INTERVAL: int = 4
""" Floor on that interval, so a huge horde stays a wall of groans rather than a buzz. """


# Functions
def generate_vocals() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Managed horde ambience.
	# Round zombies are Silent, so a 50-zombie horde can't stack into a wall of groans on its own.
	# Instead each player hears ONE controlled vocal at a time, and both its volume and how often it repeats scale with the zombie count near THEM.
	# The rate is what sells a chase: ten zombies on your heels groan several times a second, an empty room barely at all.
	write_versioned_function("zombies/horde_ambient", f"""
# @s = an in-game player. Count zombies within earshot.
execute store result score #horde_count {ns}.data if entity @e[tag={ns}.zombie_round,distance=..{VOCAL_RANGE}]

# Nothing nearby: wait a full cycle before paying for another entity scan.
execute if score #horde_count {ns}.data matches ..0 run scoreboard players set @s {ns}.zb.horde_cd {HORDE_MAX_INTERVAL}
execute if score #horde_count {ns}.data matches ..0 run return 0

# Volume (hundredths) = 0.25 + count*0.03, hard-capped at 0.80 (so ~18+ zombies all sound the same).
scoreboard players set #horde_vol {ns}.data 25
scoreboard players operation #horde_tmp {ns}.data = #horde_count {ns}.data
scoreboard players operation #horde_tmp {ns}.data *= #3 {ns}.data
scoreboard players operation #horde_vol {ns}.data += #horde_tmp {ns}.data
execute if score #horde_vol {ns}.data matches 80.. run scoreboard players set #horde_vol {ns}.data 80
execute store result storage {ns}:temp _horde.vol double 0.01 run scoreboard players get #horde_vol {ns}.data

# Sprint channel first. BO2 leads with the sprinter that is closing on you rather than a random member
# of the horde, and the channel lockout is what keeps it to one scream at a time (see SPRINT_LOCKOUT).
# The scream is NOT pitch-shifted: bending a 4-second human scream is instantly audible as a gimmick.
scoreboard players set #horde_sprint {ns}.data 0
execute unless score @s {ns}.zb.vox_sprint > #total_tick {ns}.data store success score #horde_sprint {ns}.data at @n[tag={ns}.zb_sprint,tag={ns}.zombie_round,distance=..{VOCAL_RANGE},sort=random] run function {ns}:v{version}/zombies/vocals/horde_sprint with storage {ns}:temp _horde
execute if score #horde_sprint {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.vox_sprint = #total_tick {ns}.data
execute if score #horde_sprint {ns}.data matches 1 run scoreboard players add @s {ns}.zb.vox_sprint {SPRINT_LOCKOUT}

# Otherwise the short groan set, from a random nearby zombie so the horde comes from the right
# direction and distance rather than being centred on the player. Random pitch 0.70..1.05 keeps a
# 12-clip set from sounding metronomic over a long round.
execute if score #horde_sprint {ns}.data matches 0 store result score #horde_pitch {ns}.data run random value 70..105
execute if score #horde_sprint {ns}.data matches 0 store result storage {ns}:temp _horde.pitch double 0.01 run scoreboard players get #horde_pitch {ns}.data
execute if score #horde_sprint {ns}.data matches 0 at @e[tag={ns}.zombie_round,distance=..{VOCAL_RANGE},sort=random,limit=1] run function {ns}:v{version}/zombies/vocals/horde_ambient with storage {ns}:temp _horde

# Schedule this player's next vocal: {HORDE_MAX_INTERVAL} ticks divided by the nearby count, so 1 zombie
# groans every {HORDE_MAX_INTERVAL / 20:.1f}s and 10 groan {20 * 10 // HORDE_MAX_INTERVAL} times a second.
# The floor keeps a huge horde from turning into a buzz.
scoreboard players operation #horde_next {ns}.data = #{HORDE_MAX_INTERVAL} {ns}.data
scoreboard players operation #horde_next {ns}.data /= #horde_count {ns}.data
execute if score #horde_next {ns}.data matches ..{HORDE_MIN_INTERVAL} run scoreboard players set #horde_next {ns}.data {HORDE_MIN_INTERVAL}
scoreboard players operation @s {ns}.zb.horde_cd = #horde_next {ns}.data
""")

	# @s = the player; execution position = a nearby zombie, so the sound is directional.
	write_versioned_function("zombies/vocals/horde_ambient", f"$playsound {ns}:{VOCAL_AMBIENT} hostile @s ~ ~ ~ $(vol) $(pitch)")

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

	## Death groan. @s = the dying zombie, execution position = the zombie (called from on_zombie_dying).
	## The budget is per-player rather than per-death, so one kill always sounds while a Nuke thins out.
	write_versioned_function("zombies/vocals/death", f"""
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,distance=..{VOCAL_RANGE}] unless score @s {ns}.zb.vox_death > #total_tick {ns}.data run function {ns}:v{version}/zombies/vocals/death_for
""")

	## @s = a listening player, execution position = the dying zombie (inherited, `as` does not move it).
	write_versioned_function("zombies/vocals/death_for", f"""
scoreboard players operation @s {ns}.zb.vox_death = #total_tick {ns}.data
scoreboard players add @s {ns}.zb.vox_death {DEATH_LOCKOUT}
playsound {ns}:{VOCAL_DEATH} hostile @s ~ ~ ~ 2.0 1.0
""")
