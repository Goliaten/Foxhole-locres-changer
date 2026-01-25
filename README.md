# Foxhole Locres Changer

## Usage
### Changing locres keys
Change keys that you'd want altered in `to_alter.json`. Keys have to include namespace before them.
If value of keys won't have `\n` at the end, the script will add it. It's like that so later on the locres is properly saved.

### Script parameters
In order for the script to work properly, change these values in `main.py`
- `pak_path` - points to the location of `War-WindowsNoEditor.pak` - main .pak file of the game
Optionally you can change these:
- `output_mod_name` - what the output name of the file should be.
- `locres_path` - if you want to edit other localization file, or for other language. It's a path to the .locres file within game's .pak file

### Running
Install required packages via `pip` or `uv`, and then run the script:
```
python main.py
```

## Tools used in this script
- [UE4LocalizationsTool](https://github.com/amrshaheen61/UE4LocalizationsTool/tree/master) (included in this repo)
- [u4pak](https://github.com/panzi/u4pak) (included as submodule)

# TODO
- [ ] move `args` from main.py into separate `params.json` or into argparse
- [ ] move static variables in from main.py into separate `config.py`

