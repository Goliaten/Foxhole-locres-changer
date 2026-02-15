import argparse
import json
from shutil import copy, rmtree
from typing import Dict, List
import config as cfg
import pyuepak as pk
from pathlib import Path
import os
import subprocess


def log_entry_exit(func):
    def wrapper(*args, **kwargs):
        print(f"Entering: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Exiting : {func.__name__}")
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


@log_entry_exit
def get_game_version(pak: pk.PakFile, args: argparse.Namespace) -> str:
    if args.dont_add_version:
        print("Version disabled by --dont_add_version")
        return ""
    data = pak.read_file(cfg.DEFAULT_GAME_PATH)
    data = data.decode().split("\r\n")
    for x in data:
        if "ProjectVersion" in x:
            return x.split("=")[1]
    return ""


@log_entry_exit
def extract_data(args: argparse.Namespace) -> str:
    pak = pk.PakFile()
    pak.read(args.pak_path)
    extract_package(pak, args.locres_path, cfg.TMP_LOCRES_PATH)
    return pak


@log_entry_exit
def disassemble_locres(args: argparse.Namespace):
    command = [
        args.UE4localizationsTool_path,
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


def open_exported_locres(args: argparse.Namespace) -> Dict[str, str]:
    out: Dict[str, str] = {}
    with open(cfg.TMP_LOCRES_EXPORTED_PATH, "r") as file:
        while line := file.readline():
            line_s = line.split("=", 1)
            out[line_s[0]] = line_s[1]
    return out


@log_entry_exit
def alter_locres(args: argparse.Namespace):
    data = open_exported_locres(args)
    to_replace = get_keys_to_alter(args.alter_keys_json_file)
    n_data = data | to_replace
    to_save = [f"{key}={value}" for key, value in n_data.items()]
    with open(cfg.TMP_LOCRES_EXPORTED_PATH, "w") as file:
        file.writelines(to_save)


@log_entry_exit
def assemble_locres(args: argparse.Namespace) -> None:
    command = [
        args.UE4localizationsTool_path,
        "import",
        cfg.TMP_LOCRES_EXPORTED_PATH,
    ]
    run_subprocess(command)


def prepare_mod_structure(args: argparse.Namespace) -> None:
    locres_target_location = Path(
        cfg.PAK_STRUCTURE_ROOT, os.path.split(args.locres_path)[0]
    )
    locres_target_location.mkdir(exist_ok=True, parents=True)
    copy(
        cfg.TMP_LOCRES_IMPORTED_PATH,
        os.path.join(locres_target_location, os.path.split(args.locres_path)[1]),
    )


@log_entry_exit
def assemble_mod(args: argparse.Namespace, game_version: str) -> None:
    prepare_mod_structure(args)

    files = [
        str(x.relative_to(cfg.PAK_STRUCTURE_ROOT))
        for x in Path(cfg.PAK_STRUCTURE_ROOT).rglob("*.*")
    ]

    out_path = os.path.join(
        cfg.ROOT,
        str(args.output_mod_name).replace(
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


def main(args: argparse.Namespace) -> None:
    # open game files
    # extract .locres
    pak = extract_data(args)
    version = get_game_version(pak, args)
    disassemble_locres(args)

    # edit the .locres
    alter_locres(args)
    assemble_locres(args)

    # assemble the mod
    assemble_mod(args, version)

    cleanup()


def setup() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Locres changer",
        description="Script used to alter .locres files in Unreal Engine game. "
        "Designed for Foxhole, a UE 4.24 game.",
    )
    parser.add_argument(
        "--pak_path",
        "-p",
        type=str,
        help="Path to .pak file of the game",
        default=cfg.PAK_PATH,
    )
    parser.add_argument(
        "--locres_path",
        "-l",
        type=str,
        help="Path within the .pak file, pointing to .locres file",
        default=cfg.LOCRES_PATH,
    )
    parser.add_argument(
        "--output_mod_name",
        "-o",
        type=str,
        help="Filename of output file.",
        default=cfg.OUTPUT_MOD_NAME,
    )
    parser.add_argument(
        "--alter_keys_json_file",
        "-a",
        type=str,
        help="Path to .json file containing keys to change in .locres.",
        default=cfg.ALTER_KEYS_JSON_FILE,
    )
    parser.add_argument(
        "--UE4localizationsTool_path",
        type=str,
        help="Path to UE4localizationsTool.exe",
        default=cfg.UE4_LOCALIZATIONS_TOOL_PATH,
    )
    parser.add_argument(
        "--default_game_path",
        type=str,
        help="Path within the .pak file, pointing at .ini file containing ProjectVersion key with game version.",
        default=cfg.DEFAULT_GAME_PATH,
    )
    parser.add_argument(
        "--dont_add_version",
        help="Don't add game version to the output filename.",
        action="store_true",
    )

    return parser


if __name__ == "__main__":
    old_cwd = os.getcwd()
    os.chdir(os.path.split(__file__)[0])
    try:
        main(setup().parse_args())
    except Exception:
        import traceback

        traceback.print_exc()
    os.chdir(old_cwd)
