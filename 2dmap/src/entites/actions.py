class Action:
    """基本的行动类"""
    def __init__(self, soldier):
        self.soldier = soldier

    def execute(self):
        """执行动作"""
        raise NotImplementedError("子类必须实现 execute() 方法")


class MoveAction(Action):
    """移动动作"""
    def __init__(self, soldier, target_x, target_y):
        super().__init__(soldier)
        self.target_x = target_x
        self.target_y = target_y

    def execute(self):
        """执行移动"""
        print(f"{self.soldier.team} 的 {self.soldier.__class__.__name__} 移动到 ({self.target_x}, {self.target_y})")
        self.soldier.move(self.target_x, self.target_y)


class AttackAction(Action):
    """攻击动作"""
    def __init__(self, soldier, target):
        super().__init__(soldier)
        self.target = target

    def execute(self):
        """执行攻击"""
        print(f"{self.soldier.team} 的 {self.soldier.__class__.__name__} 攻击 {self.target.team} 的 {self.target.__class__.__name__}")
        self.soldier.attack(self.target)


class BuildObstacleAction(Action):
    """修筑障碍动作（工程兵专属）"""
    def __init__(self, soldier):
        if not isinstance(soldier, Engineer):
            raise ValueError("只有工程兵可以执行修筑障碍动作")
        super().__init__(soldier)

    def execute(self):
        """执行修筑障碍"""
        print(f"{self.soldier.team} 的工程兵正在修筑障碍")
        self.soldier.build_obstacle()


class HealAction(Action):
    """治疗动作（医疗兵专属）"""
    def __init__(self, soldier, target):
        if not isinstance(soldier, Medic):
            raise ValueError("只有医疗兵可以执行治疗动作")
        super().__init__(soldier)
        self.target = target

    def execute(self):
        """执行治疗"""
        print(f"{self.soldier.team} 的医疗兵正在治疗 {self.target.team} 的单位")
        self.soldier.heal(self.target)


class ReloadAction(Action):
    """重新装弹动作（适用于需要装弹的士兵，如突击兵）"""
    def __init__(self, soldier):
        if not isinstance(soldier, Assault):
            raise ValueError("只有突击兵可以执行重新装弹动作")
        super().__init__(soldier)

    def execute(self):
        """执行重新装弹"""
        print(f"{self.soldier.team} 的突击兵正在重装弹夹")
        self.soldier.reload()


class AimAndAttackAction(Action):
    """瞄准并攻击（支援兵专属）"""
    def __init__(self, soldier, target):
        if not isinstance(soldier, Support):
            raise ValueError("只有支援兵可以执行瞄准并攻击动作")
        super().__init__(soldier)
        self.target = target

    def execute(self):
        """执行瞄准和攻击"""
        print(f"{self.soldier.team} 的支援兵正在瞄准 {self.target.team} 的单位")
        self.soldier.aim_and_attack(self.target)


class SupplyAction(Action):
    """支援动作（支援兵给友军补给弹药或护甲）"""
    def __init__(self, soldier, target):
        if not isinstance(soldier, Support):
            raise ValueError("只有支援兵可以执行补给动作")
        super().__init__(soldier)
        self.target = target

    def execute(self):
        """执行补给弹药或护甲的动作"""
        print(f"{self.soldier.team} 的支援兵正在为 {self.target.team} 提供补给")
        # 这里可以根据需求选择恢复护甲或补充弹药
        if self.target.armor < 100:
            self.target.armor = min(self.target.armor + 50, 100)
            print(f"{self.target.team} 的护甲恢复至 {self.target.armor}")
        elif self.target.weapon and self.target.weapon.current_ammo < self.target.weapon.max_ammo:
            self.target.weapon.reload()
            print(f"{self.target.team} 的武器弹药已补充")


def execute_action(action):
    """执行传入的动作"""
    action.execute()

