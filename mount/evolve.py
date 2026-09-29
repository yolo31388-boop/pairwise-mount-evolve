"""坐骑进化与圣兽系统"""
from dataclasses import dataclass, field

MAX_LEVEL = 10
EVOLVE_QUALITY = "legendary"
PITY_THRESHOLD = 5
DEFAULT_REFUND_RATE = 0.5

EVOLVE_FORMS = {
    "land": "qilin",
    "flying": "phoenix",
    "water": "dragon",
    "fire": "fire_qilin",
}

SACRED_SKILLS = {
    "phoenix": "nirvana_rebirth",
    "dragon": "tidal_domain",
    "qilin": "earth_guard",
    "fire_qilin": "flame_purge",
}


@dataclass
class Mount:
    mid: str
    name: str
    level: int = 1
    quality: str = "common"
    mount_type: str = "land"
    bloodline: float = 0.5
    consumed: bool = False


class EvolveSystem:
    def __init__(self, seed=42, refund_rate=DEFAULT_REFUND_RATE, pity_threshold=PITY_THRESHOLD):
        import random
        self.rng = random.Random(seed)
        self.refund_rate = refund_rate
        self.pity_threshold = pity_threshold
        self._fail_counts = {}

    def can_evolve(self, mount: Mount) -> bool:
        # fix1: 只有满级传说坐骑才能进化
        return (
            not mount.consumed
            and mount.level >= MAX_LEVEL
            and mount.quality == EVOLVE_QUALITY
        )

    def get_evolve_form(self, mount_type: str) -> str:
        # fix2: 形态按坐骑类型分支
        return EVOLVE_FORMS.get(mount_type, f"sacred_{mount_type}")

    def get_sacred_skill(self, beast_type: str) -> str:
        # fix3: 技能按圣兽类型区分
        return SACRED_SKILLS.get(beast_type, f"{beast_type}_skill")

    def get_evolve_material(self, mount_type: str) -> str:
        # fix4: 材料按坐骑类型区分
        return f"{mount_type}_evolve_stone"

    def get_evolve_rate(self, level: int) -> float:
        # fix5: 等级越高成功率越低
        rate = 1.0 - level * 0.08
        return max(0.1, min(1.0, rate))

    def get_failure_refund(self) -> float:
        # fix6: 失败返还材料（默认50%）
        return self.refund_rate

    def get_pity_threshold(self) -> int:
        # fix6: 保底机制，连续失败N次后必成功
        return self.pity_threshold

    def calculate_bloodline(self, parent1: float, parent2: float) -> float:
        # fix7: 血脉按父母血统计算，纯种有加成
        base = (parent1 + parent2) / 2.0
        if parent1 == parent2 and parent1 > 0:
            base += 0.1 * parent1  # 纯种加成
        return max(0.0, min(1.0, base))

    def can_evolve_type(self, from_type: str, to_type: str) -> bool:
        # fix8: 类型限制，不能跨类型进化
        return from_type == to_type

    def is_mount_consumed(self) -> bool:
        # fix9: 进化后原坐骑消耗
        return True

    def evolve(self, mount: Mount):
        """执行进化：成功率判定 + 保底 + 材料返还 + 消耗原坐骑。

        返回 (success, form_or_refund)。
        """
        if not self.can_evolve(mount):
            return False, None

        fails = self._fail_counts.get(mount.mid, 0)
        rate = self.get_evolve_rate(mount.level)
        success = fails + 1 >= self.pity_threshold or self.rng.random() < rate

        if success:
            self._fail_counts[mount.mid] = 0
            mount.consumed = True  # fix9
            return True, self.get_evolve_form(mount.mount_type)

        self._fail_counts[mount.mid] = fails + 1
        return False, self.get_failure_refund()
