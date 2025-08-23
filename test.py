import cv2

from src.client.grid import AnchorTypes, generate_grid
from src.client.vision import locate_gun_towers
from src.libs.android import screenshot
from src.libs.vision import match_template


def main():
    image = screenshot()

    template = 'data/src/templates/basic_level/anchor.png'
    template = cv2.imread(template)

    result = match_template(image, template, threshold=0.8)
    result = result[0].rect

    # draw grid
    matrix = generate_grid(AnchorTypes.EXIT, result)

    for col in matrix:
        for cell in col:
            cv2.circle(
                image,
                (cell.center.x, cell.center.y),
                radius=3,
                color=(0, 255, 0),
                thickness=-1
            )
            cv2.rectangle(
                image,
                (cell.x, cell.y),
                (cell.x + cell.w, cell.y + cell.h),
                color=(255, 0, 0),
                thickness=1
            )

    # locate the gun towers
    towers = locate_gun_towers(image)
    for tower in towers:
        cv2.rectangle(
            image,
            (tower.rectangle.x, tower.rectangle.y),
            (tower.rectangle.x + tower.rectangle.w, tower.rectangle.y + tower.rectangle.h),
            color=(0, 0, 255),
            thickness=2
        )

    cv2.imwrite('temp.png', image)

    print('Done')


if __name__ == "__main__":
    main()
