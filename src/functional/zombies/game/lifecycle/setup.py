""" Zombies scoreboards, storage layout and the signal function tags. """
# Imports
from stewbeet import Mem, write_load_file, write_tag


# Functions
def write_zombies_setup() -> None:
	ns: str = Mem.ctx.project_id

	write_load_file(f"""
scoreboard objectives add {ns}.zb.in_game dummy
scoreboard objectives add {ns}.zb.points dummy
scoreboard objectives add {ns}.zb.kills dummy
scoreboard objectives add {ns}.zb.downs dummy

# zb.run: the #zb_run a player plays in, 0 once zombies/reset_player cleaned them. A player offline when their run
# ended keeps theirs, which is how zombies/on_rejoin tells them apart from one coming back to the run.
scoreboard objectives add {ns}.zb.run dummy
scoreboard objectives add {ns}.zb.rejoins custom:leave_game

# Index into LETHAL_GRENADE_IDS (0 = frag), so an emptied lethal slot refills the bought type (see inventory).
scoreboard objectives add {ns}.zb.lethal_type dummy
# Index into TACTICAL_GRENADE_IDS plus one, 0 for none, so Max Ammo gives back an emptied tactical slot.
scoreboard objectives add {ns}.zb.tactical_type dummy

# zb.passive: 0 none, 1 points x1.2, 2 power-ups x1.5. zb.ability: 0 none, 1 coward, 2 guardian.
# zb.ability_cd: rounds of cooldown left (0 = ready).
scoreboard objectives add {ns}.zb.passive dummy
scoreboard objectives add {ns}.zb.ability dummy
scoreboard objectives add {ns}.zb.ability_cd dummy

# Ticks to this player's next horde vocal.
scoreboard objectives add {ns}.zb.horde_cd dummy

# #total_tick when each vocal channel frees up (see vocals). Never reset: #total_tick only grows,
# and an unset score fails the `>` test, which reads as ready.
scoreboard objectives add {ns}.zb.vox_sprint dummy
scoreboard objectives add {ns}.zb.vox_attack dummy
scoreboard objectives add {ns}.zb.vox_death dummy

scoreboard objectives add {ns}.zb.spawn.gid dummy

# Held by spawn markers, and by zombies as the last spawn they used, so a rescue never reuses it.
scoreboard objectives add {ns}.zb.spawn.sid dummy

scoreboard objectives add {ns}.zb.sb_rank dummy

# Ticks left for a rising zombie; on a spawn marker, the whole rise duration.
scoreboard objectives add {ns}.zb.rise_tick dummy
# Thousandths of a block per tick, negative for a spawn_from_ceiling descent.
scoreboard objectives add {ns}.zb.rise_step dummy

# A zombie's whole health, absorption included, which max_health alone cannot hold past 1024.
scoreboard objectives add {ns}.zb.max_hp dummy

# totalKillCount, and the baseline snapshot.
scoreboard objectives add {ns}.total_kills totalKillCount
scoreboard objectives add {ns}.zb.prev_kills dummy

scoreboard objectives add {ns}.zb.stuck_x dummy
scoreboard objectives add {ns}.zb.stuck_z dummy
scoreboard objectives add {ns}.zb.stuck_ticks dummy
scoreboard objectives add {ns}.zb.stuck_dist dummy

execute unless data storage {ns}:zombies game run data modify storage {ns}:zombies game set value {{state:"lobby",map_id:"",round:0}}

# "vanilla": classic CoD zombies; "zonweeb": passives, abilities and special zombies.
execute unless data storage {ns}:zombies game.variant run data modify storage {ns}:zombies game.variant set value "zonweeb"

# Extended through a function tag.
execute unless data storage {ns}:zombies mystery_box_pool run data modify storage {ns}:zombies mystery_box_pool set value []
""")

	for event in ["register_maps", "register_mystery_box_item", "on_round_start", "on_round_end", "on_game_start", "on_game_end"]:
		write_tag(f"zombies/{event}", Mem.ctx.data[ns].function_tags, [])

