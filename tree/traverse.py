#!/usr/bin/env python
import json


class TreeNode():
    """
    定义树结点为多个子结点，以及多个父节点
    """
    __groups = []

    def __init__(self, name):
        self.ancestor_nodes = []
        self.descendant_nodes = []
        self.name = name
        self.__groups.append(name)
        self.visited = False

    def __repr__(self):
        return self.name
        # print(self.name)

    def set_visited(self):
        self.visited = True

    def visited_flag(self):
        return self.visited

    def add_ancestor(self, treenode):
        self.ancestor_nodes.append(treenode)

    def add_descendant(self, treenode):
        self.descendant_nodes.append(treenode)

    def ancestor_visited_flag(self):
        for node in self.ancestor_nodes:
            if not node.visited:
                return False
        return True
        pass
        # if all ancestors have been visited return true


class Forest():
    """存在多个root"""

    def __init__(self):
        self.root_nodes = []
        self.root_factor_names = []
        self.preorder_path = []

        self.factor_names = []

    def new_node(self, name):
        if name not in self.factor_names:
            # 需要保证每个factor只有一个实例
            treenode = TreeNode(name)
            self.factor_names.append(treenode.name)
        else:
            # find the exist node
            for n in self.root_nodes:
                treenode = self.search_node(n, name)
                if self.search_node(n, name) is not None:
                    break
        return treenode

    def build_from(self, filepath):

        with open(filepath, 'r') as f:
            data = f.read()

        data = json.loads(data)
        for key, value in data.items():
            tn = self.new_node(key)
            for p in value:
                tnp = self.new_node(p)
                self.build(tnp, tn)

    def build(self, parent, child):
        if parent is None:
            pass
        parent.add_descendant(child)
        child.add_ancestor(parent)
        # if child in self.root_nodes:
        #     self.root_nodes.remove(child)
        self.add_root(parent)

    @staticmethod
    def search_node(node, name):
        if node.name == name:
            return node
        else:
            for n in node.descendant_nodes:
                target = Forest.search_node(n, name)
                if target is not None:
                    return target
        # return None

    def add_root(self, treenode):
        if treenode.name in self.root_factor_names:
            return
        self.root_nodes.append(treenode)
        self.root_factor_names.append(treenode.name)

    def preorder_traverse(self, name):
        """
        以优先计算所有依赖
        :return: all exist path
        """
        traverse_paths = []
        for node in self.root_nodes:
            print(node)
            path = [[]]  # 路径有金条
            PreorderIterator(node).traverse(path, node, name)
            traverse_paths.extend(path)

    def path(self, treenode):
        """

        :param treenode:
        :return: a list contain all the paths to the given treenode
        """


class PreorderIterator(object):
    """
    preorder,
    1. stack current node,
    2. checkout ancestor
    """

    def __init__(self, node):

        self.node = node
        self.stack = []
        self.stack.append(self.node)
        self.path = []

    @staticmethod
    def traverse(path, treenode, name):
        if treenode.name == name:
            return path
        if treenode.ancestor_visited_flag():
            for p in path:
                p.append(treenode.name)
            treenode.set_visited()
            for node in treenode.descendant_nodes:
                PreorderIterator.traverse(path, node)
        else:
            for node in treenode.ancestor_nodes:
                PreorderIterator.traverse(path, node)

    def next(self):

        if len(self.stack) > 0:  # and self.node is not None:
            self.node = self.stack.pop()

        # for node in self.node.descendant_nodes:
        for node in self.node.ancestor_nodes:
            self.stack.append(node)

        if self.node.left is not None:
            self.stack.append(self.node.left)

        return self.node.value


if __name__ == "__main__":
    import os

    dir = os.path.dirname(os.path.realpath(__file__))
    dependenceforest = Forest()
    dependenceforest.build_from(os.path.join(dir, 'factors_dependence.json'))
    dependenceforest.preorder_traverse("cashconversioncycle")
# root = Node(10)

# root.PrintTree()
