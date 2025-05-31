
# Imports
import os

ROOT: str = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")  # This line gets the full root path to this folder, don't change it unless you know what you're doing.
IGNORE_UNSET: bool = True                          # If True, the program will ignore unset optionnal values in the configuration dictionnary


# Folders
BUILD_FOLDER: str = f"{ROOT}/build"                 # Folder where the final datapack and resource pack are built
ASSETS_FOLDER: str = f"{ROOT}/assets"               # Folder containing the all assets (textures, sounds, ... folders) for the datapack and resource pack
MERGE_FOLDER: str = f"{ROOT}/merge"
BUILD_COPY_DESTINATIONS: tuple[list, list] = (["D:/latest_snapshot/world/datapacks"],["D:/minecraft/snapshot/resourcepacks"])


# Dev constants
DATABASE_DEBUG: str = f"{ROOT}/database_debug.json" # Dump of the database for debugging purposes
ENABLE_TRANSLATIONS: bool = True                    # Will convert all the text components to translate and generate a lang file in the resource pack.
MERGE_LIBS: bool = False                             # Make new zip of merged libraries with the datapack and resource pack using Smithed Weld


# Project information
AUTHOR: str = "TheBradqq, Stoupy51"      # Author(s) name(s) displayed in pack.mcmeta, also used to add convention.debug tag to the players of the same name(s)
PROJECT_NAME: str = "MC Guns System"     # Name of the datapack, used for messages and items lore
VERSION: str = "5.0.0"                   # Project version in the following mandatory format: major.minor.patch, ex: 1.0.0 or 1.21.615
NAMESPACE: str = "mgs"                   # Simplified version of the datapack name. Used to namespace functions, tags, etc. Should be the same you use in the merge folder.
DESCRIPTION = f"{PROJECT_NAME} [{VERSION}] by {AUTHOR}" # Pack description displayed in pack.mcmeta


# Technical constants
SOURCE_LORE: list[dict] = [{"text":"ICON"},{"text":f" {PROJECT_NAME}","italic":True,"color":"blue"}]	# Appended lore to any custom item, can be an empty string


# Configuration dictionnary
configuration = {
    "ignore_unset": IGNORE_UNSET,

    "build_folder": BUILD_FOLDER,
    "assets_folder": ASSETS_FOLDER,
    "merge_folder": MERGE_FOLDER,
    "build_copy_destinations": BUILD_COPY_DESTINATIONS,
    "database_debug": DATABASE_DEBUG,
    "enable_translations": ENABLE_TRANSLATIONS,
    "merge_libs": MERGE_LIBS,
    "author": AUTHOR,
    "project_name": PROJECT_NAME,
    "version": VERSION,
    "namespace": NAMESPACE,
    "description": DESCRIPTION,
    "source_lore": SOURCE_LORE,
}

