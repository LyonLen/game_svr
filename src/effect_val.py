import dataclasses
import math


@dataclasses.dataclass
class EffectVal(object):
    __doc__ = """
EffectVal设计思想：
1 满足多模块能够对着同一个游戏数值效果累积数值，并具有上限。这种场景会出现的问题如下：
    比如：a模块+2000，b模块+1000，limit为1500；对外表现，则是1500；这里是不识别变更值的，固然算变更值性能更好
        但是，为了代码的简单，这里每次都重复计算，_value会存储一个溢出值。b模块移除，则表现在外部还会为1500，因为a模块足以填充满limit。
2 _module_rates和_global_rate的设计，满足了游戏策划的扩展性设计：
    对某个模块的所有效果加成；
    对此效果，无视模块，统统加成。

策划可设计的效果举例：
    1 攻击力数值加成10；
    2 攻击力百分比加成10%；
    3 攻击力数值和百分比混合加成的结果，受limit限制，子模块无需关注是否溢出，算出来多少往里根据数值/百分比累积即可；
    4 “基于某个模块”的攻击力加成百分比。
"""

    _value: float = 0
    _limit: int = 0
    _module_values: dict = dataclasses.field(default_factory=dict)
    _module_rates: dict = dataclasses.field(default_factory=dict)
    _global_rate: float = 1.0

    def change_value(self, module_name, chg_value: float):
        self._change(self._module_values, module_name, chg_value)

    def change_module_rate(self, module_name, chg_value: float):
        self._change(self._module_rates, module_name, chg_value)

    def remove_module(self, module_name):
        self._module_values.pop(module_name)
        self._module_rates.pop(module_name)
        self._recalc_value()

    def _change(self, module_dict, module_name, chg_value: float):
        self._module_values.setdefault(module_name, 0)
        self._module_rates.setdefault(module_name, 1.0)
        if chg_value < 0 and abs(chg_value) > module_dict[module_name]:
            raise Exception(f"module_name={module_name} chg_value={chg_value} exceeds {module_dict}")
        module_dict[module_name] += chg_value
        self._recalc_value()

    def change_global_rate(self, chg_value: float):
        if chg_value < 0 and abs(chg_value) > self._global_rate:
            raise Exception(f"change value={chg_value} exceeds module rates={self._global_rate}")
        self._global_rate += chg_value
        self._recalc_value()

    def _recalc_value(self):
        self._value = 0
        # 当然可以基于change，不用重算，但是换来的代价就是代码更加复杂
        # 比如: global的变更，得循环所有模块; 单模块的rate、base变更，确实可以做到单模块变更; 整个模块的移除，也是一个逻辑。
        for module_name, module_value in self._module_values.items():
            self._value += module_value * self._module_rates[module_name] * self._global_rate

    @property
    def value(self):
        return min(math.floor(self._value), self._limit) if self._limit else math.floor(self._value)

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit: int):
        self._limit = limit
