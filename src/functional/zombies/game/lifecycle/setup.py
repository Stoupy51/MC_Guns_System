""" Zombies scoreboards, storage layout and the signal function tags. """
# Imports
from stewbeet import Mem, write_load_file, write_tag


# Functions
def write_zombies_setup() -> None:
	ns: str = Mem.ctx.project_id

	## Scoreboards & Storage Setup
	write_load_file(f"""
## Zombies scoreboards
scoreboard objectives add {ns}.zb.in_game dummy
scoreboard objectives add {ns}.zb.points dummy
scoreboard objectives add {ns}.zb.kills dummy
scoreboard objectives add {ns}.zb.downs dummy

# Bought lethal grenade type (index into LETHAL_GRENADE_IDS, 0 = frag): re-gives the RIGHT type
# when the lethal slot is emptied (round-end replenish / Max Ammo / recovery). See inventory.py.
scoreboard objectives add {ns}.zb.lethal_type dummy

# Perk scoreboards
# zb.passive: 0=none, 1=points_x1.2, 2=powerup_x1.5
# zb.ability: 0=none, 1=coward, 2=guardian
# Ability cooldown (0 = ready, 1+ = on cooldown in rounds remaining)
scoreboard objectives add {ns}.zb.passive dummy
scoreboard objectives add {ns}.zb.ability dummy
scoreboard objectives add {ns}.zb.ability_cd dummy

# Ticks until this player's next horde vocal; horde_ambient refreshes it from the count near THEM
scoreboard objectives add {ns}.zb.horde_cd dummy

# Zombie vocal budgets (enemies/vocals.py): #total_tick timestamps of when each channel frees up again.
# No reset needed anywhere — #total_tick only ever grows, so a stale value is always in the past, and an
# unset score fails the `>` comparison, which reads as "ready".
scoreboard objectives add {ns}.zb.vox_sprint dummy
scoreboard objectives add {ns}.zb.vox_attack dummy
scoreboard objectives add {ns}.zb.vox_death dummy

# Per-enemy Health x1000, read by death_watch_tick only while the enemy is not yet tagged zb_dying.
# Hitting 0 is what fires the death groan, on the exact tick the enemy died.
scoreboard objectives add {ns}.zb.hp dummy

# Spawn point group_id scoreboard
scoreboard objectives add {ns}.zb.spawn.gid dummy

# Spawn point unique id: held by spawn markers, and by zombies as "last spawn point used"
# (initial spawn or stuck-rescue) so a rescue never reuses the previous spawn point.
scoreboard objectives add {ns}.zb.spawn.sid dummy

# Sidebar rank scoreboard
scoreboard objectives add {ns}.zb.sb_rank dummy

# Rise animation: ticks remaining for each rising zombie
scoreboard objectives add {ns}.zb.rise_tick dummy

# Kill tracking (vanilla totalKillCount stat) and baseline snapshot
scoreboard objectives add {ns}.total_kills totalKillCount
scoreboard objectives add {ns}.zb.prev_kills dummy

# Stuck zombie detection per-zombie scores
scoreboard objectives add {ns}.zb.stuck_x dummy
scoreboard objectives add {ns}.zb.stuck_z dummy
scoreboard objectives add {ns}.zb.stuck_ticks dummy
scoreboard objectives add {ns}.zb.stuck_dist dummy

# Initialize zombies game state
execute unless data storage {ns}:zombies game run data modify storage {ns}:zombies game set value {{state:"lobby",map_id:"",round:0}}

# Game variant: "vanilla" = classic CoD zombies, "zonweeb" = passives/abilities/special zombies
execute unless data storage {ns}:zombies game.variant run data modify storage {ns}:zombies game.variant set value "zonweeb"

# Initialize mystery box base pool (can be extended via function tag)
execute unless data storage {ns}:zombies mystery_box_pool run data modify storage {ns}:zombies mystery_box_pool set value []
""")

	## Signal function tags
	for event in ["register_maps", "register_mystery_box_item", "on_round_start", "on_round_end", "on_game_start", "on_game_end"]:
		write_tag(f"zombies/{event}", Mem.ctx.data[ns].function_tags, [])

