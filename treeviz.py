from __future__ import print_function
import fileinput
import pygraphviz as pgv


def treeViz(tree):
    graph = pgv.AGraph(directed=True, rankdir="LR")

    def walk(node, parent=None, dist=None):
        if parent:
            graph.add_edge(
                parent,
                node["string"],
                label=dist
            )
        for key in node["children"]:
            walk(node["children"][key], parent=node["string"], dist=key)

    walk(tree._root)

    print(graph)


if __name__ == "__main__":
    from bktree import BKTree
    from hamdist import hamdist

    tree = BKTree(hamdist)

    for line in fileinput.input():
        tree.insert(line)

    treeViz(tree)
