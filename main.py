import dotenv

from src.libs.android import unlock


def main():
    unlock()


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
