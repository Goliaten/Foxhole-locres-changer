# Foxhole Locres Changer

# Usage
This project uses a submodule. To properly clone it use:
```
git clone --recurse-submodules https://github.com/Goliaten/Foxhole-locres-changer.git
```

## Changing locres keys
Change keys that you'd want altered in `to_alter.json`. Keys have to include namespace before them.
If value of keys won't have `\n` at the end, the script will add it. It's like that so later on the locres is properly saved.

# Script parameters
## For Foxhole
In order for the script to work properly, change these values in `config.py`
- `pak_path` - points to the location of `War-WindowsNoEditor.pak` - main .pak file of the game
Optionally you can change these:
- `output_mod_name` - what the output name of the file should be.
- `locres_path` - if you want to edit other localization file, or for other language. It's a path to the .locres file within game's .pak file
## For other games
For other games to work correctly, it is recommended to change the following keys:
- `pak_path` - path to the `.pak` file in a game
- `LOCRES_PATH` - path to the `.locres` file within the `.pak` file
- `DEFAULT_GAME_PATH` - path to a `.ini` file in the `.pak` file containing a `ProjectVersion` key, which represents version of the application.

If you the game doesnt have such file, or you don't want to have game version in output file, pass `--dont_add_version` in command line when executing the script.

## Full list
### PAK_PATH
Points to the location of the `.pak` file, which this script will open.

By default it takes value from `config.py` script, `PAK_PATH` constant.
Value can also be supplied as a command line parameter `--pak_path PAK_PATH` or `-p PAK_PATH`.
### LOCRES_PATH
Points to the location of the `.locres` file within the `.pak` file.

By default it takes value from `config.py` script, `LOCRES_PATH` constant.
Value can also be supplied as a command line parameter `--locres_path LOCRES_PATH` or `-l LOCRES_PATH`.
### OUTPUT_MOD_NAME
Name of the assembled mod. This can also be a path with name to a separate directory.
By default game version is appended to the end of the name. This can be disabled with `--dont_add_version` command line flag.

By default it takes value from `config.py` script, `OUTPUT_MOD_NAME` constant.
Value can also be supplied as a command line parameter `--output_mod_name OUTPUT_MOD_NAME` or `-o OUTPUT_MOD_NAME`.
### ALTER_KEYS_JSON_FILE
Path to a .json file containing keys to change with their new values. Refer to [Changing locres keys](#changing-locres-keys) section for information on the file itself.

By default it takes value from `config.py` script, `ALTER_KEYS_JSON_FILE` constant.
Value can also be supplied as a command line parameter `--alter_keys_json_file ALTER_KEYS_JSON_FILE` or `-a ALTER_KEYS_JSON_FILE`.
### UE4_LOCALIZATIONS_TOOL_PATH
Points to the UE4localizationsTool executable. It should be included in this repository, but if you'd rather use your own version, it can be changed with this.

By default it takes value from `config.py` script, `UE4_LOCALIZATIONS_TOOL_PATH` constant.
Value can also be supplied as a command line parameter `--UE4localizationsTool_path UE4_LOCALIZATIONS_TOOL_PATH`.
### DEFAULT_GAME_PATH
Path within the .pak file, pointing at .ini file containing ProjectVersion key with game version. Used in appending game version to the assembled mod name.

By default it takes value from `config.py` script, `DEFAULT_GAME_PATH` constant.
Value can also be supplied as a command line parameter `--default_game_path DEFAULT_GAME_PATH`.
### dont_add_version
Flag that disables adding game version to the output filename.

To set, pass `--dont_add_version` to the command line. Example: `python main.py --dont_add_version`

## Running
Install required packages via `pip` or `uv`, and then run the script:
```
python main.py
    [-h]
    [--pak_path PAK_PATH]
    [--locres_path LOCRES_PATH]
    [--output_mod_name OUTPUT_MOD_NAME]
    [--alter_keys_json_file ALTER_KEYS_JSON_FILE]
    [--UE4localizationsTool_path UE4LOCALIZATIONSTOOL_PATH]
    [--default_game_path DEFAULT_GAME_PATH]
    [--dont_add_version]
```

# Tools used in this script
- [UE4LocalizationsTool](https://github.com/amrshaheen61/UE4LocalizationsTool/tree/master) (included in this repo)
- [u4pak](https://github.com/panzi/u4pak) (included as submodule)

# TODO
- [ ] check behaviour when executed from non project root directory

