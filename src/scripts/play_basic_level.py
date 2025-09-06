import src.game.client
from src.game import client


def place_towers_for_basic_level():
    # the first towers placed
    client.update_tiles([
        (6, 0, 'gu1'),
        (6, 1, 'gu1'),
        (5, 2, 'gu3'),
        (4, 2, 'sl2'),
        (3, 2, 'gu3'),
        (2, 2, 'gu1'),
        (0, 2, 'gu1'),
    ])

    # break for fast-forward button
    src.game.client.enable_fast_forward()

    # next line of towers to keep path blocked
    client.update_tiles([
        (0, 3, 'gu1'),
        (0, 4, 'gu1'),
        (1, 4, 'gu1'),
        (2, 4, 'sl1'),
        (3, 4, 'gu1'),
        (4, 4, 'gu1'),
        (5, 4, 'gu1'),
        (6, 4, 'sl1'),
        (7, 4, 'gu1'),
        (9, 4, 'gu1'),
        (4, 0, 'gu3'),
        (3, 0, 'gu3'),
        (2, 0, 'sl1'),
        (1, 0, 'gu3'),
        (0, 0, 'gu3'),
        (0, 1, 'gu3')
    ])

    # start upgrading
    client.update_tiles([
        (6, 0, 'gu3'),
        (6, 1, 'gu3'),
        (6, 2, 'gu3'),
        (5, 2, 'gu3'),
        (3, 2, 'gu3'),
        (2, 2, 'gu3'),
        (0, 2, 'gu3'),
        (0, 3, 'gu3'),
        (0, 4, 'gu3'),
        (1, 4, 'gu3'),
        (3, 4, 'gu3'),
        (4, 4, 'gu3'),
        (5, 4, 'gu3'),
        (7, 4, 'gu3'),
        (9, 4, 'gu3')
    ])
    
    # temporary for air defense
    
    client.update_tiles([
        (5, 5, 'aa2'),
        (5, 6, 'aa2'),
        (5, 7, 'aa2'),
        (5, 8, 'aa2'),
        (5, 9, 'aa2'),
        (5, 10, 'aa2'),
        (5, 11, 'gu3'),
        (5, 12, 'gu3'),
        (5, 13, 'gu3'),
        (5, 14, 'gu3'),
        (5, 15, 'gu3'),
        (5, 16, 'gu3'),
        (4, 6, 'sl2'),
        (6, 8, 'sl2')
    ])
