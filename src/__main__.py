from .pipeline import main
from .gui import launch_gui

if __name__ == "__main__":
    # main(None)        # CLI
    launch_gui(main)    # GUI