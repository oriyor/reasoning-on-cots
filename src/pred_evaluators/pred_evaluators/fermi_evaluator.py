from copy import deepcopy

import numpy as np
import pint

ureg = pint.UnitRegistry(system="mks", autoconvert_offset_to_baseunit=True)
# ureg.load_definitions("data/test_datasets/fermi/units.txt")


class FermiEvaluator:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def convert_units(self, answer):
        if type(answer) == str:
            try:
                # try converting units
                original_pint = ureg(answer)
            except:
                # keelp as is, can be num or string
                original_pint = answer
        else:
            original_pint = answer
        # if it's still string, try parsing
        if type(original_pint) == str:
            try:
                original_pint = float(original_pint.replace("$", "").split(" ")[0])
            except:
                original_pint = None
        if original_pint is None:
            return None, None
        # this means it's ureg
        if type(original_pint) not in [float, int]:
            try:
                converted_pint = original_pint.to_base_units()
            except:
                converted_pint = deepcopy(original_pint)
            return converted_pint.magnitude, converted_pint.units
        else:
            return original_pint, None

    def evaluate(self, pred, gold) -> str:
        pred = pred.split("=")[-1]
        gold_split, pred_split = gold.split(" "), pred.split(" ")
        if len(gold_split) > 1 and len(pred_split) == 1:
            gold_split_measurement_value = gold_split[-1]
            if not pred_split[-1].endswith(gold_split_measurement_value):
                pred += " " + gold_split_measurement_value

        y, y_hat = self.convert_units(pred)[0], self.convert_units(gold)[0]
        conversion_dict = {"million": 1e6, "trillion": 1e9}
        for k, v in conversion_dict.items():
            if k in pred:
                converted_pred = self.convert_units(pred.replace(k, "".strip()))[0]
                if converted_pred is not None:
                    y = converted_pred * v

        if type(y) not in [int, float, np.float64] or type(y_hat) not in [
            int,
            float,
            np.float64,
        ]:
            return 0
        if y is None or y_hat is None:
            return 0
        if y < 0 or y_hat < 0:
            return 0
        if y == 0 and y_hat == 0:
            return 1
        elif y == 0 or y_hat == 0:
            return max(0, 1 - np.abs(np.log10(np.abs(y - y_hat))))
        # elif y/y_hat == 0:
        #     return 0
        try:
            return max(0, 3 - np.abs(np.log10(y / y_hat))) / 3
        except:
            return 0
