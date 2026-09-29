"""坐骑进化与圣兽系统 - 红态测试"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mount.evolve import EvolveSystem, Mount

class TestEvolveCondition:
    def test_low_level_cannot_evolve(self):
        es = EvolveSystem()
        m = Mount("m1", "horse", level=1, quality="common")
        assert es.can_evolve(m) == False

class TestEvolveForm:
    def test_different_types_evolve_differently(self):
        es = EvolveSystem()
        f1 = es.get_evolve_form("land")
        f2 = es.get_evolve_form("flying")
        assert f1 != f2

class TestSacredSkill:
    def test_different_beasts_different_skills(self):
        es = EvolveSystem()
        s1 = es.get_sacred_skill("phoenix")
        s2 = es.get_sacred_skill("dragon")
        assert s1 != s2

class TestEvolveMaterial:
    def test_different_types_use_different_materials(self):
        es = EvolveSystem()
        m1 = es.get_evolve_material("fire")
        m2 = es.get_evolve_material("water")
        assert m1 != m2

class TestEvolveRate:
    def test_high_level_evolve_can_fail(self):
        es = EvolveSystem()
        r1 = es.get_evolve_rate(1)
        r10 = es.get_evolve_rate(10)
        assert r10 < r1

class TestFailureRefund:
    def test_failure_refunds_materials(self):
        es = EvolveSystem()
        refund = es.get_failure_refund()
        assert refund > 0

class TestBloodline:
    def test_pure_parents_give_purer_offspring(self):
        es = EvolveSystem()
        b1 = es.calculate_bloodline(1.0, 1.0)
        b2 = es.calculate_bloodline(0.0, 0.0)
        assert b1 > b2

class TestTypeRestriction:
    def test_land_mount_cannot_evolve_flying(self):
        es = EvolveSystem()
        assert es.can_evolve_type("land", "flying") == False

class TestMountConsumed:
    def test_original_mount_is_consumed(self):
        es = EvolveSystem()
        assert es.is_mount_consumed() == True
