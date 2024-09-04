import random

LONG_ATTACK_NUM = 10


techplus_long_attack = 1
techplus_long_defence = 1
BASE_NUM = 5



class Archer:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.long_attack_num = LONG_ATTACK_NUM
        self.long_defence_num = LONG_ATTACK_NUM

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def long_attacknum(self, long_attack_num):
        
        self.long_attack_num = LONG_ATTACK_NUM + techplus_long_attack


    def long_defencenum(self, long_defence_num):
        self.long_defence_num = LONG_ATTACK_NUM + techplus_long_defence


    # def techplus_attack(self, plus_damage):
    #     self.damage += plus_damage

    # def techplus_defence(self, plus_defence);
    #     self.defence += plus_defence   

    


def display_team_status(team, team_name):
    print(f"\n{team_name} 状态:")
    for i, archer in enumerate(team):
        status = "存活" if archer.is_alive() else "死亡"
        print(f"{i + 1}. {archer.name} - HP: {archer.hp} ({status})\n远攻：{archer.long_attack_num} 远防：{archer.long_defence_num}\n")

def get_target(team):
    while True:

        try:

            target = int(input("选择一个目标：")) - 1
            if 0 <= target < len(team) and team[target].is_alive():
                return target
            else:
                print("无效选择，请选择一个存活的目标。")
        except ValueError:
            print("请输入一个有效的数字。")

# def game_turn(player_team, computer_team):
#     # 玩家回合
#     display_team_status(computer_team, "黑队")
#     for i,archer in enumerate(player_team):
#         if archer.is_alive():
        
#          target = get_target(computer_team)
#          computer_team[target].take_damage(20)
#          print(f"你命令 {archer.name}射击了 {computer_team[target].name}！")

#     # 电脑回合
#     living_targets = [archer for archer in player_team if archer.is_alive()]
#     for i,archer in enumerate(computer_team):
#         if archer.is_alive(): 
#           target = random.choice(living_targets)
#           target.take_damage(20)
#           print(f"电脑{archer.name}射击了 {target.name}！")



def game_turn(player_team, computer_team):
    # display_team_status(player_team, "红队")
    # display_team_status(computer_team, "黑队")
    # 玩家选择目标
    player_targets = []
    for i, archer in enumerate(player_team):
        if archer.is_alive():
            target = get_target(computer_team)
            player_targets.append((i, target))
    
    # 电脑选择目标
    computer_targets = []
    living_targets = [i for i, archer in enumerate(player_team) if archer.is_alive()]
    for i, archer in enumerate(computer_team):
        if archer.is_alive():
            target = random.choice(living_targets)
            computer_targets.append((i, target))
    
    # # 显示电脑队伍状态
    # display_team_status(computer_team, "黑队")
    
    # 玩家射击
    for player_index, target_index in player_targets:
        computer_team[target_index].take_damage(20)
        print(f"你命令 {player_team[player_index].name} 射击了 {computer_team[target_index].name}！")
    
    # 显示玩家队伍状态
    # display_team_status(player_team, "红队")
    
    # 电脑射击
    for computer_index, target_index in computer_targets:
        player_team[target_index].take_damage(20)
        print(f"电脑 {computer_team[computer_index].name} 射击了 {player_team[target_index].name}！")     


    display_team_status(player_team, "红队")
    display_team_status(computer_team, "黑队")


def check_game_over(player_team, computer_team):
    player_alive = any(archer.is_alive() for archer in player_team)
    computer_alive = any(archer.is_alive() for archer in computer_team)
    if not player_alive:
        print("\n黑队获胜！")
        return True
    elif not computer_alive:
        print("\n红队获胜！")
        return True
    return False

def main():
    player_team = [Archer(f"红队{i + 1}") for i in range(5)]
    computer_team = [Archer(f"黑队{i + 1}") for i in range(5)]

    print("start")
    
    while True:
        game_turn(player_team, computer_team)
        # display_team_status(player_team, "红队")
        if check_game_over(player_team, computer_team):
            break

if __name__ == "__main__":
    main()
