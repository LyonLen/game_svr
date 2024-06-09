import dataclasses
import math


@dataclasses.dataclass
class EffectVal(object):
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
