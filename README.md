# Foxhole Locres Changer

# Usage
This project uses a submodule. To properly clone it use:
```
git clone --recurse-submodules https://github.com/Goliaten/Foxhole-locres-changer.git 
```

## Changing locres keys
Change keys that you'd want altered in `to_alter.json`. Keys have to include namespace before them.
If value of keys won't have `\n` at the end, the script will add it. It's like that so later on the locres is properly saved.

## Script parameters
### For Foxhole
In order for the script to work properly, change these values in `config.py`
- `pak_path` - points to the location of `War-WindowsNoEditor.pak` - main .pak file of the game
Optionally you can change these:
- `output_mod_name` - what the output name of the file should be.
- `locres_path` - if you want to edit other localization file, or for other language. It's a path to the .locres file within game's .pak file
### For other games
For other games to work correctly, it is recommended to change the following keys:
- `pak_path` - path to the `.pak` file in a game
- `LOCRES_PATH` - path to the `.locres` file within the `.pak` file
- `DEFAULT_GAME_PATH` - path to a `.ini` file in the `.pak` file containing a `ProjectVersion` key, which represents version of the application.

If you the game doesnt have such file, or you don't want to have game version in output file, pass `--dont_add_version` in command line when executing the script.

## Running
Install required packages via `pip` or `uv`, and then run the script:
```
python main.py
```

# Tools used in this script
- [UE4LocalizationsTool](https://github.com/amrshaheen61/UE4LocalizationsTool/tree/master) (included in this repo)
- [u4pak](https://github.com/panzi/u4pak) (included as submodule)

# TODO
- [ ] check behaviour when executed from non project root directory

