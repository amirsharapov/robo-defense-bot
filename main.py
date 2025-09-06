import time

import dotenv

from src.game import utils
from src.libs import android, adb
from src.scripts.play_basic_level import place_towers_for_basic_level


def main():
    android.setup_screenshot_api_port_forwarding()
    if android.unlock():
        time.sleep(3)
    android.accept_tablet_data_permissions()

    # begin the loop
    while True:
        android.go_back()
        # android.go_to_home_screen()
        time.sleep(1)

        adb.send_monkey_event('com.magicwach.rdefense', 'android.intent.category.LAUNCHER', 1)
        time.sleep(1)

        # start the new game
        utils.tap_first_template_match('game/main_menu/new_game_button.png')
        time.sleep(1)

        # confirm starting over if needed
        template_prefix = 'game/main_menu/prompts/discard_game_and_start_over/'

        if utils.get_first_template_match(template_prefix + 'prompt_v1.png'):
            utils.tap_first_template_match(template_prefix + 'yes_button_v1.png')
            time.sleep(1)

        if utils.get_first_template_match(template_prefix + 'prompt_v2.png'):
            utils.tap_first_template_match(template_prefix + 'yes_button_v2.png')
            time.sleep(1)

        # skipping this for now
        # game.set_difficulty_level(5)
        # time.sleep(1)

        utils.tap_first_template_match('game/basic_level/start_game_button.png')
        time.sleep(1)

        android.tap_middle_of_screen()
        time.sleep(1)

        place_towers_for_basic_level()

        # keep checking for the game over text
        while True:
            match = utils.get_first_template_match('game/you_win_message.png')

            if match:
                break

            time.sleep(5)


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
