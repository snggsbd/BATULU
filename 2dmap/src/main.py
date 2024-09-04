import arcade
import arcade.gui
import time
from arcade.gui import UIManager, UIFlatButton, UIInputText, UIBoxLayout, UILabel

# 设置默认游戏窗口大小
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "2D Turn-Based Strategy Game"

# 回合间的延迟
TURN_DELAY = 0.1  # 每个回合至少持续0.1秒


class MainMenuView(arcade.View):
    """主菜单界面"""

    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

    def on_show(self):
        """当这个视图显示时"""
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.ui_manager.clear()  # 清理现有的UI元素
        self.ui_manager.enable()

        # 创建一个垂直布局，用于排列按钮
        self.v_box = UIBoxLayout(vertical=True, space_between=20)

        # 创建开始游戏按钮
        start_button = UIFlatButton(text="开始游戏", width=200)
        start_button.on_click = self.on_click_start
        self.v_box.add(start_button)

        # 创建修改设置按钮
        settings_button = UIFlatButton(text="修改设置", width=200)
        settings_button.on_click = self.on_click_settings
        self.v_box.add(settings_button)

        # 创建退出游戏按钮
        exit_button = UIFlatButton(text="退出游戏", width=200)
        exit_button.on_click = self.on_click_exit
        self.v_box.add(exit_button)

        # 将按钮添加到UIManager中
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        """处理开始游戏按钮点击"""
        game_view = TurnBasedStrategyGame()
        game_view.setup()
        self.window.show_view(game_view)

    def on_click_settings(self, event):
        """处理修改设置按钮点击"""
        settings_view = SettingsView()
        self.window.show_view(settings_view)

    def on_click_exit(self, event):
        """处理退出游戏按钮点击"""
        arcade.close_window()

    def on_draw(self):
        """渲染主菜单界面"""
        arcade.start_render()
        # 渲染UI元素
        self.ui_manager.draw()

        # 添加标题文字
        arcade.draw_text("2D Strategy Game", self.window.width / 2, self.window.height / 1.5,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

    def on_hide_view(self):
        """当视图隐藏时，禁用UIManager"""
        self.ui_manager.disable()


class SettingsView(arcade.View):
    """设置界面"""

    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

    def on_show(self):
        """当这个视图显示时"""
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.ui_manager.clear()  # 清理现有的UI元素
        self.ui_manager.enable()

        # 创建一个垂直布局，用于排列设置项
        self.v_box = UIBoxLayout(vertical=True, space_between=20)

        # 添加窗口宽度设置
        self.v_box.add(UILabel(text="窗口宽度:", font_size=20))
        self.width_input = UIInputText(text=str(self.window.width), width=200)
        self.v_box.add(self.width_input)

        # 添加窗口高度设置
        self.v_box.add(UILabel(text="窗口高度:", font_size=20))
        self.height_input = UIInputText(text=str(self.window.height), width=200)
        self.v_box.add(self.height_input)

        # 添加全屏切换按钮
        self.fullscreen_button = UIFlatButton(text="切换全屏", width=200)
        self.fullscreen_button.on_click = self.on_click_fullscreen
        self.v_box.add(self.fullscreen_button)

        # 添加应用设置按钮
        apply_button = UIFlatButton(text="应用设置", width=200)
        apply_button.on_click = self.on_click_apply
        self.v_box.add(apply_button)

        # 添加返回主菜单按钮
        back_button = UIFlatButton(text="返回主菜单", width=200)
        back_button.on_click = self.on_click_back
        self.v_box.add(back_button)

        # 将设置项添加到UIManager中
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_fullscreen(self, event):
        """切换全屏模式"""
        self.window.set_fullscreen(not self.window.fullscreen)

    def on_click_apply(self, event):
        """应用窗口大小设置"""
        try:
            new_width = int(self.width_input.text)
            new_height = int(self.height_input.text)
            self.window.set_size(new_width, new_height)
        except ValueError:
            print("请输入有效的窗口宽度和高度！")

    def on_click_back(self, event):
        """返回主菜单"""
        main_menu = MainMenuView()
        self.window.show_view(main_menu)

    def on_draw(self):
        """渲染设置界面"""
        arcade.start_render()
        # 渲染UI元素
        self.ui_manager.draw()

    def on_hide_view(self):
        """当视图隐藏时，禁用UIManager"""
        self.ui_manager.disable()


class TurnBasedStrategyGame(arcade.View):
    """游戏主视图"""

    def __init__(self):
        super().__init__()
        self.turn_counter = 0  # 当前回合计数
        self.player_units = []  # 玩家单位列表
        self.enemy_units = []  # 敌方单位列表
        self.map = None  # 地图对象

    def setup(self):
        """游戏开始前的设置"""
        arcade.set_background_color(arcade.color.ASH_GREY)

        # 加载地图
        self.load_map()

        # 初始化单位
        self.initialize_units()

    def load_map(self):
        """加载或生成地图"""
        # 这里可以加载Tiled地图，或者调用随机地图生成器
        pass

    def initialize_units(self):
        """初始化玩家和敌方单位"""
        # 这里可以添加玩家和敌人的单位，设置初始位置
        pass

    def on_show(self):
        """当这个视图显示时"""
        arcade.set_background_color(arcade.color.ASH_GREY)

    def on_draw(self):
        """渲染屏幕内容，每帧都调用"""
        arcade.start_render()

        # 绘制地图
        self.draw_map()

        # 绘制玩家单位
        for unit in self.player_units:
            unit.draw()

        # 绘制敌方单位
        for unit in self.enemy_units:
            unit.draw()

    def draw_map(self):
        """绘制地图"""
        # 在这里绘制地图，例如通过Arcade的TileMap类来渲染Tiled地图
        pass

    def on_update(self, delta_time):
        """游戏逻辑更新，每帧调用"""
        # 控制回合系统，每0.1秒更新一次
        self.handle_turn_logic()

    def handle_turn_logic(self):
        """处理回合逻辑"""
        self.turn_counter += 1
        print(f"Executing turn {self.turn_counter}")

        # 暂时模拟回合的延时
        time.sleep(TURN_DELAY)

        # 执行回合操作，比如单位移动和攻击逻辑
        for unit in self.player_units:
            unit.take_turn()
        for unit in self.enemy_units:
            unit.take_turn()

    def on_key_press(self, key, modifiers):
        """处理按键事件"""
        if key == arcade.key.ESCAPE:
            main_menu = MainMenuView()
            self.window.show_view(main_menu)


class Unit:
    """示例单位类"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 10

    def draw(self):
        """绘制单位"""
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

    def take_turn(self):
        """单位执行回合逻辑"""
        # 示例：单位随机移动
        import random
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)


def main():
    """游戏主函数"""
    window = arcade.Window(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    main_menu_view = MainMenuView()
    window.show_view(main_menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
