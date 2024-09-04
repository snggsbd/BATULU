import arcade
import numpy as np
import csv
import os

# 地图文件路径
TERRAIN_FILE = "terrain_map.csv"
HEIGHT_FILE = "height_map.csv"

# 地形类型
EMPTY = 0  # 空地
OBSTACLE = 1  # 障碍物
WATER = 2  # 水域
MOUNTAIN = 3  # 山地

# 颜色定义（用于渲染）
COLOR_MAPPING = {
    EMPTY: arcade.color.LIGHT_GRAY,   # 空地颜色
    OBSTACLE: arcade.color.DARK_BROWN,   # 障碍物颜色
    WATER: arcade.color.BLUE,   # 水域颜色
    MOUNTAIN: arcade.color.DARK_SLATE_GRAY   # 山地颜色
}

def load_map_from_csv(terrain_filename, height_filename):
    """从 CSV 文件中加载地形和高度地图"""
    if os.path.exists(terrain_filename) and os.path.exists(height_filename):
        with open(terrain_filename, 'r') as f:
            terrain_map = np.array([list(map(int, row)) for row in csv.reader(f)])
        
        with open(height_filename, 'r') as f:
            height_map = np.array([list(map(int, row)) for row in csv.reader(f)])
        
        return terrain_map, height_map
    else:
        raise FileNotFoundError(f"地图文件 {terrain_filename} 或 {height_filename} 不存在！")


def render_map(terrain_map, height_map, tile_size=5):
    """根据地图数据渲染地图"""
    rows, cols = terrain_map.shape
    for row in range(rows):
        for col in range(cols):
            # 获取地形和高度信息
            terrain_type = terrain_map[row, col]
            height_value = height_map[row, col]
            
            # 选择地形颜色
            color = COLOR_MAPPING.get(terrain_type, arcade.color.WHITE)
            
            # 根据高度调整亮度
            brightness_factor = 1 - (height_value / 100)  # 假设高度为0-100
            color_with_brightness = arcade.color_from_hex_string(
                arcade.color.hex_color_adjust_brightness(color, brightness_factor)
            )

            # 绘制地形方块
            arcade.draw_rectangle_filled(
                col * tile_size + tile_size / 2,
                row * tile_size + tile_size / 2,
                tile_size, tile_size,
                color_with_brightness
            )


class MapView(arcade.View):
    """地图渲染视图"""
    
    def __init__(self):
        super().__init__()
        self.terrain_map = None
        self.height_map = None
        self.tile_size = 5  # 每个单元格的大小（像素）
    
    def setup(self):
        """加载地图并设置"""
        self.terrain_map, self.height_map = load_map_from_csv(TERRAIN_FILE, HEIGHT_FILE)
    
    def on_draw(self):
        """渲染地图"""
        arcade.start_render()
        render_map(self.terrain_map, self.height_map, self.tile_size)


def main():
    """主函数，用于加载和渲染地图"""
    window = arcade.Window(1000, 1000, "Map Loader")
    map_view = MapView()
    map_view.setup()
    window.show_view(map_view)
    arcade.run()


if __name__ == "__main__":
    main()
