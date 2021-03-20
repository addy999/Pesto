import os
import coverage
import typer
import webbrowser

from .src.runner import *

app = typer.Typer()


@app.command()
def main(
    dir: str = typer.Argument(
        "./", help="Directory containing tests, named with *tests*.py pattern."
    ),
    cov: bool = typer.Option(
        False, "-c", show_default=False, help="Generate code coverage for tests."
    ),
    cov_dir: str = typer.Option(
        "./cov", "--cov-dir", help="Output coverage html report directory."
    ),
    open_cov: bool = typer.Option(
        False,
        "--open-cov",
        show_default=False,
        help="Weather to open browser and show generated coverage. Sets cov to True as well.",
    ),
    watch: bool = typer.Option(
        False,
        "-w",
        show_default=False,
        help="Watch file changes and re-run tests live.",
    ),
):

    main_runner(dir, cov, cov_dir, open_cov)

    if watch:
        start_watcher(lambda: main_runner(dir, cov, cov_dir, open_cov=False), dir)


def main_runner(dir: str, cov: bool, cov_dir: str, open_cov: bool):

    print("\033c\033[3J", end="")

    if cov or open_cov:

        cov = coverage.Coverage(source=[os.path.abspath(dir)], omit=["**/__init__.py"])
        cov.start()

    test_files = find_test_files(dir)
    test_suites = []
    for test_file in test_files:
        test_suites += find_test_suite(os.path.join(os.getcwd(), test_file))

    run_test_suites(test_suites)

    if cov or open_cov:
        cov.stop()
        cov.save()
        cov.html_report(directory=cov_dir)
        if open_cov:
            webbrowser.open("http://0.0.0.0:8000/")
            os.system(f"cd {cov_dir} && python3 -m http.server")


# if __name__ == "__main__":

#     typer.run(main)
