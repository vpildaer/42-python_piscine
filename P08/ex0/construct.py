import sys
import os
import site


def construct() -> None:
    is_not_venv: bool = (sys.prefix == sys.base_prefix)
    if is_not_venv:
        print("\nMATRIX STATUS: You're still plugged in\n")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected\n")
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print(r"matrix_env\Scripts\activate # On Windows")
        print("")
        print("Then run this program again.")
    else:
        print("\nMATRIX STATUS: Welcome to the construct\n")
        print(f"Current Python: {sys.executable}")
        path: str = os.path.basename(sys.prefix)
        print(f"Virtual Environment: {path}")
        print(f"Environment Path: {sys.prefix}\n")
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.\n")
        print("Package installation path:")
        try:
            print(site.getsitepackages()[0])
        except AttributeError:
            print("Package installation path: unavailable")


if __name__ == "__main__":
    construct()
