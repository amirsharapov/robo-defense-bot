import time

import dotenv

from src.libs import android, adb
from src.game import client as game, controls
from src.scripts.play_basic_level import place_towers_for_basic_level


def main():
    android.setup_screenshot_api_port_forwarding()
    android.unlock()
    time.sleep(3)
    android.accept_tablet_data_permissions()

    # begin the loop
    while True:
        android.go_to_home_screen()
        adb.send_monkey_event('com.magicwach.rdefense', 'android.intent.category.LAUNCHER', 1)
        time.sleep(1)

        # start the new game
        controls.tap_new_game_button()

        # game.confirm_start_over_prompt()
        # game.set_difficulty_level(5)

        time.sleep(1)


        controls.tap_start_game_button()
        time.sleep(1)

        controls.tap_middle_of_screen()
        time.sleep(1)

        place_towers_for_basic_level()

        while True:
            # keep checking for the game over text
            pass


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
