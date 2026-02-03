import glob
import os
import shutil

paths = glob.glob("./frames/*")

sorted_paths = sorted(paths)

bb_tree = []

for path in sorted_paths:
    basename = os.path.basename(path)
    if basename == "classes.txt":
        continue
    if basename.endswith(".txt"):
        bb_tree.append(path[:-4])
    
# copy to dir

for i in range(len(bb_tree)):
    shutil.copy(bb_tree[i] + ".jpg", f"./data/images/frame_{i:06d}.jpg")
    shutil.copy(bb_tree[i] + ".txt", f"./data/labels/frame_{i:06d}.txt")