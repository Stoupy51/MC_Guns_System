""" Widow's Wine: the web burst, shared by the thrown grenade and the on-hurt passive. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_widows_wine() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Widow's Wine: web grenades, a passive web burst when hurt, and a knife melee bump.
	# The web applies heavy slowness, weakness and light damage to every zombie in range.
	# Shared by the thrown grenade and the on-hurt passive so the effect is defined once.

	## Web burst: @s/pos = the burst center. Macro radius (blocks). Roots + lightly damages zombies.
	write_versioned_function("zombies/perks/widows_web_burst", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(radius)] run function {ns}:v{version}/zombies/perks/widows_web_hit
""")

	# Per-zombie webbing (@s = zombie): 5s stun, weakness, cobweb particle, light damage.
	# NOTE /effect give durations are in SECONDS, not ticks; 400 once meant a ~6.7min freeze.
	write_versioned_function("zombies/perks/widows_web_hit", f"""
effect give @s minecraft:slowness 5 5 true
effect give @s minecraft:weakness 5 2 true
particle minecraft:item{{item:"minecraft:cobweb"}} ~ ~0.5 ~ 0.3 0.5 0.3 0.05 8
execute store result storage {ns}:temp _ww_dmg.amount int 1 run attribute @s minecraft:max_health get 0.15
data modify storage {ns}:temp _ww_dmg.type set value "minecraft:generic"
function {ns}:v{version}/zombies/traps/apply_trap_damage with storage {ns}:temp _ww_dmg
""")

	# When a Widow's Wine owner is hurt, consume one web grenade and burst webbing around themselves.
	# The burst only targets zombies, and a 2s cooldown stops a flurry of hits draining the stock.
	write_versioned_function("zombies/perks/widows_on_hurt", f"""
# Need at least one web grenade in the lethal slot (grenade_type lives under the item's stats compound)
execute unless items entity @s hotbar.7 *[custom_data~{{{ns}:{{stats:{{grenade_type:"web"}}}}}}] run return fail

# 2s (40t) internal cooldown
execute store result score #ww_now {ns}.data run time query gametime
scoreboard players operation #ww_since {ns}.data = #ww_now {ns}.data
scoreboard players operation #ww_since {ns}.data -= @s {ns}.zb.ww_last
execute if score #ww_since {ns}.data matches ..39 run return fail
scoreboard players operation @s {ns}.zb.ww_last = #ww_now {ns}.data

# Consume one web grenade + burst webbing around the player
item modify entity @s hotbar.7 {ns}:v{version}/grenade/consume_one
particle minecraft:item{{item:"minecraft:cobweb"}} ~ ~1 ~ 0.8 0.8 0.8 0.1 40 force @a[distance=..48]
playsound minecraft:block.wool.place player @a[distance=..32] ~ ~ ~ 1 0.7
execute store result storage {ns}:temp _web.radius float 1 run scoreboard players get #4 {ns}.data
execute at @s run function {ns}:v{version}/zombies/perks/widows_web_burst with storage {ns}:temp _web
""")

