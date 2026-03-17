import argparse
import sys
# import the platform modules
from platforms import pico, esp32_idf, esp32_pio

SUPPORTED_PLATFORMS = {
        'pico': pico.setup,
        'esp32_idf': esp32_idf.setup, # esp32 is considered as esp-idf
        'esp32_pio': esp32_pio.setup
        }

def main():
    parser = argparse.ArgumentParser(description='Setup the development environment for the specified platform.',
                                     epilog='Example usage: lazyembed <platform> <project_name>')
    _ = parser.add_argument('platform', choices=SUPPORTED_PLATFORMS.keys(), help='The target platform to set up (e.g., pico, esp32_idf, esp32_pio).')
    _ = parser.add_argument('project_name', help='The name of the project to create.')
    args = parser.parse_args()

    try:
        SUPPORTED_PLATFORMS[args.platform](args.project_name) #pyright: ignore
        print(f"Successfully set up the development environment for {args.platform} with project name '{args.project_name}'.") #pyright: ignore
    except Exception as e:
        print(f"Error setting up the development environment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

