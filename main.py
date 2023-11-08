import zlib
import os

def find_object(git_dir, obj_hash):
    path = os.path.join(git_dir, 'objects', obj_hash[:2], obj_hash[2:])
    with open(path, 'rb') as f:
        return zlib.decompress(f.read())

def parse_tree(tree_data):
    i = 0
    entries = []
    while i < len(tree_data):
        start = i
        i = tree_data.index(b'\x00', start)
        fields = tree_data[start:i].decode().split(' ', 2)
        entries.append((fields[0], fields[1], tree_data[i+1:i+21].hex()))
        i += 21
    return entries

def print_tree(git_dir, tree_hash):
    tree_data = find_object(git_dir, tree_hash)
    for mode, path, hash in parse_tree(tree_data):
        print(f'{mode} {path} {hash}')
        if mode == '040000':  # it's a tree, recurse into it
            print_tree(git_dir, hash)

def print_commit_tree(git_dir, commit_hash):
    commit_data = find_object(git_dir, commit_hash).decode()
    for line in commit_data.split('\n'):
        if line.startswith('tree '):
            print_tree(git_dir, line.split()[1])
            break

print_commit_tree('.git', 'commit_hash')
