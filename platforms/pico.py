from ast import main
from enum import pickle_by_global_name
from functools import total_ordering
import os
import shutil
from common import get_env_var, get_target_dir, create_directory, create_file
def get_board_choice() -> str:
    """
    Prompts the user to select a board from a predefined list of supported boards and returns the selected board.
    """
    supported_boards = ['pico', 'pico_w', 'pico_2', 'pico_2w']
    print("Supported boards:")
    for idx, board in enumerate(supported_boards, start=1):
        print(f"{idx}. {board}")
    
    while True:
        choice = input("Select a board by entering the corresponding number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(supported_boards):
            return supported_boards[int(choice) - 1]
        else:
            print("Invalid choice. Please enter a valid number corresponding to the board.")

def setup(project_name: str) -> None:
    """
    Sets up the development environment for the Raspberry Pi Pico platform by creating a project directory and populating it with template files.
    """
    target_dir = get_target_dir(project_name)

    create_directory(target_dir)

    pico_sdk_path = get_env_var('PICO_SDK_PATH')
    import_cmake_src = os.path.join(pico_sdk_path, 'external/pico_sdk_import.cmake')
    if not os.path.isfile(import_cmake_src):
        raise FileNotFoundError(f"Could not find pico_sdk_import.cmake at {import_cmake_src}. Please ensure PICO_SDK_PATH is set correctly.")

    ### We will create all the necessary files for a basic Raspberry Pi Pico project
    DIRS_TO_CREATE = {
            "src_dir ": os.path.join(target_dir, 'src'),
            "inc_dir ": os.path.join(target_dir, 'inc'),
            "lib_dir ": os.path.join(target_dir, 'lib')
            }
    FILES_TO_CREATE = {
            "CMakeLists.txt": os.path.join(target_dir, 'CMakeLists.txt'),
            "main.c": os.path.join(DIRS_TO_CREATE['src_dir '], 'main.c'),
            "pico_sdk_import.cmake": os.path.join(target_dir, 'pico_sdk_import.cmake')
            }

    for _, dir_path in DIRS_TO_CREATE.items():
        create_directory(dir_path)
        print(f"Created directory: {dir_path}")

    board_choice = get_board_choice()
    cmake_content = f"""
cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)
project({project_name} LANGUAGES C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(PICO_BOARD {board_choice})
pico_sdk_init()
add_executable({project_name})
target_sources({project_name} PRIVATE 
    src/main.c
)
target_include_directories({project_name} PRIVATE 
    inc
)
target_link_libraries({project_name} PRIVATE 
    pico_stdlib
)
pico_enable_stdio_usb({project_name} 1)
pico_enable_stdio_uart({project_name} 0)
pico_add_extra_outputs({project_name})
            """
    main_c_content = """
#include <stdio.h>
#include "pico/stdlib.h"

int main(void) {
    stdio_init_all();
    while (true) {
        printf("Hello, Raspberry Pi Pico!\\n");
        sleep_ms(1000);
    }
    return 0;
}
    """
    _ = shutil.copy(import_cmake_src, FILES_TO_CREATE["pico_sdk_import.cmake"])
    print(f"Copied pico_sdk_import.cmake from {import_cmake_src} to {FILES_TO_CREATE['pico_sdk_import.cmake']}")

    cmake_chars = create_file(FILES_TO_CREATE["CMakeLists.txt"], cmake_content)
    print(f"Created file: CMakeLists.txt with content for {board_choice}")

    main_chars = create_file(FILES_TO_CREATE['main.c'], main_c_content)
    print(f"Created file: main.c")
    
    total_chars = cmake_chars + main_chars
    print(f"\nSuccessfully set up the Raspberry Pi Pico development environment!\n{total_chars} characters written across all files.")
