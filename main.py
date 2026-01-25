from collections import defaultdict
import json
import pprint
from typing import Dict, TypedDict
import pyuepak as pk
from pathlib import Path
import os
import subprocess


class ArgsDict(TypedDict):
    pak_path: str | Path
    locres_path: str | Path
    output_mod_name: str | Path
    alter_keys_json_file: str | Path
    UE4localizationsTool_path: str | Path


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
def extract_locres(args: ArgsDict) -> None:
    pak = pk.PakFile()
    pak.read(args["pak_path"])
    extract_package(pak, args["locres_path"], TMP_LOCRES_PATH)


def disassemble_locres(args: ArgsDict):
    command = [
        args["UE4localizationsTool_path"],
        "export",
        TMP_LOCRES_PATH,
    ]
    print(" ".join(command))
    p1 = subprocess.Popen(command)
    p1.wait()
    p1.kill()


def parse_data(data: str) -> str:
    """Parsing rules for new values"""
    data = data.replace("<lf>", "\n")

    return data


def get_keys_to_alter(file_path: str | Path) -> Dict[str, str]:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def open_exported_locres(args: ArgsDict) -> Dict[str, str]:
    out: Dict[str, str] = {}
    with open(TMP_LOCRES_EXPORTED_PATH, "r") as file:
        while line := file.readline():
            line_s = line.split("=", 1)
            out[line_s[0]] = line_s[1]
    return out


@log_entry_exit
def alter_locres(args: ArgsDict) -> Dict[str, str]:
    data = open_exported_locres(args)
    to_replace = get_keys_to_alter(args["alter_keys_json_file"])
    return data | to_replace


def assemble_locres(args: ArgsDict, data: Dict[str, str]) -> None:
    command = [
        args["UE4localizationsTool_path"],
        "import",
        TMP_LOCRES_EXPORTED_PATH,
    ]
    print(" ".join(command))
    p1 = subprocess.Popen(command)
    p1.wait()
    p1.kill()


@log_entry_exit
def assemble_mod(args: ArgsDict) -> None:
    n_pak = pk.PakFile()

    with open(TMP_LOCRES_IMPORTED_PATH, "rb") as file:
        locres = file.read()

    n_pak.add_file(args["locres_path"], bytes(locres))
    n_pak.write(OUTPUT_NAME)


def main(args: ArgsDict) -> None:
    # open game files
    # extract .locres
    extract_locres(args)
    disassemble_locres(args)

    # edit the .locres
    data = alter_locres(args)
    assemble_locres(args, data)

    # assemble the mod
    assemble_mod(args)


TMP_LOCRES_FILE = "tmp.locres"
TMP_LOCRES_EXPORTED = TMP_LOCRES_FILE + ".txt"
TMP_LOCRES_IMPORTED = TMP_LOCRES_FILE.replace(".", "_NEW.", 1)
ROOT = os.path.split(__file__)[0]
TMP_LOCRES_PATH = os.path.join(ROOT, TMP_LOCRES_FILE)
# though does the exporter import in local dir, or the dir of itself
TMP_LOCRES_EXPORTED_PATH = os.path.join(ROOT, TMP_LOCRES_EXPORTED)
TMP_LOCRES_IMPORTED_PATH = os.path.join(ROOT, TMP_LOCRES_IMPORTED)
OUTPUT_NAME = "output_pak.pak"

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
        "UE4localizationsTool_path": r"UE4localizationsTool.exe",
    }

    main(args)
