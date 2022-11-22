import os
import sys
from collections import defaultdict
from functools import cmp_to_key
import json
import copy
import shutil
xks = defaultdict(list, [])

MAX_SPLIT = 20
input_dir = sys.argv[1]
output_dir = sys.argv[2]
name_map = {
        "yuwen": "语文",
        "shuxue": "数学",
        "yingyu": "英语",
        "wuli": "物理",
        "huaxue": "化学",
        "shengwu": "生物"

}

def detect_type(name):
    if "文数" in name:
        return None
    if "理数" in name or "数学" in name :
        return "shuxue"
    if "英语" in name:
        return "yingyu"
    if "语文" in name:
        return "yuwen"
    if "物理" in name:
        return "wuli"
    if "化学" in name:
        return "huaxue"
    if "生物" in name:
        return "shengwu"
def is_ans(name):
    if "答案" in name:
        return True
    elif '试题' in name:
        return False
    else:
        return False

def fmt_name(name):
    return name.replace("（", "(").replace("）", ")").replace("'", "").replace("\"", "")


def key_func(a):
    return 1 if is_ans(a) else 0


x = sorted(os.listdir(input_dir))
skf = {}
for i in x:
    sub_dir = os.path.join(input_dir, i)
    if os.path.isdir(sub_dir):
        xkn = {}
        #print(sub_dir)
        sub_x = sorted(os.listdir(sub_dir), key = key_func, reverse=False)
        if len(sub_x) > 0:
            for si in sub_x:
                ntype = detect_type(si)
                if ntype:
                    xks[ntype].append((i, si, is_ans(si)))

        for k, xi in xks.items():
            if len(xks[k] ) > MAX_SPLIT:
                if k in skf:
                    skf[k].append(copy.deepcopy(xks[k]))
                else:
                    skf[k] = [copy.deepcopy(xks[k])]
                xks[k] = []





for k, v in skf.items():
    #print(k, len(v), skf[k])
    print('-=----------------------------------------')
    print( k, len(v))
    print('-=----------------------------------------')

    for idx in range(len(v)):
        xk_id = "%s_%d" % (k, idx)
        xk_id_dir = os.path.join(output_dir, xk_id)
        if not os.path.exists(xk_id_dir):
            os.makedirs(xk_id_dir)
        names = []
        for (d, f, _) in v[idx]:
            print(xk_id, d, f)
            fname = fmt_name(f)
            names.append(fname)
            if_path = os.path.join(input_dir, d, f)
            of_path = os.path.join(xk_id_dir, fname)
            shutil.copy(if_path, of_path)
        with open(os.path.join(xk_id_dir, "file.txt"), "w") as f:
            f.write(json.dumps({"files": names, "name": name_map[k], "index": idx + 1}))



    
    





    #for i in v:
    #    print("..", i)
