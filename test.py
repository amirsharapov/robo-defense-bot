from src.game import vision
from src.game.client import (
    toggle_fast_forward_button
)

def main():
    match = vision.locate_you_win_message()
    print(match)
    match = vision.locate_gun_towers()
    print(len(match))



if __name__ == "__main__":
    main()
