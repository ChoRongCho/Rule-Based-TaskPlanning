import os
from openai import OpenAI


# 일반 유닛
class Unit:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


# 공격 유닛
class AttackUnit(Unit):
    def __init__(self, name, hp, damage):
        Unit.__init__(self, name, hp)
        self.damage = damage

    def attack(self, location):
        print("{0} : {1} 방향으로 적군을 공격 합니다. [공격력 {2}]" \
              .format(self.name, location, self.damage))

    def damaged(self, damage):
        print("{0} : {1} 데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1} 입니다.".format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴되었습니다.".format(self.name))


# 날 수 있는 기능을 가진 클래스
class Flyable:
    def __init__(self, flying_speed):  # 공중 이동 속도
        self.flying_speed = flying_speed

    def fly(self, name, location):  # 유닛 이름, 이동 방향
        print("{0} : {1} 방향으로 날아갑니다. [속도 {2}]" \
              .format(name, location, self.flying_speed))


# 공중 공격 유닛
class FlyableAttackUnit(AttackUnit, Flyable):
    def __init__(self, name, hp, damage, flying_speed):  # 이름, 체력, 공격력, 공중 이동 속도
        AttackUnit.__init__(self, name, hp, damage)  # 이름, 체력, 공격력
        Flyable.__init__(self, flying_speed)  # 공중 이동 속도


def main():
    # 발키리 : 공중 공격 유닛, 한번에 14발 미사일 발사.
    valkyrie = FlyableAttackUnit("발키리", 200, 6, 5)  # 이름, 체력, 공격력, 공중 이동 속도
    valkyrie.fly(valkyrie.name, "3시")  # 3시 방향으로 발키리를 이동
    valkyrie.attack("6시")
    valkyrie.damaged(200)


def clients():
    client = OpenAI(api_key="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")



if __name__ == '__main__':
    main()
