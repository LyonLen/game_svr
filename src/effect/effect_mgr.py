import json

from src.effect.effect_val import EffectVal


class EffectMgr:
    _EFFECT_DICT = {}

    @staticmethod
    def init():
        with open("test.json") as f:
            effect_conf_dict = json.load(f)
            for one_effect in effect_conf_dict["effects"]:
                EffectMgr._EFFECT_DICT[one_effect["effect_id"]] = EffectVal(
                    _limit=one_effect.get("effect_limit", 0)
                )

    @staticmethod
    def get_effect(effect_id) -> EffectVal:
        return EffectMgr._EFFECT_DICT[effect_id]


if __name__ == "__main__":
    EffectMgr.init()
    EffectMgr.get_effect(1).change_value("pet", 1)
    EffectMgr.get_effect(1).change_value("rune", 300)
    print(EffectMgr.get_effect(1).value)
    print(EffectMgr._EFFECT_DICT)
