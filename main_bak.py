import pygame
import sys
import random

from ZombiesVSPlants.common.helper import get_nearest_position, load_image_source, load_all_shooters, get_image_size, get_path, get_path
from ZombiesVSPlants.config.config import BULLET_SPEED, BULLET_REFRESH_TIME, ZOMBIE_REFRESH_TIME, SHOOTER_SIZE, ZOMBIE_SPEED_X, LINES

pygame.init()


#顶部菜单高度
menu_height = 60

# 获取背景草地和僵尸, 包括大小，路径等
background_grass_path = get_path("background_grass.png")
zombie_path = get_path("enemy_zombie.png", )
single_line_height = get_image_size("background_grass.png")[1]
zombie_size = get_image_size("enemy_zombie.png")

# 定义屏幕大小和僵尸路数
screen_height = LINES*single_line_height+menu_height
screen_width = 800


# 背景色, 僵尸矢量速度(负数表示从右往左，正数表示从左往右)
background_color = 255, 255, 255
ZOMBIE_SPEED = [-ZOMBIE_SPEED_X, 0]

# 其他
LINES_LIST = [i for i in range(1, LINES+1)]
zombie_start_x = screen_width-zombie_size[0]
zombie_start_y = (single_line_height-zombie_size[1])/2
shooter_centered_position__list_y = [line*single_line_height+zombie_start_y+menu_height for line in range(5)]
# 打死僵尸的爆炸效果
boom = load_image_source("boom.png")
# 鼠标拖动武器初始化数据
dragging = False
mouse_follow = None
mouse_follow_rect = None
added_shooters = []
shooter_bullets = []
bullets_rect = []
collide_zombies = []
collide_bullets = []
# 屏幕大小
screen = pygame.display.set_mode((screen_width, screen_height))
# 加载顶部菜单
res = load_all_shooters()
menu_start_position = 5, 5
menu_shooters = [load_image_source(unselected_shooter, with_bullet=True) for unselected_shooter in res["unselected"]]
menu_shooters_selected = [load_image_source(selected_shooter) for selected_shooter in res["selected"]]
menu_shooters_rect = [pygame.Rect(menu_start_position[0]+55*i, menu_start_position[1], SHOOTER_SIZE[0], SHOOTER_SIZE[1]) for i in range(len(menu_shooters))]

# 背景草地
grass = load_image_source(background_grass_path)
grass_rect = [pygame.Rect(0, i * single_line_height+menu_height, screen_width, single_line_height) for i in range(LINES)]
# 初始化第一个僵尸
zombie = load_image_source(zombie_path)
zombies_rect = [pygame.Rect(zombie_start_x, zombie_start_y+menu_height, zombie_size[0], zombie_size[1])]
# 每隔ZOMBIE_REFRESH_TIME触发僵尸刷新事件
NEW_ZOMBIE_EVENT = pygame.USEREVENT+1
pygame.time.set_timer(NEW_ZOMBIE_EVENT, ZOMBIE_REFRESH_TIME)
# 每隔BULLET_REFRESH_TIME触发子弹刷新事件
NEW_BULLET_EVENT = pygame.USEREVENT+2
pygame.time.set_timer(NEW_BULLET_EVENT, BULLET_REFRESH_TIME)


while 1:
    screen.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 处理菜单点击事件
        # 左键单击某个武器时，可以拖动武器(武器跟随鼠标)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(len(menu_shooters)):
                if menu_shooters_rect[i].collidepoint(event.pos):
                    dragging = not dragging
                    mouse_follow = menu_shooters[i]
        # 右键单击且处于拖动状态时，可以放置武器到某条线路的正中位置
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x = event.pos[0]
            if event.pos[1] > menu_height and dragging:
                dragging = not dragging
                y = get_nearest_position(shooter_centered_position__list_y, event.pos[1])
                added_shooters.append([mouse_follow[0], x, y])
                shooter_bullets.append([x, y, mouse_follow[1]])
        # 子弹刷新事件
        if event.type == NEW_BULLET_EVENT:
            for j in range(len(shooter_bullets)):
                bullets_rect.append([shooter_bullets[j][2], pygame.Rect(shooter_bullets[j][0], shooter_bullets[j][1], 15, 15)])
        # 僵尸刷新事件
        if event.type == NEW_ZOMBIE_EVENT:
            # 新僵尸随机出现的数量和出现在哪几路
            new_zombies_count = random.randint(1, LINES)
            new_zombies_lines = random.sample(LINES_LIST, new_zombies_count)
            # 添加新僵尸到僵尸列表里去
            for line in new_zombies_lines:
                new_zombie_rect = pygame.Rect(zombie_start_x, line * single_line_height + zombie_start_y + menu_height, zombie_size[0], zombie_size[1])
                zombies_rect.append(new_zombie_rect)
    # 绘制顶部武器菜单
    for i in range(len(menu_shooters)):
        menu_rect = menu_shooters_rect[i]
        screen.blit(menu_shooters[i][0], menu_rect)

    # 鼠标移动到顶部菜单栏事件
    for i in range(len(menu_shooters)):
        if menu_shooters_rect[i].collidepoint(pygame.mouse.get_pos()):
            screen.blit(menu_shooters_selected[i], menu_shooters_rect[i])

    # 绘制背景草地
    for r in grass_rect:
        screen.blit(grass, r)
    # 绘制所有的射手
    for new in added_shooters:
        shooter_rect = pygame.Rect(new[1], new[2], 50, 50)
        screen.blit(new[0], shooter_rect)
    # 绘制子弹
    for j in range(len(bullets_rect)):
        bullets_rect[j][1].x += 1
        screen.blit(bullets_rect[j][0], bullets_rect[j][1])
    # 绘制所有僵尸
    for i in range(len(zombies_rect)):
        zombies_rect[i].x -= ZOMBIE_SPEED_X
        screen.blit(zombie, zombies_rect[i])

    if dragging and mouse_follow[0]:
        pos_follow_mouse = pygame.mouse.get_pos()
        mouse_follow_rect = pygame.Rect(pos_follow_mouse[0], pos_follow_mouse[1], 50, 50)
        screen.blit(mouse_follow[0], mouse_follow_rect)

    # 子弹和僵尸的碰撞检测
    for i in range(len(bullets_rect)):
        for j in range(len(zombies_rect)):
            if bullets_rect[i][1].colliderect(zombies_rect[j]):
                screen.blit(boom, zombies_rect[j])
                collide_bullets.append(bullets_rect[i])
                collide_zombies.append(zombies_rect[j])
    bullets_rect = [i for i in bullets_rect if i not in collide_bullets]
    zombies_rect = [j for j in zombies_rect if j not in collide_zombies]
    # 如何处理反向的一种很好的方法
    # if zombie_rect.left < 0 or zombie_rect.right > screen_width:
    #     ZOMBIE_SPEED[0] = -ZOMBIE_SPEED[0]
    pygame.display.flip()