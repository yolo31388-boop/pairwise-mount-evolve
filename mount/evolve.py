"""坐骑进化与圣兽系统 - 含9个bug"""
from dataclasses import dataclass, field

@dataclass
class Mount:
    mid: str
    name: str
    level: int = 1
    quality: str = "common"
    mount_type: str = "land"  # bug8: 不检查类型
    bloodline: float = 0.5  # bug7: 不计算

class EvolveSystem:
    def __init__(self, seed=42):
        import random
        self.rng = random.Random(seed)

    def can_evolve(self, mount: Mount) -> bool:
        # bug1: 无条件
        return True

    def get_evolve_form(self, mount_type: str) -> str:
        # bug2: 固定形态
        return "sacred_beast"

    def get_sacred_skill(self, beast_type: str) -> str:
        # bug3: 通用技能
        return "sacred_power"

    def get_evolve_material(self, mount_type: str) -> str:
        # bug4: 通用材料
        return "evolve_stone"

    def get_evolve_rate(self, level: int) -> float:
        # bug5: 100%成功
        return 1.0

    def get_failure_refund(self) -> float:
        # bug6: 无返还
        return 0.0

    def calculate_bloodline(self, parent1: float, parent2: float) -> float:
        # bug7: 不计算
        return 0.5

    def can_evolve_type(self, from_type: str, to_type: str) -> bool:
        # bug8: 跨类型
        return True

    def is_mount_consumed(self) -> bool:
        # bug9: 不消耗
        return False
