import os


def oracle() -> None:

    try:
        from dotenv import load_dotenv, find_dotenv
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Module dotenv not available")

    values: dict[str, str | None] = {"matrix_mode": "",
                                     "database_url": "",
                                     "api_key": "",
                                     "log_level": "",
                                     "zion_endpoint": ""}

    init_values: dict[str, str | None] = values.copy()

    init_values["matrix_mode"] = os.getenv("MATRIX_MODE")
    init_values["database_url"] = os.getenv("DATABASE_URL")
    init_values["api_key"] = os.getenv("API_KEY")
    init_values["log_level"] = os.getenv("LOG_LEVEL")
    init_values["zion_endpoint"] = os.getenv("ZION_ENDPOINT")

    print("\nORACLE STATUS: Reading the Matrix...\n")

    is_loaded: bool = load_dotenv(override=False)

    values["matrix_mode"] = os.getenv("MATRIX_MODE", "production")
    values["database_url"] = os.getenv("DATABASE_URL")
    values["api_key"] = os.getenv("API_KEY")
    values["log_level"] = os.getenv("LOG_LEVEL", "INFO")
    values["zion_endpoint"] = os.getenv("ZION_ENDPOINT")

    if not is_loaded and all(init_values[k] is None for k in values.keys()):
        print("Error - Configuration could not be loaded")
        print("Reason: .env is missing and no env variables set")
        print("Make sure to use a .env file to load configuration")

    elif values["matrix_mode"] == "production" and values["api_key"] is None:
        print("Error - Could not load configuration for production mode")
        print("Reason: API key is missing")

    else:
        print("Configuration loaded:")
        print(f'Mode: {values["matrix_mode"]}')

        if values["database_url"] is not None:
            print("Database: Connected to local instance")
        else:
            print("Database: Could not connect to local instance")

        if (values["matrix_mode"] == "development" and
                values["api_key"] is None):
            print("Warning - API key is missing")
        else:
            print("API Access: Authenticated")

        print(f'Log Level: {values["log_level"]}')
        if (values["matrix_mode"] == "production" and
                values["log_level"] == "DEBUG"):
            print("Warning - You are using DEBUG mode for production")
            print("You should not be using this Log Level")

        if values["zion_endpoint"] is not None:
            print("Zion Network: Online")
        else:
            print("Zion Network: Offline")
            print("Warning - You are offline")

    print("")

    if find_dotenv() == "":
        print("[ERROR] No .env file found - Secrets could be hardcoded")
    else:
        print("[OK] No hardcoded secrets detected")

    if find_dotenv() != "" and is_loaded:
        print("[OK] .env file properly configured")
    else:
        print("[ERROR] .env file not configured properly")

    is_override: bool = False

    for k in init_values.keys():
        if init_values[k] is not None:
            if init_values[k] != values[k]:
                is_override = True

    if is_override:
        print("[ERROR] - Production overrides unavailable")
    else:
        print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    try:
        oracle()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("Interruption")
