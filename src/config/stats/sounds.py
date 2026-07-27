""" Per-gun sound key sets and the resolver that turns them into asset paths. """
# Constants
# Sound keys every gun carries; shotguns swap playerbegin/playerend for a pump.
GUN_SOUNDS: tuple[str, ...] = ("fire", "pap_fire", "reload", "playerbegin", "playerend")
PUMP_SOUNDS: tuple[str, ...] = ("fire", "pap_fire", "reload", "pump")

# Functions
def gun_sounds(weapon_id: str, *keys: str, **overrides: str) -> dict[str, str]:
	""" Sound map for a gun: every key resolves to "<weapon_id>/<key>".

	Overrides replace a listed key in place (keeping its position) or append a new one, so
	non-derivable entries like `crack` and the RPG-7's handling clips stay declarative.
	"""
	return {key: f"{weapon_id}/{key}" for key in keys} | overrides

