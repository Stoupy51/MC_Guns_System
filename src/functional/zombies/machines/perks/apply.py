""" Granting a perk and the per-perk effect function behind it. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....progression import Xp
from .definitions import PERK_DEFINITIONS


# Functions
def write_perk_apply() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/perks/apply", f"""
$scoreboard players set @s {ns}.zb.perk.$(perk_id) 1

# Owning the perk (even from the random-perk power-up) clears its chip-in progress, so a rebuy after going down starts at zero.
$scoreboard players set @s {ns}.zb.perkpaid.$(perk_id) 0

$function {ns}:v{version}/zombies/perks/apply/$(perk_id)
""")

	## Generated from PERK_DEFINITIONS.
	for perk_data in PERK_DEFINITIONS.values():
		lines: list[str] = [
			command.replace("{ns}", ns).replace("{version}", version)
			for command in perk_data.commands
		]
		if perk_data.has_song:
			lines.append(f"execute at @s run playsound {ns}:zombies/perks/{perk_data.perk_id} ambient @s ~ ~ ~ 1.0 1.0")

		# Emojis stay uncoloured in chat.
		msg_emoji, msg_text = perk_data.message.split(" ", 1)
		lines.append(f'tellraw @s [{MGS_TAG},"{msg_emoji} ",{{"text":"{msg_text}","color":"{perk_data.message_color}"}},{Xp.suffix("zb", "perk")}]')
		lines.append(Xp.give("zb", "perk"))
		write_versioned_function(f"zombies/perks/apply/{perk_data.perk_id}", "\n".join(lines))

