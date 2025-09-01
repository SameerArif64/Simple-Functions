from re import sub
from sys import path as sys_path
from time import sleep
from pathlib import Path
from os import startfile
from typing import List
from winsound import Beep
from importlib import util
from pynput.mouse import Listener

def get_mouse_coordinates():
    def on_click(x, y, button, pressed):
        # Check if left button is pressed
        if button.name == 'left' and pressed:
            print(f"Mouse clicked at ({x}, {y})")
        
        # Check if right button is pressed to stop the listener
        if button.name == 'right' and pressed:
            print("Right click detected. Exiting program.")
            return False  # This stops the listener and ends the program

    # Start listener to monitor mouse events
    with Listener(on_click=on_click) as listener:
        listener.join()

def import_from_file(file_path: Path, attribute_name: str = None):
    """
    Dynamically imports a module or specific attribute (class, function, variable) from a Python file.
    Resolves internal dependencies automatically.

    :param file_path: Path to the Python file.
    :param attribute_name: The name of the attribute to import. If None, returns the entire module.
    :return: The imported module or attribute.
    :raises FileNotFoundError: If the file does not exist.
    :raises ImportError: If the module cannot be loaded.
    :raises AttributeError: If the specified attribute does not exist.
    """
    file_path = Path(file_path)
    # Ensure the file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Resolve the absolute path and parent directory
    file_path = file_path.resolve()
    parent_dir = str(file_path.parent)

    # Temporarily add the parent directory to sys_path for dependency resolution
    if parent_dir not in sys_path:
        sys_path.insert(0, parent_dir)

    try:
        # Load the module dynamically
        module_name = file_path.stem  # Use the file name without the extension
        spec = util.spec_from_file_location(module_name, str(file_path))
        if spec is None:
            raise ImportError(f"Could not create a module spec for: {file_path}")
        
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Return the module if no specific attribute is requested
        if not attribute_name:
            return module

        # Retrieve the requested attribute
        if hasattr(module, attribute_name):
            return getattr(module, attribute_name)
        else:
            raise AttributeError(f"Module '{module_name}' has no attribute '{attribute_name}'")

    finally:
        # Clean up sys_path to avoid polluting the global environment
        if parent_dir in sys_path:
            sys_path.remove(parent_dir)

def open_file(file_path: Path):
    """Open a file using the default application."""
    startfile(file_path)

def wait_for_file_availability(file_path: Path, notify_only: bool = False, wait_time: int = 600, wait_interval: int = 3) -> bool:
    """
    Wait until a file becomes available for read/write access.

    Args:
        file_path (Path): Path to the file to check.
        notify_only (bool): If True, return immediately if the file is unavailable.
        wait_time (int): Maximum time (in seconds) to wait for the file to become available.
        wait_interval (int): Interval (in seconds) between checks.

    Returns:
        bool: True if the file is available, False if notify_only is True and the file is unavailable.

    Raises:
        TimeoutError: If the file is not available within the specified wait_time.
    """
    error_displayed = False  # Tracks if the error message has already been displayed

    if not file_path.exists():
        print(f"Error: The file '{file_path}' does not exist.")
        return True

    while True:
    # for _ in range(0, wait_time, wait_interval):
        try:
            with open(file_path, 'r+'):  # Attempt to open the file in read/write mode
                if error_displayed:
                    print(f"The file '{file_path}' is now available.")
                return True
        except IOError:
            if notify_only:
                return False
            if not error_displayed:
                Beep(500, 1000)  # Play a beep sound
                print(f"Warning: The file '{file_path}' is currently in use. Please close it to proceed.")
                error_displayed = True
            sleep(wait_interval)  # Wait before retrying
    # else:
    #     print(f"Error: The file '{file_path}' was not closed within the specified wait time ({wait_time} seconds).")
    #     raise TimeoutError(f"The file '{file_path}' is still in use after {wait_time} seconds.")

def remove_special_characters(input_string: str, lower: bool = True) -> str:
    """Remove special characters from a string."""
    output_string = sub(r'[^a-zA-Z0-9]', '', str(input_string))
    if lower:
        return output_string.lower()
    else:
        return output_string

def print_directory_tree(startpath: Path, indent: str = "", exclude: List[str] | None = None) -> None:
    """
    Recursively print a directory tree structure.

    Args:
        startpath (Path): The root directory path to start printing from.
        indent (str, optional): Indentation string used for nested levels. Defaults to "".
        exclude (list[str], optional): Filenames or directory names to exclude. Defaults to [].

    Example:
        >>> from pathlib import Path
        >>> print_tree(Path("."), exclude=[".git", "__pycache__"])
    """
    if exclude is None:
        exclude = []

    items = sorted(
        (item for item in startpath.iterdir()),
        key=lambda x: (x.is_file(), x.name.lower())
    )

    for i, item in enumerate(items):
        connector = "└── " if i == len(items) - 1 else "├── "
        print(indent + connector + item.name)

        if item.is_dir() and item.name not in exclude:
            extension = "    " if i == len(items) - 1 else "│   "
            print_directory_tree(item, indent + extension, exclude)
