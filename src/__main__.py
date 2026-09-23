from .pipeline import main
from .gui import launch_gui
from .directories import PathConfig

if __name__ == "__main__":
    paths = PathConfig()
    # main(None, paths)        # CLI
    launch_gui(main, paths)    # GUI