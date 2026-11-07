""" Upload the built zips to GitHub, Modrinth and Smithed, using the credentials in ~/stewbeet/credentials.yml. """

# Imports
from beet import ProjectConfig
from stewbeet import JsonDict
from stewbeet.continuous_delivery import (
	load_credentials,
	upload_to_github,
	upload_to_modrinth,
	upload_to_smithed,
)
from stewbeet.utils import get_project_config
from stouputils.io import read_file

# Constants
SUMMARY: str = "Guns, Call of Duty style game modes and a Zombies mode, as a datapack and a resource pack."

# Get credentials and the beet configuration
credentials: dict[str, str] = load_credentials("~/stewbeet/credentials.yml")
cfg: ProjectConfig = get_project_config()
if cfg.output is None:
	raise ValueError("The beet configuration must define an output folder before uploading")
output_folder: str = str(cfg.output)

ZIP_FILES: list[str] = [
	f"{output_folder}/MCGunsSystem_datapack_with_libs.zip",
	f"{output_folder}/MCGunsSystem_resource_pack_with_libs.zip",
	f"{output_folder}/MCGunsSystem_datapack.zip",
	f"{output_folder}/MCGunsSystem_resource_pack.zip",
]

# Upload to GitHub
github_config: JsonDict = {
	"project_name": "MC_Guns_System",
	"version": cfg.version,
	"build_folder": output_folder,
	"files": ZIP_FILES,
}
changelog: str = upload_to_github(credentials, github_config)

# Upload to Modrinth
modrinth_config: JsonDict = {
	"slug": "mc_guns_system",
	"project_name": cfg.name,
	"version": cfg.version,
	"summary": SUMMARY,
	"description_markdown": read_file(f"{cfg.directory}/README.md"),
	"version_type": "release",
	"build_folder": output_folder,
}
upload_to_modrinth(credentials, modrinth_config, changelog)

# Upload to Smithed
smithed_config: JsonDict = {
	"project_id": "mc_guns_system",
	"project_name": cfg.name,
	"version": cfg.version,
	"github_project_name": "MC_Guns_System",
}
upload_to_smithed(credentials, smithed_config, changelog)

