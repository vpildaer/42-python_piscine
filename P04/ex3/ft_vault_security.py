#!/usr/bin/env python3

def secure_archive(name: str, mode: str = "r", content: str = "") \
                   -> tuple[bool, str]:
    try:
        with open(name, mode) as file:
            if mode == "r":
                return (True, file.read())
            elif mode == "w":
                file.write(content)
                return (True, 'Content successfully written to file')
            else:
                return (False, f"Unsupported mode: {mode}")
    except FileNotFoundError as e:
        return (False, f"{e}")
    except PermissionError as e:
        return (False, f"{e}")
    except Exception as e:
        return (False, f"{e}")


if __name__ == "__main__":
    print("=== Cyber Archives Security ===\n")
    print("Using 'secure_archive' to read from a non existent file:")
    print(f"""{secure_archive("nofile.txt", "r")}""")
    print("")
    print("Using 'secure_archive' to read from an inaccessible file:")
    print(f"""{secure_archive("noaccess.txt", "r")}""")
    print("")
    print("Using 'secure_archive' to read from a regular file:")
    print(f"""{secure_archive("ancient_fragment.txt", "r")}""")
    print("")
    result: bool
    data: str
    result, data = secure_archive("ancient_fragment.txt", "r")
    print("Using 'secure_archive' to write previous content to a new file:")
    print(f"""{secure_archive("new_file.txt", "w", data)}""")
