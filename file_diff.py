import os
import subprocess
import sys
import re
import time
import json
import decimal
import copy

class Node:
	def __init__(self, id, name, children, parent):
		self.id = id
		self.name = name
		self.children = children
		self.parent = parent
	
	def add_child(self, id2):
		self.children.append(id2)


# Increase recurse limit
sys.setrecursionlimit(2000)


def get_AST(filename):
	unique_id = 0
	node_dict = dict()
	node_dict[0] = Node(0, "root", [], 0)
	cmd = "clang -Xclang -ast-dump -fsyntax-only -fno-diagnostics-color %s | sed -E 's/\|/ /g' | sed -E 's/-/ /g' | sed -E 's/`/ /g' | sed -E 's/0x[A-Fa-f0-9]+//g' | sed -E 's/line:[0-9]*:[0-9]*//g' | sed -E 's/<%s[^>]*>//g'" % (filename, filename.split('/')[-1][:-2])
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

		elif(curr_indent > prev_indent): # Child Case
			unique_id += 1
			stack.append(unique_id)
			node_dict[parent].add_child(unique_id)
			node_dict[unique_id] = Node(unique_id, present, [], parent)
			parent = unique_id
		else:
			remove_cnt = (prev_indent - curr_indent + 2) // 2
			for _ in range(0,remove_cnt):
				stack.pop()
			parent = stack[-1]
			unique_id += 1
			stack.append(unique_id)
			node_dict[parent].add_child(unique_id)
			node_dict[unique_id] = Node(unique_id, present, [], parent)
			parent = unique_id
		prev_indent = curr_indent
	return node_dict

# Changes
# Removed line number and addresses
# Addresses are removed because they got change everytime
# Line number is removed because if we add a number in the middle then everything after it will change

diff_list = dict()
diff_list["Addition in AST1"] = []
diff_list["Addition in AST2"] = []
diff_list["Modification"] = []
def get_diff(tree1, tree2, rootNode1, rootNode2):
	# print "Comparing %s and %s" % (tree1[rootNode1], tree2[rootNode2])
	global diff_list
	tree1_root_children = sorted(tree1[rootNode1].children, key=lambda x: tree1[x].name)
	tree2_root_children = sorted(tree2[rootNode2].children, key=lambda x: tree2[x].name)

	tree1_root_children_names = [tree1[x].name for x in tree1_root_children]
	tree2_root_children_names = [tree2[x].name for x in tree2_root_children]

	if tree1_root_children_names == tree2_root_children_names:
		for iroot1, iroot2 in zip(tree1_root_children, tree2_root_children):
			if (iroot1 in tree1) and (iroot2 in tree2):
				get_diff(tree1, tree2, iroot1, iroot2)
			elif (iroot1 in tree1):
				# Retrieve ancestors
				t1 = copy.copy(iroot1)
				tmp_list = []
				while(t1 != tree1[t1].parent):
					tmp_list.append(t1.name)
					t1 = tree1[t1].parent
				# Store node with ancestors
				diff_list["Addition in AST1"].append(tmp_list)
			else:
				# Retrieve ancestors
				t1 = copy.copy(iroot2)
				tmp_list = []
				while(t1 != tree2[t1].parent):
					tmp_list.append(t1.name)
					t1 = tree2[t1].parent
				# Store node with ancestors
				diff_list["Addition in AST2"].append(tmp_list)
	else:
		print(tree1_root_children_names)
		print(tree2_root_children_names)
		print(len(tree1_root_children_names))
		print(len(tree2_root_children_names))
		tmp_list_1 = []
		tmp_list_2 = []
		t1 = copy.copy(rootNode1)
		while(t1 != tree1[t1].parent):
			tmp_list_1.append(tree1[t1].name)
			t1 = tree1[t1].parent
		tmp_list_1.append(tree1[t1].name)
		t1 = copy.copy(rootNode2)
		while(t1 != tree2[t1].parent):
			tmp_list_2.append(tree2[t1].name)
			t1 = tree2[t1].parent
		tmp_list_2.append(tree2[t1].name)
		diff_list["Modification"].append([tmp_list_1, tmp_list_2])

def get_diff_files(filename1, filename2):
	global diff_list
	diff_list = dict()
	diff_list["Addition in AST1"] = []
	diff_list["Addition in AST2"] = []
	diff_list["Modification"] = []
	ast1 = get_AST(filename1)
	ast2 = get_AST(filename2)
	get_diff(ast1, ast2, 0, 0)
	if (diff_list["Addition in AST1"] == []) and (diff_list["Addition in AST2"] == []) and (diff_list["Modification"] == []):
		return None
	return diff_list


if __name__ == "__main__":
	result = get_diff_files(sys.argv[1], sys.argv[2])
	if result is not None:
		print(result)
	else:
		print("There is no difference.")
