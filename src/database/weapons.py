
# Imports
from stewbeet import Item, JsonDict

from ..config.catalogs import SCOPE_VARIANTS
from ..config.stats import (
    AK47,
    AUG,
    DEAGLE,
    FAMAS,
    FNFAL,
    G3A3,
    GLOCK17,
    GLOCK18,
    M4A1,
    M9,
    M16A4,
    M24,
    M82,
    M249,
    M500,
    M590,
    M1911,
    MAC10,
    MAKAROV,
    MOSIN,
    MP5,
    MP7,
    PPSH41,
    RAY_GUN,
    RPK,
    SCAR17,
    SPAS12,
    STEN,
    SVD,
    VZ61,
    add_item,
)

# Map weapon ID -> stats dict
WEAPON_STATS: dict[str, JsonDict] = {
    "ak47": AK47, "aug": AUG, "famas": FAMAS, "fnfal": FNFAL, "g3a3": G3A3,
    "m4a1": M4A1, "m16a4": M16A4, "m24": M24, "m82": M82, "m249": M249,
    "m500": M500, "m590": M590, "mac10": MAC10, "mosin": MOSIN, "mp5": MP5,
    "mp7": MP7, "ppsh41": PPSH41, "rpk": RPK, "scar17": SCAR17, "spas12": SPAS12,
    "sten": STEN, "svd": SVD,
    # Pistols
    "m1911": M1911, "m9": M9, "deagle": DEAGLE, "makarov": MAKAROV,
    "glock17": GLOCK17, "glock18": GLOCK18, "vz61": VZ61, "ray_gun": RAY_GUN,
}

# Special rarity overrides
WEAPON_RARITY: dict[str, str] = {
    "ray_gun": "epic",
}


def main() -> None:
    weapons: list[Item] = [Item.from_id("rpg7")]
    for weapon_id, stats in WEAPON_STATS.items():
        # Get scope variants from catalog (default: iron sights only)
        variants: tuple[str, ...] = SCOPE_VARIANTS.get(weapon_id, ("",))
        rarity: str | None = WEAPON_RARITY.get(weapon_id)
        for suffix in variants:
            item_id: str = f"{weapon_id}{suffix}"
            for name in (item_id, f"{item_id}_zoom"):
                item: Item = add_item(name, stats=stats, model_path="auto")
                if rarity:
                    item.components["rarity"] = rarity
                weapons.append(item)

    # For each weapon, make variants with only one material (e.g. wood, metal, gold, etc.)
    # TODO: move after "Adjust guns data" in setup definitions, better for components
    for material in ("gold", "autumn", "black_metal", "copper", "red_polymer_stripes"):
        for weapon in weapons:
            item_id: str = f"{weapon.id}_{material}" if not weapon.id.endswith("_zoom") else f"{weapon.id[:-5]}_{material}_zoom"
            item: Item = Item(
                id=item_id, base_item=weapon.base_item, components=weapon.components.copy(), override_model=weapon.override_model
            )

            # Replace texture in override model with material texture
            if item.override_model:
                item.override_model = item.override_model.copy()
                item.override_model["textures"] = item.override_model.get("textures", {}).copy()
                for key, texture in item.override_model["textures"].items():
                    if all(x not in texture for x in ("acogdetails", "holodetails", "kobradetails", "reticles")):
                        item.override_model["textures"][key] = f"mgs:item/{material}"

