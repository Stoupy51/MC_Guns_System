""" Shared command builders for zombies modules. """
# Imports
from stewbeet import write_versioned_function

from ..core.feedback import ZombiesFeedback
from ..helpers import MGS_TAG
from ..helpers.lifecycle import GameLifecycle


# Classes
class ZombiesCommon:
	""" Common helpers. """

	# Functions
	@staticmethod
	def game_active_guard_cmd(ns: str) -> str:
		""" Return the standard guard command for active zombies games. """
		return GameLifecycle.game_active_guard(ns, "zombies")

	@staticmethod
	def write_deny_functions() -> None:
		""" The two handlers every "you can't do that" path in zombies falls back to. """
		# The message rides in as a whole text component so the English stays a literal here for auto.lang_file.
		# The argument is `msg`, not `text`, or lang_file would translate the outer quoted value instead of the component inside it.
		write_versioned_function("zombies/deny/message", f"""
$tellraw @s [{MGS_TAG},$(msg)]
{ZombiesFeedback.zb_sound('deny')}
""")

		# Same message everywhere, only the score holding the price differs
		write_versioned_function("zombies/deny/not_enough_points", f"""
$tellraw @s [{MGS_TAG},{{"text":"You don't have enough points (","color":"red"}},{{"score":{{"name":"$(score)","objective":"$(obj)"}},"color":"yellow"}},{{"text":" needed).","color":"red"}}]
{ZombiesFeedback.zb_sound('deny')}
""")

	@staticmethod
	def deny_cmd(ns: str, version: str, component: str) -> str:
		""" One command showing `component` in chat with the deny sound, so it survives `return run`. """
		return f"function {ns}:v{version}/zombies/deny/message {{msg:'{component}'}}"

	@staticmethod
	def deny_not_enough_points_cmd(ns: str, version: str, price_score: str, objective: str = "") -> str:
		""" One command for the shared not-enough-points message, naming the score that holds the price. """
		obj: str = objective or f"{ns}.data"
		return f'function {ns}:v{version}/zombies/deny/not_enough_points {{score:"{price_score}",obj:"{obj}"}}'

	@staticmethod
	def gun_cd(ns: str) -> str:
		""" Return the custom-data predicate body matching any gun item.

		Returns:
			str: The body of a `custom_data~` item predicate, braces included.

		>>> ZombiesCommon.gun_cd("mgs")
		'{mgs:{gun:true}}'
		"""
		return "{" + ns + ":{gun:true}}"

