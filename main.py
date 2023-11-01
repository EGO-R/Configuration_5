import os
import zlib

def read_object(sha1):
    path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
    with open(path, 'rb') as f:
        data = zlib.decompress(f.read())
        return data.decode()

def read_tree(tree_sha1):
    tree = read_object(tree_sha1)
    for line in tree.splitlines():
        mode, type, sha1, name = line.split(' ', 3)
        if type == 'blob':
            print(f'blob {sha1} {name}')
        elif type == 'tree':
            print(f'tree {sha1} {name}')
            read_tree(sha1)

def read_commit(commit_sha1):
    commit = read_object(commit_sha1)
    for line in commit.splitlines():
        if line.startswith('tree '):
            tree_sha1 = line.split(' ')[1]
            read_tree(tree_sha1)

commit_sha1 = 'ef691122727b76e82c85a040066d3730fab20b3d'
read_commit(commit_sha1)

