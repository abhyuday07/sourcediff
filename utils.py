import os
import sys
import pprint
import json


class Node:
    def __init__(self, id, content, children, parent):
        self.id = id
        self.content = content
        tmp = content.split()
        if "FunctionDecl" in tmp:
            print(tmp)
        self.children = children
        self.parent = parent

    def add_child(self, id2):
        self.children.append(id2)

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'children': self.children,
            'parent': self.parent
        }, indent=4)


def get_AST(file_path):
    unique_id = 0
    node_dict = dict()
    node_dict[0] = Node(0, "root", [], 0)
    cmd = "clang -Xclang -ast-dump -fsyntax-only -fno-diagnostics-color %s | sed -E 's/\|/ /g' | sed -E 's/-/ /g' | sed -E 's/`/ /g' | sed -E 's/0x[A-Fa-f0-9]+//g' | sed -E 's/line:[0-9]*:[0-9]*//g' | sed -E 's/<%s[^>]*>//g'" % (
        file_path, file_path.split('/')[-1][:-2])
    lines = os.popen(cmd).read().split('\n')[:-1]
    curr_indent = 0
    prev_indent = 0
    stack = [0]
    parent = unique_id
    first_time = True
    for line in lines:
        present = line.lstrip(' ')
        curr_indent = len(line) - len(present)
        if(curr_indent == 0 and first_time):  # Base case
            first_time = False
            parent = stack[-1]
            unique_id += 1
            node_dict[0].add_child(unique_id)
            node_dict[unique_id] = Node(unique_id, present, [], 0)
            stack.append(unique_id)
            parent = unique_id

        elif(curr_indent > prev_indent):  # Child Case
            unique_id += 1
            stack.append(unique_id)
            node_dict[parent].add_child(unique_id)
            node_dict[unique_id] = Node(unique_id, present, [], parent)
            parent = unique_id
        else:
            remove_cnt = (prev_indent - curr_indent + 2) // 2
            for _ in range(0, remove_cnt):
                stack.pop()
            parent = stack[-1]
            unique_id += 1
            stack.append(unique_id)
            node_dict[parent].add_child(unique_id)
            node_dict[unique_id] = Node(unique_id, present, [], parent)
            parent = unique_id
        prev_indent = curr_indent
    return node_dict


def is_funcs_different(file_1_ast, file_2_ast, func_1_node, func_2_node):
    return False


def get_diff_files(file_path_1, file_path_2):
    # Create list to store differences
    diff_functions = [[], []]
    # Get ast of both the files
    file_1_ast = get_AST(file_path_1)
    file_2_ast = get_AST(file_path_2)
    # Retrieve the function declaration nodes from both the files and sort them
    file_1_functions = sorted([x for x in file_1_ast[1].children if "FunctionDecl" in file_1_ast[x].name], key = lambda x: file_1_ast[x].name)
    file_2_functions = sorted([x for x in file_2_ast[1].children if "FunctionDecl" in file_2_ast[x].name], key = lambda x: file_2_ast[x].name)
    # Retrieve same functions and different functions by traversing on both the list like merge sort
    m, n = len(file_1_functions), len(file_2_functions)
    mi, ni = 0, 0
    while(mi < m or ni < n):
        if mi == m and ni == n:
            break
        # Compare the name of both the functions
        if mi == m:
            diff_functions[1].append(file_2_ast[file_2_functions[ni]].name)
            ni += 1
        elif ni == n:
            diff_functions[0].append(file_1_ast[file_1_functions[mi]].name)
            mi += 1
        elif file_1_ast[file_1_functions[mi]].name == file_2_ast[file_2_functions[ni]].name:
            # Check if functions are differnt 
            if is_funcs_different(file_1_ast, file_2_ast, file_1_functions[mi], file_2_functions[ni]):
                # Add in difference list
                diff_functions[0].append(file_1_ast[file_1_functions[mi]].name)
                diff_functions[1].append(file_2_ast[file_2_functions[ni]].name)
            mi += 1
            ni += 1
        elif file_1_ast[file_1_functions[mi]].name < file_2_ast[file_2_functions[ni]].name:
            diff_functions[0].append(file_1_ast[file_1_functions[mi]].name)
            mi += 1
        else:
            diff_functions[1].append(file_2_ast[file_2_functions[ni]].name)
            ni += 1
    return diff_functions
    

# Test function
if __name__ == "__main__":

    # Test for the ast generator
    file_path = sys.argv[1]
    pp = pprint.PrettyPrinter(indent=4)
    ast = get_AST(file_path)
    for x in ast:
        if "FunctionDecl" in str(ast[x]):
            print(ast[x])

    # # Test for file_diff
    # print(get_diff_files(sys.argv[1], sys.argv[2]))

# If a function is extract same in previous version, even then the name of function will change if it is used in one of the version and not used in the other version
# How to get function name