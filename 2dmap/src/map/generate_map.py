import numpy as np
import csv
import os

# 地图尺寸
MAP_WIDTH = 1000  # 地图宽度，单位：格子
MAP_HEIGHT = 1000  # 地图高度，单位：格子

# 地形类型
EMPTY = 0  # 空地
OBSTACLE = 1  # 障碍物
WATER = 2  # 水域
MOUNTAIN = 3  # 山地

# 高度范围
MIN_HEIGHT = 0  # 最低高度
MAX_HEIGHT = 100  # 最高高度

# 玩家和敌人的起始点
PLAYER_START_POS = (0, 0)
ENEMY_START_POS = (MAP_HEIGHT - 1, MAP_WIDTH - 1)


def generate_random_map(width, height, obstacle_chance=0.2, water_chance=0.05, mountain_chance=0.1):
    """生成一个随机地图，包含地形和高度信息"""
    # 创建一个全空地的地图
    game_map = np.full((height, width, 2), [EMPTY, 0], dtype=int)  # 地形和高度
    
    # 随机放置障碍物、水域和山地
    for y in range(height):
        for x in range(width):
            rand_val = np.random.random()
            if rand_val < obstacle_chance:
                game_map[y, x][0] = OBSTACLE  # 地形为障碍物
            elif rand_val < obstacle_chance + water_chance:
                game_map[y, x][0] = WATER  # 地形为水域
            elif rand_val < obstacle_chance + water_chance + mountain_chance:
                game_map[y, x][0] = MOUNTAIN  # 地形为山地
            
            # 生成随机高度
            game_map[y, x][1] = np.random.randint(MIN_HEIGHT, MAX_HEIGHT)

    return game_map


def save_map_to_csv(game_map, terrain_filename="terrain_map.csv", height_filename="height_map.csv"):
    """将生成的地图保存为两个 CSV 文件，分别为地形和高度信息"""
    terrain_map = game_map[:, :, 0]  # 地形部分
    height_map = game_map[:, :, 1]  # 高度部分

    # 保存地形到 CSV 文件
    with open(terrain_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(terrain_map)

    # 保存高度到 CSV 文件
    with open(height_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(height_map)


def load_map_from_csv(terrain_filename="terrain_map.csv", height_filename="height_map.csv"):
    """从 CSV 文件中加载地形和高度地图"""
    if os.path.exists(terrain_filename) and os.path.exists(height_filename):
        with open(terrain_filename, 'r') as f:
            terrain_map = np.array([list(map(int, row)) for row in csv.reader(f)])
        
        with open(height_filename, 'r') as f:
            height_map = np.array([list(map(int, row)) for row in csv.reader(f)])
        
        # 将地形和高度合并为完整地图
        game_map = np.stack((terrain_map, height_map), axis=-1)
        return game_map
    else:
        raise FileNotFoundError(f"地图文件 {terrain_filename} 或 {height_filename} 不存在！")


if __name__ == "__main__":
    # 生成随机地图
    game_map = generate_random_map(MAP_WIDTH, MAP_HEIGHT)

    # 保存地图到 CSV 文件
    save_map_to_csv(game_map)
    print("地图已保存为 terrain_map.csv 和 height_map.csv")

    # 从文件中加载地图
    loaded_map = load_map_from_csv()
    print("已从文件中加载地图。")
