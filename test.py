import time

from src.game import vision, controls
from src.libs import android


def main():
    android.setup_screenshot_api_port_forwarding()
    controls.tap_game_icon()
    time.sleep(1)
    controls.tap_new_game_button()
    time.sleep(1)
    controls.tap_start_game_button()
    time.sleep(1)



if __name__ == "__main__":
    main()
