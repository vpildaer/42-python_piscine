import importlib
import importlib.util


def try_import() -> bool:
    res: bool = True

    modules: dict[str, str] = {"pandas": "Data manipulation",
                               "numpy": "Numerical computation",
                               "requests": "Network access",
                               "matplotlib": "Visualization"}

    for k, v in modules.items():

        if importlib.util.find_spec(k) is not None:

            try:
                mod = importlib.import_module(k)

            except ModuleNotFoundError:
                print(f"Error - {k} not found")
                res = False

            except ImportError:
                print(f"Error - {k} failed to import")
                res = False

            except AttributeError:
                print(f"Error - {k} not found")
                res = False

            else:
                if k != "requests":
                    print(f"[OK] {k} ({mod.__version__}) - "
                          f"{v} ready")

        else:
            print(f"Error - {k} not found")
            res = False

    return res


def analysis() -> None:
    from numpy import random
    import pandas
    from matplotlib import pyplot

    data = random.normal(loc=50, scale=15, size=1000)

    print("\nAnalyzing Matrix data...")

    graph = pandas.DataFrame(data)

    print(f"Processing {len(data)} data points...")

    pyplot.hist(graph, bins=30, color="hotpink", edgecolor="black")

    pyplot.xlabel("Red Flag Severity Score")

    pyplot.ylabel("Number of Text Messages")

    pyplot.title("Distribution of Red-Flagness in Young Adult Males")

    print("Generating visualization")

    pyplot.show()

    print("\nAnalysis complete!")

    try:
        pyplot.savefig("matrix_analysis.png")

    except Exception:
        print("Results not saved")
        raise

    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":

    try:
        print("\nLOADING STATUS: loading programs\n")

        if try_import():
            analysis()

        else:
            print("At least one module could not be imported successfully\n")
            print("Try again with one of these two methods:")
            print("\npython3 -m venv matrix_env")
            print("source matrix_env/bin/activate")
            print("pip install -r requirements.txt")
            print("python3 loading.py")
            print("\nor\n")
            print(" poetry install\n poetry run python loading.py")

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print("Interruption")
