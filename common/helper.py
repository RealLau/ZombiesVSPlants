import os
from PIL import Image
import pygame
current_dir = os.getcwd()


def get_path(image_name):
    return os.path.join(current_dir, "resource", image_name)


def get_image_size(image_name):
    with Image.open(get_path(image_name)) as im:
        return im.size


# 返回Surface和Surface使用的原图，以便根据Surface原图判断发射不同的子弹
def load_image_source(image_name, with_bullet=False):
    if with_bullet:
        bullet_name = "bullet_"+image_name.replace("shooter_", "")
        return pygame.image.load(get_path(image_name)), pygame.image.load(get_path(bullet_name))
    else:
        return pygame.image.load(get_path(image_name))


def load_all_shooters():
    weapon = {"selected": [], "unselected": []}
    shooter_dir = os.path.join(current_dir, "resource")
    for shooter in os.listdir(shooter_dir):
        if "shooter" in shooter:
            if "selected" in shooter:
                weapon["selected"].append(shooter)
            else:
                weapon["unselected"].append(shooter)
    weapon["selected"] = sorted(weapon["selected"])
    weapon["unselected"] = sorted(weapon["unselected"])
    return weapon


def get_nearest_position(source_list, target_number):
    return min(source_list, key=lambda x: abs(x - target_number))


class Zombie(pygame.Rect):
    def __init__(self, left, top, width, height):
        super(Zombie, self).__init__(left, top, width, height)
        self.hit = 0
        self.total_hit = 0

    def add_hit(self):
        self.hit += 1

