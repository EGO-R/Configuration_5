import zlib
import os
from graphviz import Digraph
import argparse

def find_object(git_dir, obj_hash):
    path = os.path.join(git_dir, 'objects', obj_hash[:2], obj_hash[2:])
    with open(path, 'rb') as f:
        return zlib.decompress(f.read())


def parse_tree(tree_data):
    i = tree_data.index(b'\x00') + 1
    entries = []
    while i < len(tree_data):
        start = i
        i = tree_data.index(b'\x00', start)
        fields = tree_data[start:i].decode().split(' ', 2)
        entries.append((fields[0], fields[1], tree_data[i+1:i+21].hex()))
        i += 21
    return entries

def print_tree(git_dir, tree_hash, prev_path):
    tree_data = find_object(git_dir, tree_hash)
    for mode, path, hash in parse_tree(tree_data):
        arr.append(f'{prev_path}/{path}')
        if mode == '40000':  # it's a tree, recurse into it
            print_tree(git_dir, hash, prev_path + "/" + path)

def cut_tree(line):
    while "tree " in line[1:]:
        line = line[1:]
    return line

def print_commit_tree(git_dir, commit_hash):
    commit_data = find_object(git_dir, commit_hash).decode()
    for line in commit_data.split('\n'):
        if 'tree ' in line:
            line = cut_tree(line)
            print_tree(git_dir, line.split()[1], '')
            break


def take_in_quotes(string):
    if "-" in string:
        return f"\"{string}\""
    return string


def create_graph(file_paths):
    graph = Digraph(comment='File Tree', strict=True)

    for path in file_paths:
        parts = path.split('/')
        parts = list(filter(None, parts))
        for i in range(len(parts)-1):
            if not (f"\t{take_in_quotes(parts[i])} -> {take_in_quotes(parts[i + 1])}\n" in graph.body):
                graph.edge(parts[i], parts[i+1])

    graph.render('file_graph.gv', view=True)
    print(graph)





parser = argparse.ArgumentParser(description="Visualizer")
parser.add_argument('root', help="Path to .git package.")
parser.add_argument('hash', help="Hash of commit.")

args = parser.parse_args()
args.root = args.root.replace('\\', '/')

arr = []
print_commit_tree(args.root, args.hash)
# print_commit_tree('C:/Users/Egor/IdeaProjects/Java-3rd-term/.git', '8e02e57aeef9172f7e652e2992cd6731d15b4cbd')
# print_commit_tree('C:/Users/Egor/Documents/2_курс/Processors/.git', '637d263220a757d04fceca4f10fa7660b812644f')
create_graph(arr)

