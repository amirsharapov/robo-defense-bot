import dotenv

from src.macros.unlock_device import unlock_android


def main():
    unlock_android()


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
