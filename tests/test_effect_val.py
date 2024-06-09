import math
import unittest

from src.effect_val import EffectVal


class TestEffectVal(unittest.TestCase):

    def test_effect_val(self):
        print("=" * 6, "基础测试", "=" * 6)
        effect_val = EffectVal()
        effect_val.change_value("pet", 100)
        assert effect_val.value == math.floor(100)
        try:
            effect_val.change_value("pet", -101)
        except Exception as e:
            print(e)
            assert True
        effect_val.change_module_rate("pet", 0.1)
        assert effect_val.value == math.floor(100 * (1 + 0.1))
        try:
            effect_val.change_module_rate("pet", -1.2)
        except Exception as e:
            print(e)
            assert True
        effect_val.change_value("rune", 200)
        assert effect_val.value == math.floor(100 * (1 + 0.1) + 200)
        effect_val.change_module_rate("rune", -0.2)
        assert effect_val.value == math.floor((100 * (1 + 0.1)) + (200 * (1 - 0.2)))
        effect_val.limit = 100
        assert effect_val.value == 100
        effect_val.limit = 0
        effect_val.change_global_rate(-0.2)
        assert effect_val.value == math.floor(((100 * (1 + 0.1)) + (200 * (1 - 0.2))) * 0.8)

    def test_effect_val_no_limit(self):
        print("=" * 6, "无上限单模块配置", "=" * 6)
        effect_val_no_limit = EffectVal()
        effect_val_no_limit.change_value("pet", 100)
        effect_val_no_limit.change_value("pet", 200)
        effect_val_no_limit.change_value("pet", 300)
        print("无上限单模块配置", effect_val_no_limit.value)
        assert effect_val_no_limit.value == 100 + 200 + 300

    def test_effect_val_with_limit(self):
        # 有上限单模块配置
        print("=" * 6, "有上限单模块配置", "=" * 6)
        effect_val_limit = EffectVal(_limit=100)
        effect_val_limit.change_value("pet", 100)
        effect_val_limit.change_value("pet", 200)
        effect_val_limit.change_value("pet", 300)
        assert effect_val_limit.value == 100
        print("有上限单模块配置", effect_val_limit.value)
        effect_val_limit.change_value("pet", -200)
        assert effect_val_limit.value == 100
        print("有上限单模块配置, -200, 因为其它模块还有数值，所以要补上\n", effect_val_limit, "\n effect_val.value:",
              effect_val_limit.value)
        effect_val_limit.change_value("pet", -300)
        assert effect_val_limit.value == 100
        print("有上限单模块配置, -300, 因为其它模块还有数值，所以要补上\n", effect_val_limit, "\n effect_val.value:",
              effect_val_limit.value)
        effect_val_limit.change_value("pet", -50)
        assert effect_val_limit.value == 50
        print("有上限单模块配置, -50, 已经不够上限了，所以这里会变成50\n", effect_val_limit, "\n effect_val.value:",
              effect_val_limit.value)

    def test_effect_val_no_limit_multi_module(self):
        # 无上限多模块配置
        print("=" * 6, "无上限多模块配置", "=" * 6)
        effect_val_no_limit_multi_module = EffectVal()
        effect_val_no_limit_multi_module.change_value("pet", 100)
        effect_val_no_limit_multi_module.change_value("rune", 200)
        effect_val_no_limit_multi_module.change_value("pet", 300)
        effect_val_no_limit_multi_module.change_value("spell", 300)
        assert effect_val_no_limit_multi_module.value == 100 + 200 + 300 + 300
        print("无上限多模块配置", effect_val_no_limit_multi_module.value)

    def test_effect_val_limit_multi_module(self):
        print("=" * 6, "有上限多模块配置", "=" * 6)
        effect_val_limit_multi_module = EffectVal()
        effect_val_limit_multi_module.limit = 400
        effect_val_limit_multi_module.change_value("pet", 100)
        assert effect_val_limit_multi_module.value == 100
        effect_val_limit_multi_module.change_value("rune", 200)
        assert effect_val_limit_multi_module.value == 300
        effect_val_limit_multi_module.change_value("pet", 300)
        assert effect_val_limit_multi_module.value == 400
        effect_val_limit_multi_module.change_value("spell", 300)
        assert effect_val_limit_multi_module.value == 400
        print("有上限多模块配置", effect_val_limit_multi_module.value)
        effect_val_limit_multi_module.change_value("spell", -300)
        assert effect_val_limit_multi_module.value == 400
        print("有上限多模块配置, -300, 因为其它模块还有数值，所以要补上\n", effect_val_limit_multi_module,
              "\n effect_val.value:", effect_val_limit_multi_module.value)
        effect_val_limit_multi_module.change_value("pet", -250)
        assert effect_val_limit_multi_module.value == 350
        print("有上限多模块配置, -250, 已经不够上限了，所以这里会变成350\n", effect_val_limit_multi_module,
              "\n effect_val.value:", effect_val_limit_multi_module.value)

    def test_effect_remove_module(self):
        # 删模块测试
        print("=" * 6, "删模块测试", "=" * 6)
        effect_val_del_one_module = EffectVal()
        effect_val_del_one_module.change_value("pet", 100)
        effect_val_del_one_module.change_value("rune", 200)
        effect_val_del_one_module.change_value("pet", 300)
        effect_val_del_one_module.change_value("spell", 300)
        print("删模块测试", effect_val_del_one_module)
        effect_val_del_one_module.remove_module("pet")
        assert effect_val_del_one_module.value == 500
        print("删模块测试", effect_val_del_one_module)
        print("删模块测试", effect_val_del_one_module.value)