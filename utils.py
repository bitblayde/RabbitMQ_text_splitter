from os import listdir, rmdir, makedirs
from os.path import isfile, join, exists

def get_filename(root):
    onlyfiles = [join(root, f) for f in listdir(root) if isfile(join(root, f))]
    return onlyfiles

def serialize(texts, root):
    if not exists(root):
        makedirs(root)

    for i in range(len(texts)):
        filename = f"file_{i}.txt"
        path_files = join(root, filename)
        
        with open(path_files, "w") as f:
            f.write(texts[i])

