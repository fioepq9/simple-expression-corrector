import os
import shutil


def get_new_filepath(out_dir, label):
    filepath = f"{out_dir}/{label}.jpg"
    if os.path.exists(filepath):
        i = 1
        _, suffix = os.path.splitext(filepath)
        while True:
            filepath = f"{out_dir}/{label}_{i}{suffix}"
            if not os.path.exists(filepath):
                break
            i = i + 1
    return filepath


if __name__ == "__main__":
    label_path = ["evalImageSet_old/eval.txt", "./image_1/label.txt", "./image_2/label.txt", "./image_3/label.txt"]
    out_image_dir = "evalImageSet"
    out_label_path = "eval.txt"

    if not os.path.exists(out_image_dir):
        os.mkdir(out_image_dir)

    # read
    label_txt = []
    for i, path in enumerate(label_path):
        with open(path, mode='r', encoding='utf-8') as f:
            label_txt.append(f.readlines())

    # merge
    brackets_cnt, too_many_equal_cnt = 0, 0
    filepath, label = [], []
    for i in range(max([len(txt) for txt in label_txt])):
        for j in range(len(label_txt)):
            if i >= len(label_txt[j]):
                continue
            txt: list[str] = label_txt[j]
            p, l = txt[i].strip().split('\t') 
            if "(" in l or ")" in l:
                brackets_cnt += 1
                continue
            if l.count('=') >= 2:
                too_many_equal_cnt += 1
                continue
            filepath.append(p)
            label.append(l)

    # write
    print(f"括号数量: {brackets_cnt}, 两个以上等号数量: {too_many_equal_cnt}")
    print(f"file number = {len(filepath)}")
    i = 1
    for p, l in zip(filepath, label):
        try:
            old_p = p
            new_p = get_new_filepath(out_image_dir, l)
            shutil.copyfile(old_p, new_p)
            # print(f"{i}: {p} -> {new_p}")
            with open(out_label_path, mode="a+", encoding="utf-8") as f:
                f.write(f"{new_p}\t{l}\n")
            if not os.path.exists(new_p):
                print(f"{i}: error in {new_p}")
            i += 1
        except Exception as e:
            with open('log.txt', mode='a+', encoding='utf-8') as f:
                f.write(f"{p}: {e}\n")
                print('Reason:', e)
            continue


