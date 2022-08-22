import numpy as np

def calc_meld(**kwargs):
    """
    Calculates the meld of a patient.
    """

    # Initialize variables
    krea = kwargs['krea']
    if krea < 1:
        krea = 1
    if krea > 4:
        krea = 4

    bili = kwargs["bilirubin"]
    if bili < 1:
        bili = 1
    
    inr = kwargs["inr"]
    if inr < 1:
        inr = 1

    meld = (
        10 * (
            0.957 * np.log(krea) +
            0.378 * np.log(bili) +
            1.12 * np.log(inr) +
            0.643
        )
    )

    if meld>40:
        meld = 40

    return meld


def calc_ranson_score(**kwargs):
    """
    Calculates the Ranson score of a patient.
    """

    wbc_1 = kwargs["wbc_1"]
    age = kwargs["age"]
    glucose = kwargs["glucose"]
    ast = kwargs["ast"]
    ldh = kwargs["ldh"]

    bun_1 = kwargs["bun_1"]
    bun_2 = kwargs["bun_2"]
    d_bun = bun_2 - bun_1

    hct_1 = kwargs["hct_1"]
    hct_2 = kwargs["hct_2"]
    d_hct = hct_2 - hct_1

    ca_2 = kwargs["ca_2"]

    art_o2 = kwargs["art_o2"]
    base_deficit = 24-kwargs["hco3"]

    req_fluid = kwargs["req_fluid"]

    

    return ranson_score
