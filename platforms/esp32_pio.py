import os
from common import get_target_dir, create_directory, create_file

def get_esp_target_choice() -> str:
    """
    Polls the user for their target ESP chip and validates the input.
    """
    targets = {
        "1": "esp32",    # The classic dual-core
        "2": "esp32s2",  # Single-core, USB OTG
        "3": "esp32s3",  # Dual-core, AI instructions, very popular
        "4": "esp32c3",  # RISC-V single-core
        "5": "esp32c6"   # RISC-V with Wi-Fi 6
    }
    
    print("\n⚡ Select your target ESP32 chip:")
    for key, name in targets.items():
        print(f"   {key}) {name}")
        
    while True:
        # ESP32-S3 is a great modern default
        choice = input("Enter a number [default 3 (esp32s3)]: ").strip()
        if not choice:
            return "esp32s3"
        if choice in targets:
            return targets[choice]
        print("❌ Invalid choice. Please enter 1-5.")

def set_dotclangd(root_dir:str):
    clangd_template="""
#credit to https://github.com/ironlungx/nvim-pio/blob/main/.clangd
CompileFlags:
  Add: [
    -DSSIZE_MAX,
    -DLWIP_NO_UNISTD_H=1,
    -Dssize_t=long,
    -D_SSIZE_T_DECLARED,
    -Wno-unknown-warning-option
  ]
  Remove: [
    -mlong-calls,
    -fno-tree-switch-conversion,
    -mtext-section-literals,
    -mlongcalls,
    -fstrict-volatile-bitfields,
    -free,
    -fipa-pta,
    -march=*,
    -mabi=*,
    -mcpu=*
  ]
Diagnostics:
  Suppress:
    - pp_including_mainfile_in_preamble
    - pp_expr_bad_token_start_expr
    - redefinition_different_typedef
    - main_returns_nonint
    """
    written_chars = create_file(os.path.join(root_dir, ".clangd"))
    return written_chars
    
def get_framework_choice() -> list[ str ]:
    """
    Polls the user for their preferred PlatformIO framework and validates the input.
    """
    frameworks = {
        "1": "arduino",
        "2": "espidf",
        "3": "zephyr"
    }
    print("\n🔧 Select your PlatformIO framework:")
    for key, name in frameworks.items():
        print(f"   {key}) {name}")
    while True:
        choice = input("Enter a number [default 2 (espidf)]: ").strip()
        if not choice:
            return ["espidf"]
        selected = [c.strip() for c in choice.split(",")]
        valid: list[str] = [frameworks[c] for c in selected if c in frameworks]
        if valid and len(valid) == len(selected):
            return valid
        print("❌ Invalid choice. Please enter 1-3.")

def generate_platformio_ini(root_dir: str, frameworks: list[str], target_chip: str) -> None:
    """
    Generates a platformio.ini file based on selected frameworks and target chip.
    """
    framework_str = ", ".join(frameworks)
    ini_content = (
        f"[env:{target_chip}]\n"
        f"platform = espressif32\n"
        f"board = {target_chip}\n"
        f"framework = {framework_str}\n"
    )
    _ = create_file(os.path.join(root_dir, "platformio.ini"), ini_content)

def setup(project_name: str) -> None:
    target_chip = get_esp_target_choice()
    
    #setup the directory structure for platformio
    root = get_target_dir(project_name)
    create_directory(root)
    create_directory(os.path.join(root, "src"))
    create_directory(os.path.join(root, "include"))
    create_directory(os.path.join(root, "lib"))

    resp = input("Generate .clangd file for LSP support? [y/N]: ").strip().lower()
    if resp == "y":
        _ = set_dotclangd(root)
        print("✅ .clangd file created for LSP support.")

    frameworks = get_framework_choice()
    generate_platformio_ini(root, frameworks,target_chip)
    print(f"✅ platformio.ini created with frameworks: {', '.join(frameworks)} for target chip: {target_chip}.")

