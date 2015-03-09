class BKTree:
    def __init__(self, dist_func):
        self._tree = None
        self._dist = dist_func
        pass

    def insert(self, string, meta={}):
        node = self._make_node(string, meta)
        if self._tree is None:
            self._tree = node
        else:
            self._insert_at_node(self._tree, node)

    def query(self, string):
        pass

    def _insert_at_node(self, node, new_node):
        dist = self._dist(node["string"], new_node["string"])
        if dist not in node["children"]:
            node["children"][dist] = new_node
        else:
            self._insert_at_node(node["children"][dist], new_node)

    def _make_node(self, string, meta):
        return {
            "string": string,
            "meta": meta,
            "children": {}
        }
