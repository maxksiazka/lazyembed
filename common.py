import os

def get_target_dir(project_name: str) -> str:
    """
    Combines the user's current working directory with the provided project name to create a full path for the target directory.
    This function ensures that the project will be created in the current working directory under the specified project name.
    """
    return os.path.join(os.getcwd(), project_name)

def create_directory(path: str) -> None:
    """
    Creates a directory at the specified path
    """
    os.makedirs(path, exist_ok=True)

def create_file(path: str, content: str = "") -> int:
    """
    Creates a file at the specified path with the given content.
    If the file already exists, it will overwrite it with the new content.
    """
    final_content = content.strip() + "\n"
    expected_chars = len(final_content)
    with open(path, 'w', encoding='utf-8') as f:
        written_chars = f.write(final_content)

    # Verification
    if expected_chars != written_chars:
        raise IOError(f"File write error: expected {expected_chars} bytes, but got {written_chars} bytes.")


    return written_chars
