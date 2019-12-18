# coding=utf8
# !/usr/bin/env python
import json

class TreeNode():
    """
    定义树结点为多个子结点，以及多个父节点
    """
    __groups = []
    __count = 0  # 计数， 实例个数，表示共处理了多少个结点

    def __init__(self, name):
        self.ancestor_nodes = []
        self.descendant_nodes = []
        self.name = name
        self.__groups.append(name)
        TreeNode.__count += 1
        self.visited = False

    def __repr__(self):
        return self.name
        # print(self.name)

    @staticmethod
    def get_count():
        return TreeNode.__count

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
        # if all ancestors have been visited return true


class Forest():
    """
    The forest you get might have multi root nodes

    You need to import a json file in which all the dependences are listed in the way as below sample:
        {
        "a":["b"], # node "a" is supposed to be a child node of "b",
        "b":["c", "d"], # node "b" should be a child node of "c", and "d" as well,
        "c":["e"], # "c" should be a child node of "e"
        }

    The forest you will get will be like below：
                 e
                /
          d   c
           \ /
            b
           /
          a

    About How to use this class:
        dependenceforest = Forest()
        dependenceforest.build_from(path_json_file)
        # by calling preorder_traverse(), all the preorder paths in the forest will be listed pointed by the variable "predorder_paths"
        dependenceforest.preorder_traverse()
        # path_to(a_given_node_name) will return the full path related to the given node, preorder
        dependenceforest.path_to('cashconversioncycle')

    """

    def __init__(self):
        self.root_nodes = []
        self.root_factor_names = []
        self.preorder_paths = []
        self.factor_names = []

    def count(self):
        # 返回总共创建的结点实例的个数
        return TreeNode.get_count()

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
        if child in self.root_nodes:
            self.root_nodes.remove(child)
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

    def preorder_traverse(self):
        """
        优先计算所有依赖
        :return: all exist path
        """
        traverse_paths = []
        for node in self.root_nodes:
            # print(node)
            path = [[]]  # 路径有多条
            path = PreorderIterator(node).traverse(path, node)
            traverse_paths.extend(path)
        self.preorder_paths = traverse_paths
        pass

    def path(self):
        """

        :param treenode:
        :return: a list contain all the paths to the given treenode
        """
        pass

    def path_to(self, name):
        """
        To find out the Node object with the given name
        :param name:
        :return:
        """
        for n in self.root_nodes:
            treenode = self.search_node(n, name)
            if treenode is not None:
                break

        dependencepath = PreorderIterator.preorder_traverse(treenode, [])
        return dependencepath
        # return reduce(lambda x,y:set(x).add(y), candidates)
    # def path_to(self, name):
    #     candidates = []
    #     for p in self.preorder_paths:
    #         if name in p:
    #             idx = p.index(name)
    #             candidates.append(p[:idx])
    #     candidates = sorted(candidates, key=lambda x: len(x), reverse=True)
    #     dependences = []
    #     for ds in candidates:
    #         for val in ds:
    #             if val not in dependences:
    #                 dependences.add(val)
    #     return dependences
    #     # return reduce(lambda x,y:set(x).add(y), candidates)


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
    def traverse(path, treenode):
        # if treenode.name == name:
        #     return path
        from copy import deepcopy
        # treenode.set_visited()
        if len(treenode.descendant_nodes) == 0:
            newpath = deepcopy(path)
            for p in newpath:
                p.append(treenode.name)
            return newpath
        else:
            # len(treenode.descendant_nodes)>0:
            newpath = []
            # for p in path:
            # p.appenend(treenode.name)
            for node in treenode.descendant_nodes:
                for p in PreorderIterator.traverse(path, node):
                    np = [treenode.name]
                    np.extend(p)
                    newpath.append(np)
            return newpath
            # p.extend(PreorderIterator.traverse(path, node))
            # elif not treenode.ancestor_visited_flag():
            #     for node in treenode.ancestor_nodes:
            #         if not node.visited:
            #             path.append(PreorderIterator.traverse(path, node))

    def next(self):

        if len(self.stack) > 0:  # and self.node is not None:
            self.node = self.stack.pop()

        # for node in self.node.descendant_nodes:
        for node in self.node.ancestor_nodes:
            self.stack.append(node)

        if self.node.left is not None:
            self.stack.append(self.node.left)

        return self.node.value

    @staticmethod
    def preorder_traverse(node, path):
        """
        To find out al the parent node of given node
        :param node:
        :param path:
        :return:
        """
        # if node.ancestor_visited_flag() is True:
        #     node.set_visited()
        #     path.append(node.name)
        #     return path
        if node.ancestor_visited_flag() is False:
            for n in node.ancestor_nodes:
                if n.visited is False:
                    for i in PreorderIterator.preorder_traverse(n, []):
                        if i not in path:
                            path.append(i)
        path.append(node.name)
        node.set_visited()
        return path


if __name__ == "__main__":
    import os

    dir = os.path.dirname(os.path.realpath(__file__))
    dependenceforest = Forest()
    dependenceforest.build_from(os.path.join(dir, 'factors_dependence.json'))
    dependenceforest.preorder_traverse()
    print(dependenceforest.path_to('cashconversioncycle'))
    # "cashconversioncycle")
    print(dependenceforest.count())
    pass
# root = Node(10)

# root.PrintTree()
