import argparse
import sys
# import the platform modules
from platforms import pico, esp32

SUPPORTED_PLATFORMS = {
        'pico': pico.setup,
        'esp32': esp32.setup # esp32 is considered as esp-idf
        }

def main():
    parser = argparse.ArgumentParser(description='Setup the development environment for the specified platform.',
                                     epilog='Example usage: lazyembed <platform> <project_name>')
    parser.add_argument('platform', choices=SUPPORTED_PLATFORMS.keys(), help='The target platform to set up (e.g., pico, esp32).')
    parser.add_argument('project_name', help='The name of the project to create.')
    args = parser.parse_args()

    try:
        SUPPORTED_PLATFORMS[args.platform](args.project_name)
        print(f"Successfully set up the development environment for {args.platform} with project name '{args.project_name}'.")
    except Exception as e:
        print(f"Error setting up the development environment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

