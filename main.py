import json
from shutil import copy, rmtree
from typing import Dict, List, TypedDict
import config as cfg
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


def run_subprocess(command: List[str]) -> None:
    p1 = subprocess.Popen(command)
    p1.wait()
    p1.kill()
    stdout, stderr = p1.communicate()
    print("stdout:", stdout.decode() if stdout else "")
    print("stderr:", stderr.decode() if stderr else "")


def extract_package(
    pakfile: pk.PakFile, package_path: str | Path, output_name: str | Path
) -> None:
    locres_file = pakfile.read_file(package_path)
    with open(output_name, "wb") as file:
        file.write(locres_file)


def get_game_version(pak: pk.PakFile, args: ArgsDict) -> str:
    data = pak.read_file(cfg.DEFAULT_GAME_PATH)
    data = data.decode().split("\r\n")
    for x in data:
        if "ProjectVersion" in x:
            return x.split("=")[1]
    return ""


@log_entry_exit
def extract_data(args: ArgsDict) -> str:
    pak = pk.PakFile()
    pak.read(args["pak_path"])
    extract_package(pak, args["locres_path"], cfg.TMP_LOCRES_PATH)

    return get_game_version(pak, args)


def disassemble_locres(args: ArgsDict):
    command = [
        args["UE4localizationsTool_path"],
        "export",
        cfg.TMP_LOCRES_PATH,
    ]
    run_subprocess(command)


def get_keys_to_alter(file_path: str | Path) -> Dict[str, str]:
    with open(file_path, "r") as file:
        data = json.load(file)

    data = {
        key: (value if value[-2:] == "\n" else value + "\n")
        for key, value in data.items()
    }
    return data


def open_exported_locres(args: ArgsDict) -> Dict[str, str]:
    out: Dict[str, str] = {}
    with open(cfg.TMP_LOCRES_EXPORTED_PATH, "r") as file:
        while line := file.readline():
            line_s = line.split("=", 1)
            out[line_s[0]] = line_s[1]
    return out


@log_entry_exit
def alter_locres(args: ArgsDict):
    data = open_exported_locres(args)
    to_replace = get_keys_to_alter(args["alter_keys_json_file"])
    n_data = data | to_replace
    to_save = [f"{key}={value}" for key, value in n_data.items()]
    with open(cfg.TMP_LOCRES_EXPORTED_PATH, "w") as file:
        file.writelines(to_save)


def assemble_locres(args: ArgsDict) -> None:
    command = [
        args["UE4localizationsTool_path"],
        "import",
        cfg.TMP_LOCRES_EXPORTED_PATH,
    ]
    run_subprocess(command)


def prepare_mod_structure(args: ArgsDict) -> None:
    locres_target_location = Path(
        cfg.PAK_STRUCTURE_ROOT, os.path.split(args["locres_path"])[0]
    )
    locres_target_location.mkdir(exist_ok=True, parents=True)
    copy(
        cfg.TMP_LOCRES_IMPORTED_PATH,
        os.path.join(locres_target_location, os.path.split(args["locres_path"])[1]),
    )


@log_entry_exit
def assemble_mod(args: ArgsDict, game_version: str) -> None:
    prepare_mod_structure(args)

    files = [
        str(x.relative_to(cfg.PAK_STRUCTURE_ROOT))
        for x in Path(cfg.PAK_STRUCTURE_ROOT).rglob("*.*")
    ]

    out_path = os.path.join(
        cfg.ROOT,
        str(args["output_mod_name"]).replace(
            ".pak", f"{'_v' + game_version if game_version else ''}.pak", 1
        ),
    )

    # package mod from inside mod directory, to preserve .pak structure
    wd = os.getcwd()
    os.chdir(cfg.PAK_STRUCTURE_ROOT)
    print(f"Saving mod to {out_path}")

    command = [
        "python",
        os.path.join("..", "u4pak", "u4pak.py"),
        "pack",
        out_path,
    ] + files
    run_subprocess(command)
    os.chdir(wd)


def cleanup():
    files_to_remove = [
        cfg.TMP_LOCRES_PATH,
        cfg.TMP_LOCRES_EXPORTED_PATH,
        cfg.TMP_LOCRES_IMPORTED_PATH,
    ]
    dirs_to_remove = [cfg.PAK_STRUCTURE_ROOT]
    for file in files_to_remove:
        os.remove(file)
    for dirr in dirs_to_remove:
        rmtree(dirr)


def main(args: ArgsDict) -> None:
    # open game files
    # extract .locres
    version = extract_data(args)
    disassemble_locres(args)

    # edit the .locres
    alter_locres(args)
    assemble_locres(args)

    # assemble the mod
    assemble_mod(args, version)

    cleanup()


if __name__ == "__main__":
    args: ArgsDict = {
        "pak_path": Path(
            r"D:\SteamLibrary\steamapps\common\Foxhole\War\Content\Paks\War-WindowsNoEditor.pak"
        ),
        "locres_path": Path(
            "War/Content/Localization/Foxhole-CodeStrings/en/Foxhole-CodeStrings.locres"
        ),
        "output_mod_name": "War-WindowsNoEditor_Headpats.pak",
        "alter_keys_json_file": "to_alter.json",
        "UE4localizationsTool_path": r"UE4localizationsTool.exe",
    }

    main(args)
