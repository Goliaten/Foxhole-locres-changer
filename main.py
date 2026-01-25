from collections import defaultdict
import json
from typing import Dict, TypedDict
import pyuepak as pk
from pathlib import Path
import os


class ArgsDict(TypedDict):
    pak_path: str | Path
    locres_path: str | Path
    output_mod_name: str | Path
    alter_keys_json_file: str | Path


def log_entry_exit(func):
    def wrapper(*args, **kwargs):
        print(f"Entering: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Exiting: {func.__name__}")
        return result

    return wrapper


def extract_package(
    pakfile: pk.PakFile, package_path: str | Path, output_name: str | Path
) -> None:
    locres_file = pakfile.read_file(package_path)
    with open(output_name, "wb") as file:
        file.write(locres_file)


@log_entry_exit
def extract(args: ArgsDict) -> None:
    pak = pk.PakFile()
    pak.read(args["pak_path"])
    extract_package(pak, args["locres_path"], TMP_LOCRES_FILE)


def parse_data(data: str) -> str:
    """Parsing rules for new values"""
    data = data.replace("<lf>", "\n")

    return data


def get_keys_to_alter(file_path: str | Path) -> Dict[str, Dict[str, str]]:
    with open(file_path, "r") as file:
        data = json.load(file)
    out = defaultdict(dict)
    for dataline in data:
        namespace, key = dataline.split("::")
        value = data[dataline]

        value = parse_data(value)

        out[namespace][key] = value
    return out


@log_entry_exit
def alter_locres(args: ArgsDict):
    # locres = pl.LocresFile()
    # locres.read(Path(ROOT, TMP_LOCRES_FILE))
    # namespace_keys_to_alter = get_keys_to_alter(args["alter_keys_json_file"])

    # for namespace in locres:
    #     keys_to_alter = namespace_keys_to_alter.get(namespace.name, {})

    #     for key, value in namespace.entrys.items():
    #         if key not in keys_to_alter:
    #             continue
    #         new_value = keys_to_alter.get(key, value.translation)
    #         value.translation = new_value
    #         value.hash = pl.entry_hash(value.translation)

    #         namespace.entrys[key] = value
    # # module doesnt want to save me fookin file
    # locres.write(Path(ROOT, TMP_LOCRES_FILE))


@log_entry_exit
def assemble_mod(args: ArgsDict) -> None:
    n_pak = pk.PakFile()

    with open(Path(ROOT, TMP_LOCRES_FILE), "rb") as file:
        locres = file.read()

    n_pak.add_file(args["locres_path"], bytes(locres))


def main(args: ArgsDict) -> None:
    # open game files
    # extract .locres
    extract(args)

    # edit the .locres
    alter_locres(args)

    # assemble the mod
    assemble_mod(args)


TMP_LOCRES_FILE = "tmp.locres"
TMP_LOCMETA_FILE = "tmp.locmeta"
ROOT = os.path.split(__file__)[0]

if __name__ == "__main__":
    # r"D:\modding\tools\Template\War-WindowsNoEditor_HeadpatsEN61.23.0.pak"
    # r"D:\SteamLibrary\steamapps\common\Foxhole\War\Content\Paks\War-WindowsNoEditor.pak"
    # r"War/Content/Localization/Foxhole-CodeStrings/en/Foxhole-CodeStrings.locres"
    # r"War/Content/Functions/Step.uasset"
    args: ArgsDict = {
        "pak_path": Path(
            r"D:\SteamLibrary\steamapps\common\Foxhole\War\Content\Paks\War-WindowsNoEditor.pak"
        ),
        "locres_path": Path(
            "War/Content/Localization/Foxhole-CodeStrings/en/Foxhole-CodeStrings.locres"
        ),
        "output_mod_name": "test.pak",
        "alter_keys_json_file": "to_alter.json",
    }

    main(args)
