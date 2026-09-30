"""坐骑进化与圣兽系统"""
from dataclasses import dataclass, field
import random

MAX_LEVEL = 100
EVOLVE_QUALITY = "legendary"
DEFAULT_REFUND_RATE = 0.5
PITY_THRESHOLD = 5  # 连续失败N次后必成功

# 进化形态: 按坐骑类型 + 属性分支
EVOLVE_FORMS = {
    ("land", "fire"): "flame_qilin",
    ("land", "water"): "tide_tortoise",
    ("land", "wind"): "storm_tiger",
    ("flying", "fire"): "phoenix",
    ("flying", "water"): "rain_dragon",
    ("flying", "wind"): "thunder_roc",
    ("water", "fire"): "lava_leviathan",
    ("water", "water"): "frost_whale",
    ("water", "wind"): "mist_serpent",
}

# 圣兽专属技能: 按圣兽类型 + 血脉纯度区分
SACRED_SKILLS = {
    "phoenix": ("nirvana_flame", "rebirth_of_purity"),
    "dragon": ("dragon_breath", "ancient_dragon_roar"),
    "flame_qilin": ("qilin_fire", "holy_qilin_blessing"),
    "tide_tortoise": ("tidal_shield", "abyss_guardian"),
    "storm_tiger": ("storm_claw", "tempest_god_fury"),
    "rain_dragon": ("rain_call", "ocean_sovereign"),
    "thunder_roc": ("thunder_dive", "sky_thunder_wrath"),
    "lava_leviathan": ("lava_surge", "volcano_heart"),
    "frost_whale": ("frost_wave", "glacial_prison"),
    "mist_serpent": ("mist_veil", "illusion_of_nine_heavens"),
}

# 进化材料: 按坐骑类型区分
EVOLVE_MATERIALS = {
    "fire": "fire_evolve_stone",
    "water": "water_evolve_stone",
    "wind": "wind_evolve_stone",
    "land": "earth_evolve_stone",
    "flying": "sky_evolve_stone",
}

# 类型限制: 坐骑类型 -> 允许进化成的圣兽类型
ALLOWED_TYPE_EVOLUTION = {
    "land": {"land"},
    "flying": {"flying"},
    "water": {"water"},
}

PURE_BLOODLINE_THRESHOLD = 0.9
PURE_BLOODLINE_BONUS = 0.1


@dataclass
class Mount:
    mid: str
    name: str
    level: int = 1
    quality: str = "common"
    mount_type: str = "land"
    attribute: str = "fire"
    bloodline: float = 0.5


class EvolveSystem:
    def __init__(self, seed=42, refund_rate=DEFAULT_REFUND_RATE, pity_threshold=PITY_THRESHOLD):
        self.rng = random.Random(seed)
        self.refund_rate = refund_rate
        self.pity_threshold = pity_threshold
        self._fail_streak = {}

    # 1. 进化条件: 只有满级传说坐骑才能进化
    def can_evolve(self, mount: Mount) -> bool:
        return mount.level >= MAX_LEVEL and mount.quality == EVOLVE_QUALITY

    # 2. 进化形态: 按坐骑类型和属性分支
    def get_evolve_form(self, mount_type: str, attribute: str = "fire") -> str:
        return EVOLVE_FORMS.get((mount_type, attribute), f"{mount_type}_{attribute}_beast")

    # 3. 圣兽技能: 按圣兽类型和血脉区分
    def get_sacred_skill(self, beast_type: str, bloodline: float = 0.5) -> str:
        common_skill, pure_skill = SACRED_SKILLS.get(
            beast_type, (f"{beast_type}_power", f"{beast_type}_pure_power"))
        return pure_skill if bloodline >= PURE_BLOODLINE_THRESHOLD else common_skill

    # 4. 进化材料: 按坐骑类型区分
    def get_evolve_material(self, mount_type: str) -> str:
        return EVOLVE_MATERIALS.get(mount_type, f"{mount_type}_evolve_stone")

    # 5. 成功率: 等级越高成功率越低
    def get_evolve_rate(self, level: int) -> float:
        rate = 1.0 - 0.05 * max(0, level - 1)
        return max(0.05, min(1.0, rate))

    # 6. 失败保底与材料返还
    def get_failure_refund(self) -> float:
        return self.refund_rate

    def _pity_key(self, mount: Mount) -> str:
        return mount.mid

    def evolve(self, mount: Mount, target_type: str = None):
        """执行进化。返回 (成功?, 形态或返还材料比例)。"""
        if not self.can_evolve(mount):
            return False, "requirements_not_met"
        target_type = target_type or mount.mount_type
        if not self.can_evolve_type(mount.mount_type, target_type):
            return False, "type_mismatch"

        key = self._pity_key(mount)
        streak = self._fail_streak.get(key, 0)
        rate = self.get_evolve_rate(mount.level)
        success = streak + 1 >= self.pity_threshold or self.rng.random() < rate

        if success:
            self._fail_streak[key] = 0
            return True, self.get_evolve_form(target_type, mount.attribute)
        self._fail_streak[key] = streak + 1
        return False, self.get_failure_refund()

    # 7. 血脉: 按父母血统计算, 纯种有加成
    def calculate_bloodline(self, parent1: float, parent2: float) -> float:
        bloodline = (parent1 + parent2) / 2
        if parent1 >= PURE_BLOODLINE_THRESHOLD and parent2 >= PURE_BLOODLINE_THRESHOLD:
            bloodline = min(1.0, bloodline + PURE_BLOODLINE_BONUS)
        return bloodline

    # 8. 类型限制: 陆地坐骑只能进化成陆地圣兽
    def can_evolve_type(self, from_type: str, to_type: str) -> bool:
        allowed = ALLOWED_TYPE_EVOLUTION.get(from_type, {from_type})
        return to_type in allowed

    # 9. 进化后原坐骑消耗
    def is_mount_consumed(self) -> bool:
        return True
