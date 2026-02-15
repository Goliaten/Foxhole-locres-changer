import os

PAK_PATH = (
    r"D:\SteamLibrary\steamapps\common\Foxhole\War\Content\Paks\War-WindowsNoEditor.pak"
)
LOCRES_PATH = (
    r"War/Content/Localization/Foxhole-CodeStrings/en/Foxhole-CodeStrings.locres"
)
OUTPUT_MOD_NAME = r"War-WindowsNoEditor_Headpats.pak"
ALTER_KEYS_JSON_FILE = r"to_alter.json"
# UE4_LOCALIZATIONS_TOOL_PATH = r"UE4localizationsTool.exe"

TMP_LOCRES_FILE = "tmp.locres"
TMP_LOCRES_EXPORTED = TMP_LOCRES_FILE + ".txt"
TMP_LOCRES_IMPORTED = TMP_LOCRES_FILE.replace(".", "_NEW.", 1)
ROOT = os.path.split(__file__)[0]
TMP_LOCRES_PATH = os.path.join(ROOT, TMP_LOCRES_FILE)
TMP_LOCRES_EXPORTED_PATH = os.path.join(ROOT, TMP_LOCRES_EXPORTED)
TMP_LOCRES_IMPORTED_PATH = os.path.join(ROOT, TMP_LOCRES_IMPORTED)
PAK_STRUCTURE_ROOT = "archive"
DEFAULT_GAME_PATH = "War/Config/DefaultGame.ini"
