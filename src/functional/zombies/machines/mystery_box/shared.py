""" Move animation timings, the presence-box transformations and the owned-gun predicate. """
# Imports


# Constants
# Move animation constants
MOVE_BEAR_TICKS: int = 30
""" Bear visible before ascend starts. """
MOVE_ASCEND_TICKS: int = 80
""" Ascend at old location. """
MOVE_WAIT_TICKS: int = 100
""" 5-second wait before descending. """
MOVE_DESCEND_TICKS: int = 70
""" Descend at new location. """
MOVE_TOTAL_TICKS: int = MOVE_BEAR_TICKS + MOVE_ASCEND_TICKS + MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS
""" 280. """

# Monkey Bomb pool weight (weapon weights come from the catalog; the monkey is a non-catalog tactical added to the pool manually — BO-style fairly common roll)
MONKEY_BOMB_WEIGHT: int = 5

MB_SCALE: float = 2.4
""" Uniform scale of the two item_displays a presence box is made of.
The chest model is full-width, so 2.4 makes the box about 2.4 blocks across.
"""
MB_CLOSED_TF: str = f"{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[{MB_SCALE}f,{MB_SCALE}f,{MB_SCALE}f]}}"
""" Lid transformation at rest: identity rotation, so the two halves sit flush. """
MB_OPEN_TF: str = f"{{left_rotation:[-0.766f,0f,0f,0.643f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.415f,-0.652f],scale:[{MB_SCALE}f,{MB_SCALE}f,{MB_SCALE}f]}}"
""" Lid transformation when open: hinged ~100° about X at the lid's front-bottom edge, like a real chest opening toward the front.
An item_display rotates about the model centre, so the translation cancels that out to keep the hinge edge fixed (T = p - R·p, with p = (0, -0.15, -0.6) the hinge's scaled offset from the centre).
"""

# Functions
def owned_gun_macro_cd(ns: str) -> str:
	""" Custom-data predicate matching any gun whose base weapon is the macro's $(weapon_id).

	Args:
		ns (str): The project namespace.
	Returns:
		str: The body of a `custom_data~` item predicate, braces included.

	Examples:
		>>> owned_gun_macro_cd("mgs")
		'{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}'
	"""
	return "{" + ns + ':{gun:true,stats:{base_weapon:"$(weapon_id)"}}}'

