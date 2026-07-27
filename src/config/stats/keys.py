""" Stat key constants: the field-name vocabulary every weapon table and generator shares. """
# Constants
# Mandatory constants
CAPACITY: str = "capacity"
""" Maximum number of bullets that can be loaded into the weapon's magazine. """
REMAINING_BULLETS: str = "remaining_bullets"
""" Current number of bullets remaining in the weapon's magazine.
This value is updated when firing and reloading the weapon. """
RELOAD_TIME: str = "reload_time"
""" Time required to reload the weapon, measured in game ticks. """
SINGLE_RELOAD: str = "single_reload"
""" Shell-by-shell reload (bolt/tube fed weapons): each reload cycle loads exactly one
bullet with its own sound and RELOAD_TIME, then chains into the next shell until the
magazine is full - interrupted by switching weapon or trying to shoot. """
RELOAD_END: str = "reload_end"
""" Additional time in ticks after the reload animation completes.
Used to create a smoother transition between reloading and being able to fire again. """
RELOAD_MID: str = "reload_mid"
""" Time in ticks at which the reload sound effect is triggered during the reload sequence.
This parameter is optional and primarily used for weapons with longer reload animations. """
COOLDOWN: str = "cooldown"
""" Delay between consecutive shots, measured in game ticks.
Controls the weapon's rate of fire. Lower values result in faster firing rates. """
BURST: str = "burst"
""" Number of rounds automatically fired when in burst fire mode.
A value of 1 indicates semi-automatic, while 3 would be a three-round burst. """
CAN_BURST: str = "can_burst"
""" Boolean flag indicating whether the weapon supports burst fire mode.
If true, players can toggle between auto and burst fire modes by dropping the weapon. """
CAN_AUTO: str = "can_auto"
""" Boolean flag indicating whether the weapon supports automatic fire mode.
If true, players can hold right-click to continuously fire. All weapons support semi-auto. """
FIRE_MODE: str = "fire_mode"
""" Current firing mode of the weapon: 'auto' for automatic fire or 'burst' for burst fire.
In auto mode, holding right-click continuously fires. In burst mode, each click fires a fixed burst. """
PELLET_COUNT: str = "pellet_count"
""" Number of projectiles fired per shot (usually for shotguns). """
DAMAGE: str = "damage"
""" Base damage inflicted by each bullet at close range.
This value may be reduced at longer distances based on the decay parameter. """
DECAY: str = "decay"
""" Rate at which damage decreases over distance using multiplication.
For instance, a value of 0.95 means damage decreases to 59.9% damage at 10 blocks distance. """
ACCURACY_BASE: str = "acc_base"
""" Base accuracy of the weapon when standing still.
Lower values indicate better accuracy (smaller spread of bullets). """
ACCURACY_SNEAK: str = "acc_sneak"
""" Accuracy modifier applied when the player is sneaking/crouching.
Typically improves accuracy (reduces spread) when value is lower than base accuracy. """
ACCURACY_WALK: str = "acc_walk"
""" Accuracy penalty applied when the player is walking.
Higher values result in decreased accuracy (wider bullet spread). """
ACCURACY_SPRINT: str = "acc_sprint"
""" Accuracy penalty applied when the player is sprinting.
Significantly increases bullet spread, making the weapon less accurate. """
ACCURACY_JUMP: str = "acc_jump"
""" Accuracy penalty applied when the player is jumping or in mid-air.
Creates the largest reduction in accuracy, simulating the difficulty of shooting while airborne. """
SWITCH: str = "switch"
""" Time required to switch to this weapon, measured in game ticks.
Controls how quickly the player can change weapons in combat. """
KICK: str = "kick"
""" Intensity of the weapon's recoil effect.
Higher values create stronger visual kick when firing. """
CASING_MODEL: str = "casing_model"
""" Type of bullet casing ejected when firing.
Determines the visual model and properties of the ejected casing. """
CASING_OFFSET: str = "casing_offset"
""" Relative position to the player to use when summoning the casing.
The value is modified in setup_database.py according to the zoom type. """
CASING_NORMAL: str = "casing_n"
""" Vertical (Y-axis) component of the ejected casing's direction vector.
Controls the upward force applied to the casing during ejection. """
CASING_TANGENT: str = "casing_t"
""" Forward/backward (Z-axis) component of the ejected casing's direction vector.
Determines how far the casing is pushed forward or backward, with added randomness for realism. """
CASING_BINORMAL: str = "casing_b"
""" Sideways (X-axis) component of the ejected casing's direction vector.
Controls the horizontal offset of the casing, contributing to its full 3D trajectory. """
BASE_WEAPON: str = "base_weapon"
""" Identifier for the base weapon model.
Determines which weapon model and animations to use as a foundation.
Used for weapons that share the same base model but have different stats or attachments. """
WEIGHT: str = "weight"
""" Mystery box weight determining how frequently this weapon can appear.
Higher values mean more common (scale 1-10: 1=very rare, 10=very common). """
SPEED_MULTIPLY_BASE: str = "speed_multiply_base"
""" Optional movement speed multiplier applied while the weapon is held.
Uses the attribute operation `add_multiplied_base` on movement_speed.
Negative values slow the player (e.g. -0.08 = -8% base speed). """

# Projectile constants (for slow-traveling bullets like RPG rockets, grenades, etc.)
PROJECTILE_SPEED: str = "proj_speed"
""" Speed of the projectile in thousandths of blocks/tick (e.g. 1500 = 1.5 blocks/tick).
If present in a weapon's stats, the weapon fires a slow projectile instead of an instant raycast. """
PROJECTILE_GRAVITY: str = "proj_gravity"
""" Gravity applied to the projectile each tick in thousandths of blocks/tick² (e.g. 50 = 0.05 blocks/tick²).
Set to 0 for straight-line travel. Configurable per weapon for arcing projectiles like grenades. """
PROJECTILE_LIFETIME: str = "proj_lifetime"
""" Maximum lifetime of the projectile in game ticks before it auto-explodes.
Prevents orphaned projectiles from existing forever. """
PROJECTILE_MODEL: str = "proj_model"
""" Item model identifier for the visible projectile entity (item_display).
Determines the visual appearance of the projectile in flight. """
EXPLOSION_RADIUS: str = "expl_radius"
""" Radius of the explosion effect in blocks.
Entities within this radius will take damage with distance-based falloff. """
EXPLOSION_DAMAGE: str = "expl_damage"
""" Base damage dealt at the center of the explosion.
Damage decreases with distance based on the explosion decay parameter. """
EXPLOSION_DECAY: str = "expl_decay"
""" Rate at which explosion damage decreases per block of distance from impact center.
Uses the formula: damage *= pow(decay, distance). Lower values = faster falloff. """

# Grenade constants
GRENADE_TYPE: str = "grenade_type"
""" Type of grenade: 'frag', 'semtex', 'smoke', or 'flash'.
If present, the weapon is treated as a throwable grenade instead of a gun. """
GRENADE_FUSE: str = "grenade_fuse"
""" Time in game ticks before the grenade detonates after being thrown. """
GRENADE_DURATION: str = "grenade_duration"
""" Duration of the grenade effect in ticks (for smoke/flash grenades). """
GRENADE_EFFECT_RADIUS: str = "grenade_effect_radius"
""" Radius of the grenade effect in blocks (for smoke/flash grenades). """

# Stats field
STATS_FIELDS: tuple[str, ...] = (
	CAPACITY,
	REMAINING_BULLETS,
	RELOAD_TIME,
	RELOAD_END,
	RELOAD_MID,
	COOLDOWN,
	BURST,
	PELLET_COUNT,
	DAMAGE,
	DECAY,
	ACCURACY_BASE,
	ACCURACY_SNEAK,
	ACCURACY_WALK,
	ACCURACY_SPRINT,
	ACCURACY_JUMP,
	SWITCH,
	KICK,
	WEIGHT,
	SPEED_MULTIPLY_BASE,
	PROJECTILE_SPEED,
	PROJECTILE_GRAVITY,
	PROJECTILE_LIFETIME,
	EXPLOSION_RADIUS,
	EXPLOSION_DAMAGE,
	EXPLOSION_DECAY,
	FIRE_MODE,
	CAN_AUTO,
	CAN_BURST,
)

# Optional constants
MODELS: str = "models"
""" Models to use to switch between normal and zoom modes. """
IS_ZOOM: str = "is_zoom"
""" Indicates whether the weapon is currently in zoom mode """
WEAPON_ID: str = "weapon_id"
""" Dynamic unique identifier assigned to each weapon item when selected from the hotbar.
Used to track weapon switching and manage weapon-specific systems and states."""
PAP_STATS: str = "pap_stats"
""" Pack-a-Punch stat overrides applied when a weapon is upgraded.
Any PAP stat value can be a scalar or a list. Scalars are treated like a list with one value. """
PAP_NAME: str = "pap_name"
""" Optional Pack-a-Punch display name entry inside PAP_STATS.
Can be a scalar string or a list of strings (one per PAP level). """

