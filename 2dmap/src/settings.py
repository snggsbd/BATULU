import json
import os

# 默认设置
DEFAULT_SETTINGS = {
    "screen_width": 800,
    "screen_height": 600,
    "fullscreen": False,
    "volume": 100,  # 音量范围：0-100
    "turn_delay": 0.1,  # 每回合的延迟时间（秒）
}

SETTINGS_FILE = "game_settings.json"

def load_settings():
    """加载设置文件，如果文件不存在，使用默认设置"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
            return settings
        except json.JSONDecodeError:
            print("设置文件损坏，使用默认设置。")
            return DEFAULT_SETTINGS.copy()
    else:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """保存当前设置到文件"""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        print(f"保存设置时出错: {e}")

def reset_settings():
    """重置为默认设置，并保存"""
    settings = DEFAULT_SETTINGS.copy()
    save_settings(settings)
    return settings

# 示例：读取当前设置并保存更新
if __name__ == "__main__":
    current_settings = load_settings()
    print("当前设置:", current_settings)

    # 修改某个设置项，例如将音量调低
    current_settings["volume"] = 50
    save_settings(current_settings)
    print("设置已更新并保存:", current_settings)
