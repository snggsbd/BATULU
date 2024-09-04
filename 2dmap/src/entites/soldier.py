import arcade
import random
import math

# 定义武器类
class Weapon:
    def __init__(self, name, range, damage, max_ammo, fire_rate):
        """武器属性：名称、射程、伤害、最大弹药数、每回合可发射的子弹数"""
        self.name = name
        self.range = range
        self.damage = damage
        self.max_ammo = max_ammo
        self.fire_rate = fire_rate
        self.current_ammo = max_ammo

    def fire(self):
        """发射子弹，返回本回合发射的子弹数量"""
        fired_ammo = min(self.fire_rate, self.current_ammo)
        self.current_ammo -= fired_ammo
        return fired_ammo

    def reload(self):
        """重新装弹，恢复最大弹药"""
        self.current_ammo = self.max_ammo


# 士兵基础类
class Soldier:
    def __init__(self, x, y, team, health=100, armor=100, speed=2, weapon=None, color=arcade.color.BLUE):
        """士兵的初始化，包括位置、队伍、生命值、护甲、速度、武器等"""
        self.x = x
        self.y = y
        self.team = team  # 队伍：蓝方或红方
        self.health = health  # 生命值
        self.armor = armor  # 护甲值
        self.speed = speed  # 移动速度
        self.weapon = weapon  # 士兵携带的武器
        self.color = color  # 士兵颜色
        self.radius = 10  # 士兵在地图上的显示半径

    def move(self, target_x, target_y):
        """移动士兵，朝目标方向移动，基于士兵的速度"""
        direction_x = target_x - self.x
        direction_y = target_y - self.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        
        if distance > 0:
            direction_x /= distance
            direction_y /= distance
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed

    def attack(self, target):
        """攻击目标士兵"""
        if target:
            fired_ammo = self.weapon.fire()
            for _ in range(fired_ammo):
                # 计算弹药命中或散布
                if self._check_hit(target):
                    damage = self.weapon.damage
                    actual_damage = self.calculate_damage(target, damage)
                    target.take_damage(actual_damage)
                    print(f"{self.team} 士兵使用 {self.weapon.name} 攻击了 {target.team}，造成 {actual_damage} 伤害！")

    def _check_hit(self, target):
        """判断弹药是否命中目标"""
        hit_chance = 0.8  # 命中概率
        return random.random() < hit_chance

    def calculate_damage(self, target, base_damage):
        """计算基于护甲的实际伤害"""
        if target.armor > 0:
            reduced_damage = base_damage * (1 - target.armor / 100)
            target.armor -= base_damage - reduced_damage
            return reduced_damage
        return base_damage

    def take_damage(self, damage):
        """士兵受到伤害，生命值减少"""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        """判断士兵是否存活"""
        return self.health > 0

    def draw(self):
        """绘制士兵"""
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

    def distance_to(self, target):
        """计算到目标的距离"""
        return math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)


# 工程兵类，具备修筑障碍物的能力
class Engineer(Soldier):
    def __init__(self, x, y, team, weapon=None):
        super().__init__(x, y, team, health=120, armor=100, speed=1.5, weapon=weapon or Weapon("手枪", 40, 30, 7, 1), color=arcade.color.GREEN)
        self.build_turns = 0  # 工程兵修筑障碍物的回合数
    
    def build_obstacle(self):
        """工程兵修筑障碍，三回合内无法移动或攻击"""
        if self.build_turns < 3:
            self.build_turns += 1
            print(f"{self.team} 工程兵正在修筑障碍... ({self.build_turns}/3)")
        else:
            self.build_turns = 0
            print(f"{self.team} 工程兵完成了障碍的修筑！")

    def take_turn(self, allies, enemies):
        """工程兵回合：修筑障碍或攻击敌人"""
        if self.build_turns > 0:
            self.build_obstacle()
        else:
            super().take_turn(enemies)


# 医疗兵类，具备治疗能力
class Medic(Soldier):
    def __init__(self, x, y, team, weapon=None):
        super().__init__(x, y, team, health=80, armor=50, speed=2, weapon=weapon or Weapon("手枪", 40, 30, 7, 1), color=arcade.color.WHITE)
        self.heal_turns = 0

    def heal(self, target):
        """医疗兵治疗友军，5回合内无法移动或攻击"""
        if self.heal_turns < 5:
            self.heal_turns += 1
            print(f"医疗兵正在治疗 {target.team}，{self.heal_turns}/5 回合")
        else:
            target.health = min(target.health + 50, 100)
            self.heal_turns = 0
            print(f"医疗兵完成了治疗，恢复了 {target.team} 的生命值！")

    def take_turn(self, allies, enemies):
        """医疗兵回合：优先治疗友军"""
        injured_allies = [ally for ally in allies if ally.health < 100]
        if injured_allies:
            closest_ally = min(injured_allies, key=lambda ally: self.distance_to(ally))
            if self.distance_to(closest_ally) < 10:
                self.heal(closest_ally)
            else:
                self.move(closest_ally.x, closest_ally.y)
        else:
            super().take_turn(enemies)


# 突击兵类
class Assault(Soldier):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, health=100, armor=70, speed=2.5, weapon=Weapon("冲锋枪", 50, 40, 30, 3), color=arcade.color.RED)
        self.reload_turns = 0

    def reload(self):
        """突击兵需要5个回合重装弹夹"""
        if self.reload_turns < 5:
            self.reload_turns += 1
            self.speed = 1.5  # 重装时速度降低
            print(f"{self.team} 突击兵正在重装弹夹... ({self.reload_turns}/5)")
        else:
            self.weapon.reload()
            self.reload_turns = 0
            self.speed = 2.5
            print(f"{self.team} 突击兵完成了重装！")

    def take_turn(self, enemies):
        """突击兵回合：攻击或重装弹夹"""
        if self.weapon.current_ammo == 0:
            self.reload()
        else:
            super().take_turn(enemies)


# 支援兵类
class Support(Soldier):
    def __init__(self, x, y, team):
        super().__init__(x, y, team, health=100, armor=50, speed=1.0, weapon=Weapon("狙击枪", 200, 200, float('inf'), 1), color=arcade.color.YELLOW)
        self.aim_turns = 0

    def aim_and_attack(self, target):
        """支援兵瞄准并攻击，瞄准5回合后才能攻击"""
        if self.aim_turns < 5:
            self.aim_turns += 1
            print(f"{self.team} 支援兵正在瞄准 {target.team} ({self.aim_turns}/5)")
        else:
            self.attack(target)
            self.aim_turns = 0

    def take_turn(self, allies, enemies):
        """支援兵回合：瞄准敌人或补充友军护甲和弹药"""
        closest_enemy = min(enemies, key=lambda enemy: self.distance_to(enemy))
        if self.distance_to(closest_enemy) <= self.weapon.range and not self._has_obstacles(closest_enemy):
            self.aim_and_attack(closest_enemy)
        else:
            super().take_turn(enemies)

    def _has_obstacles(self, target):
        """判断瞄准路径中是否有障碍物"""
        # 简化为假设路径中没有障碍物
        return False

