from db import setup_database
from ui.windows import create_main_window

if __name__ == "__main__":
    setup_database()
    create_main_window()
