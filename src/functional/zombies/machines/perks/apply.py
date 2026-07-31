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
# Set perk scoreboard for the player
$scoreboard players set @s {ns}.zb.perk.$(perk_id) 1

# Owning the perk voids any chip-in progress toward it (including perks granted for free by the
# random-perk power-up), so a re-purchase after going down starts from zero.
$scoreboard players set @s {ns}.zb.perkpaid.$(perk_id) 0

# Call perk-specific effect function
$function {ns}:v{version}/zombies/perks/apply/$(perk_id)
""")

	## Per-perk effect functions (generated from top-level metadata)
	for perk_id, perk_data in PERK_DEFINITIONS.items():
		extra_commands: str = "\n".join(
			command.replace("{ns}", ns).replace("{version}", version)
			for command in perk_data.commands
		)
		# Split the emoji prefix out of the colored component (emojis stay uncolored in chat)
		msg_emoji, msg_text = perk_data.message.split(" ", 1)
		write_versioned_function(f"zombies/perks/apply/{perk_id}", f"""
{extra_commands}
tellraw @s [{MGS_TAG},"{msg_emoji} ",{{"text":"{msg_text}","color":"{perk_data.message_color}"}},{Xp.suffix("zb", "perk")}]
{Xp.give("zb", "perk")}
""")

