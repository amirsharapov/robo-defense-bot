import time

import dotenv

from src.game import utils, state, planner, client
from src.libs import android, adb


def main():
    android.setup_screenshot_api_port_forwarding()
    time.sleep(1)

    if android.unlock():
        time.sleep(3)

    android.accept_tablet_data_permissions()
    time.sleep(1)

    # begin the loop
    while True:
        try:
            start = time.time()

            state.reset()
            planner.clear_plans_cache()

            android.go_back()
            time.sleep(1)

            adb.send_monkey_event('com.magicwach.rdefense', 'android.intent.category.LAUNCHER', 1)
            time.sleep(2)

            utils.tap_first_template_match('game/main_menu/new_game_button.png')
            time.sleep(1)

            template_prefix = 'game/main_menu/prompts/discard_game_and_start_over/'
            if utils.get_first_template_match(template_prefix + 'prompt_v1.png'):
                utils.tap_first_template_match(template_prefix + 'yes_button_v1.png')
                time.sleep(1)
            if utils.get_first_template_match(template_prefix + 'prompt_v2.png'):
                utils.tap_first_template_match(template_prefix + 'yes_button_v2.png')
                time.sleep(1)

            # while we are still developing OCR, use this hardcoded workaround to keep level the same
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
            plans = planner.get_plans_for_strategy('basic_level_map_full_snake')
            for plan in plans:
                for command in plan.commands:
                    client.update_tile(
                        command.row_i,
                        command.col_i,
                        command.target_tower_id
                    )
                    time.sleep(0.1)
                    i += 1
                    if i == 10:
                        client.enable_fast_forward()

            while True:
                match = utils.get_first_template_match('game/you_win_message.png')

                if match:
                    elapsed = (time.time() - start) / 60
                    print(f"Level completed in {elapsed:.1f} minutes, restarting...")
                    break

                if time.time() - start > (25 * 60):
                    print("Timeout reached, restarting...")
                    break

                time.sleep(5)

        except Exception as e:
            print(f"Error occurred: {e}")
            continue


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
