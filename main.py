import time

import dotenv

from src.game import utils, state, planner, client
from src.libs import android, adb


def main():
    android.setup_screenshot_api_port_forwarding()

    if android.unlock():
        time.sleep(3)

    android.accept_tablet_data_permissions()

    # begin the loop
    while True:
        state.reset()
        planner.clear_plans_cache()

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

        # while we are still developing OCR, use this hardcoded workaround
        matches = utils.get_template_matches('game/main_menu/down_button.png')
        matches = sorted(matches, key=lambda m: m.rect.top)
        if matches:
            match = matches[0] if matches else None
            x, y = match.rect.center
            adb.tap(x, y)
            time.sleep(1)

        utils.tap_first_template_match('game/basic_level/start_game_button.png')
        time.sleep(1)

        android.tap_middle_of_screen()
        time.sleep(1)

        i = 0
        plans = planner.get_plans_for_strategy('basic_level_v1')
        for plan in plans:
            for command in plan.commands:
                client.update_tile(
                    command.row_i,
                    command.col_i,
                    command.target_tower_id
                )
                i += 1
                if i == 10:
                    client.enable_fast_forward()

        # keep checking for the game over text
        while True:
            match = utils.get_first_template_match('game/you_win_message.png')

            if match:
                time.sleep(10)
                break

            time.sleep(5)


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
