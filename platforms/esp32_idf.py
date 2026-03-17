import os
from common import get_target_dir, create_directory, create_file, get_env_var

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

def setup(project_name: str) -> None:
    # 1. Verify the IDF environment is active (Fails fast if missing)
    # Note: On ESP-IDF, users usually run 'export.sh' or 'export.bat' to set this.
    idf_path = get_env_var("IDF_PATH")
    
    # 2. Poll the user for the chip version
    target_chip = get_esp_target_choice()
    
    # 3. Set up the ESP-IDF directory structure
    root = get_target_dir(project_name)
    create_directory(root)
    create_directory(os.path.join(root, "main"))
    
    # 4. Generate the Root CMakeLists.txt
    root_cmake = f"""
cmake_minimum_required(VERSION 3.16)

# Include the core ESP-IDF build system
include($ENV{{IDF_PATH}}/tools/cmake/project.cmake)

project({project_name})
"""

    # 5. Generate the Component CMakeLists.txt (Inside the 'main' folder)
    # This registers your source files and header directories
    main_cmake = """
idf_component_register(SRCS "main.c"
                       INCLUDE_DIRS ".")
"""

    # 6. Generate sdkconfig.defaults to lock in the target chip
    # This saves the user from having to run `idf.py set-target <chip>`
    sdkconfig_content = f'CONFIG_IDF_TARGET="{target_chip}"\n'

    # 7. Generate a strict main.c using FreeRTOS and ESP_LOG
    main_content = f"""
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"

static const char *TAG = "{project_name}";

void app_main(void) {{
    ESP_LOGI(TAG, "Hardware initialized on target: %s", CONFIG_IDF_TARGET);

    while (1) {{
        ESP_LOGI(TAG, "Tick...");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }}
}}
"""

    # 8. Write and verify all files
    root_chars = create_file(os.path.join(root, "CMakeLists.txt"), root_cmake)
    main_cmake_chars = create_file(os.path.join(root, "main", "CMakeLists.txt"), main_cmake)
    sdk_chars = create_file(os.path.join(root, "sdkconfig.defaults"), sdkconfig_content)
    main_c_chars = create_file(os.path.join(root, "main", "main.c"), main_content)

    total_chars = root_chars + main_cmake_chars + sdk_chars + main_c_chars

    print(f"\n✔️  ESP-IDF project '{project_name}' successfully generated for '{target_chip}'! ({total_chars} chars written)")
    print(f"🚀  Next steps: cd {project_name} && idf.py build && idf.py flash monitor")
