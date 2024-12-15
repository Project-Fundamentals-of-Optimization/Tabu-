u= {
    "all_opti":{
        "input5.txt":[360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 390, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 390, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 390, 360, 360, 360, 360],
        "input10.txt":[570, 550, 550, 560, 570, 550, 570, 560, 560, 560, 550, 560, 560, 580, 550, 560, 550, 550, 550, 550, 560, 560, 560, 550, 580, 560, 570, 550, 570, 550, 560, 550, 550, 560, 560, 560, 570, 550, 550, 550, 570, 570, 550, 580, 560, 560, 550, 570, 560, 570],
        "input100.txt":[3400, 3300, 3330, 3360, 3440, 3330, 3330, 3420, 3390, 3380, 3430, 3320, 3390, 3330, 3330, 3380, 3420, 3320, 3330, 3330, 3370, 3400, 3410, 3350, 3370, 3390, 3370, 3390, 3360, 3370, 3380, 3260, 3340, 3330, 3390, 3350, 3320, 3390, 3330, 3340, 3320, 3320, 3350, 3400, 3380, 3330, 3380, 3410, 3260, 3360],  
        "input20010.txt":[4640, 4550, 4570, 4450, 4560, 4610, 4640, 4570, 4560, 4680, 4590, 4610, 4640, 4580, 4580, 4640, 4650, 4560, 4670, 4590, 4570, 4550, 4580, 4610, 4610, 4460, 4580, 4740, 4620, 4580, 4540, 4540, 4570, 4640, 4600, 4660, 4630, 4580, 4710, 4600, 4580, 4540, 4600, 4490, 4560, 4570, 4480, 4620, 4600, 4700, 4490, 4620, 4570, 4680, 4560],
        "input20020.txt":[3590, 3550, 3440, 3540, 3530, 3590, 3550, 3570, 3570, 3650, 3560, 3560, 3530, 3520, 3500, 3620, 3550, 3540, 3570, 3550, 3550, 3510, 3470, 3450, 3490, 3540, 3460, 3520, 3510, 3610, 3590, 3590, 3570, 3540, 3620, 3570, 3540, 3530, 3580, 3570, 3510, 3530, 3520, 3510, 3500, 3450, 3500, 3560, 3530, 3580],
        
        "input400.txt":[3500, 3580, 3550, 3490, 3510, 3540, 3510, 3520, 3570, 3460, 3530, 3480, 3480, 3540, 3480, 3440, 3500, 3550, 3550, 3570, 3500, 3570, 3510, 3500, 3530, 3500, 3540, 3530, 3540, 3540, 3440, 3560, 3450, 3510, 3520, 3550, 3560, 3600, 3560, 3530, 3530, 3540, 3550, 3580, 3520, 3490, 3490, 3530, 3520, 3490],
        "input500.txt":[3580, 3530, 3620, 3620, 3530, 3540, 3570, 3540, 3530, 3550, 3530, 3560, 3600, 3600, 3560, 3620, 3650, 3640, 3630, 3580, 3510, 3590, 3580, 3610, 3610, 3550, 3590, 3590, 3530, 3610, 3460, 3570, 3540, 3620, 3560, 3590, 3660, 3570, 3610, 3580, 3570, 3610, 3530, 3570, 3620, 3580, 3580, 3580, 3570, 3580],
        "input700.txt":[3630, 3600, 3590, 3540, 3550, 3640, 3600, 3660, 3570, 3580, 3570, 3580, 3620, 3540, 3620, 3620, 3630, 3660, 3630, 3630, 3550, 3650, 3590, 3600, 3590, 3580, 3640, 3600, 3600, 3650, 3620, 3630, 3600, 3640, 3580, 3630, 3640, 3580, 3600, 3580, 3670, 3580, 3600, 3610, 3630, 3570, 3580, 3640, 3590, 3600],
        "input900.txt":[3590, 3680, 3630, 3630, 3620, 3670, 3710, 3690, 3690, 3650, 3650, 3690, 3700, 3690, 3640, 3670, 3630, 3670, 3650, 3640, 3660, 3750, 3690, 3670, 3730, 3690, 3650, 3700, 3670, 3700, 3660, 3650, 3690, 3620, 3650, 3700, 3690, 3640, 3690, 3720, 3600, 3640, 3670, 3630, 3670, 3690, 3670, 3690, 3630, 3650],
        "input1000.txt":[3620, 3700, 3610, 3660, 3640, 3680, 3640, 3690, 3660, 3580, 3670, 3610, 3650, 3660, 3670, 3700, 3670, 3640, 3680, 3610, 3660, 3660, 3590, 3650, 3600, 3620, 3630, 3650, 3670, 3610, 3690, 3650, 3600, 3580, 3650, 3640, 3700, 3580, 3640, 3660, 3590, 3680, 3680, 3670, 3640, 3680, 3630, 3640, 3680, 3660],
    }
}

import math

def calculate_stats(data):
    """
    Calculate the minimum, maximum, mean, and standard deviation of a list.
    
    Args:
        data (list): A list of numerical values.
    
    Returns:
        dict: A dictionary with keys 'min', 'max', 'mean', 'std' and their respective values.
    """
    if not data:  # Check if the list is empty
        return {"min": None, "max": None, "mean": None, "std": None}
    
    n = len(data)
    min_val = min(data)
    max_val = max(data)
    mean_val = sum(data) / n
    variance = sum((x - mean_val) ** 2 for x in data) / n  # Population variance
    std_val = math.sqrt(variance)
    
    return {"min": min_val, "max": max_val, "mean": mean_val, "std": std_val}

data = u["all_opti"]
for key, value in data.items():
    data[key] = calculate_stats(value)
    print(f"{key}:{data[key]}")


# s = r"""
# iter 0 of input/input20010.txt: in 236.40s with loss 4640
# iter 1 of input/input20010.txt: in 249.87s with loss 4550
# iter 2 of input/input20010.txt: in 219.84s with loss 4570
# iter 3 of input/input20010.txt: in 244.92s with loss 4450
# iter 4 of input/input20010.txt: in 235.54s with loss 4560
# iter 5 of input/input20010.txt: in 219.15s with loss 4610
# iter 6 of input/input20010.txt: in 247.89s with loss 4640
# iter 7 of input/input20010.txt: in 213.50s with loss 4570
# iter 8 of input/input20010.txt: in 231.64s with loss 4560
# iter 9 of input/input20010.txt: in 229.97s with loss 4680
# iter 10 of input/input20010.txt: in 241.32s with loss 4590
# iter 11 of input/input20010.txt: in 243.68s with loss 4610
# iter 12 of input/input20010.txt: in 244.09s with loss 4640
# iter 13 of input/input20010.txt: in 280.40s with loss 4580

# iter 0 of input/input20010.txt: in 217.31s with loss 4580
# iter 1 of input/input20010.txt: in 217.17s with loss 4640
# iter 2 of input/input20010.txt: in 205.65s with loss 4650
# iter 3 of input/input20010.txt: in 229.38s with loss 4560
# iter 4 of input/input20010.txt: in 219.62s with loss 4670
# iter 5 of input/input20010.txt: in 221.59s with loss 4590
# iter 6 of input/input20010.txt: in 221.82s with loss 4570
# iter 7 of input/input20010.txt: in 213.74s with loss 4550
# iter 8 of input/input20010.txt: in 246.42s with loss 4580
# iter 9 of input/input20010.txt: in 210.02s with loss 4610
# iter 10 of input/input20010.txt: in 204.85s with loss 4610
# iter 11 of input/input20010.txt: in 226.60s with loss 4460
# iter 12 of input/input20010.txt: in 232.68s with loss 4580
# iter 13 of input/input20010.txt: in 210.08s with loss 4740
# iter 14 of input/input20010.txt: in 224.75s with loss 4620
# iter 15 of input/input20010.txt: in 229.03s with loss 4580
# iter 16 of input/input20010.txt: in 207.35s with loss 4540
# iter 17 of input/input20010.txt: in 196.32s with loss 4540
# iter 18 of input/input20010.txt: in 213.96s with loss 4570
# iter 19 of input/input20010.txt: in 216.29s with loss 4640
# iter 20 of input/input20010.txt: in 220.09s with loss 4600
# iter 21 of input/input20010.txt: in 200.51s with loss 4660
# iter 22 of input/input20010.txt: in 204.99s with loss 4630
# iter 23 of input/input20010.txt: in 199.32s with loss 4580
# iter 24 of input/input20010.txt: in 233.21s with loss 4710


# iter 0 of input/input20010.txt: in 218.69s with loss 4600
# iter 1 of input/input20010.txt: in 204.85s with loss 4580
# iter 2 of input/input20010.txt: in 228.88s with loss 4540
# iter 3 of input/input20010.txt: in 213.94s with loss 4600
# iter 4 of input/input20010.txt: in 217.47s with loss 4490
# iter 5 of input/input20010.txt: in 211.30s with loss 4560
# iter 6 of input/input20010.txt: in 230.31s with loss 4570
# iter 7 of input/input20010.txt: in 221.16s with loss 4480
# iter 8 of input/input20010.txt: in 216.20s with loss 4620
# iter 9 of input/input20010.txt: in 236.29s with loss 4600
# iter 10 of input/input20010.txt: in 210.84s with loss 4700
# iter 11 of input/input20010.txt: in 218.70s with loss 4490
# iter 12 of input/input20010.txt: in 221.46s with loss 4620
# iter 13 of input/input20010.txt: in 213.41s with loss 4570
# iter 14 of input/input20010.txt: in 206.02s with loss 4680
# iter 15 of input/input20010.txt: in 231.30s with loss 4560"""

# s = [ss for ss in s.split("\n") if len(ss)>0 ]
# # print(s)
# s = [int(ss.split()[-1]) for ss in s]
# print(s)
