import dotenv

from src.libs.android import unlock, setup_screenshot_api_port_forwarding
from src.scripts.play_basic_level import play_basic_level


def main():
    setup_screenshot_api_port_forwarding()
    play_basic_level()


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
