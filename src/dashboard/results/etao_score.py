from parameters.parameters import Parameters

class eTAOScore:
    #etao_max = 2 * sum([max(Parameters.ETAO_VALUE_CORRESPONDANCE[_].values) for _ in "eTAO"])
    #etao_min = 2 * sum([min(Parameters.ETAO_VALUE_CORRESPONDANCE[_].values) for _ in "eTAO"])


    def __init__(self):
        pass

    @staticmethod
    def compute(ocular_dryness, left_eye, right_eye, surgery):
        # Compute eTAO
        etao_right = (right_eye.e_value + right_eye.T_value + right_eye.A_value + right_eye.O_value)/4.
        etao_left = (left_eye.e_value + left_eye.T_value + left_eye.A_value + left_eye.O_value)/4.
        etao = (etao_right + etao_left)/2.

        # etao max -> 9.25
        divider = 10
        etao = etao/divider*9.

        # Add ocular dryness intensity (and max to 0)
        if ocular_dryness.intensity in [7, 8]:
            etao += 0.5
        elif ocular_dryness.intensity in [9, 10]:
            etao += 1.

        # eTAO change relatively to surgery
        if surgery.lasik:
            if etao < 4:
                etao = etao * 1.4
            else:
                etao = etao * 1.25
        if surgery.iso:
            if etao < 4:
                etao = etao * 1.35
            else:
                etao = etao * 1.2
        if surgery.blepharo:
            if etao < 4:
                etao = etao * 1.25
            else:
                etao = etao * 1.15

        if etao > 12:
            etao_ = min(etao, 10)
        elif etao > 10:
            etao_ = 9.83
        else:
            etao_ = etao
        etao = etao_

        return etao
