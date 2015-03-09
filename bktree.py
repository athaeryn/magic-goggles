class BKTree:
    def __init__(self, dist_func):
        self._root = None
        self._dist = dist_func

    def insert(self, string, meta={}):
        node = self._make_node(string, meta)
        if self._root is None:
            self._root = node
            return
        self._insert_at_node(self._root, node)

    def query(self, string, tolerance=2):
        return self._query_node(self._root, string, tolerance)

    def _query_node(self, node, string, tolerance):
        dist = self._dist(node["string"], string)
        matches = []
        if dist <= tolerance:
            matches.append(node["string"])
        for k in node["children"]:
            if k >= tolerance - 1 and k <= tolerance + 1:
                matches += self._query_node(
                    node["children"][k],
                    string,
                    tolerance
                )
        return matches

    def _insert_at_node(self, node, new_node):
        dist = self._dist(node["string"], new_node["string"])
        if dist not in node["children"]:
            node["children"][dist] = new_node
            return
        self._insert_at_node(node["children"][dist], new_node)

    def _make_node(self, string, meta):
        return {
            "string": string,
            "meta": meta,
            "children": {}
        }
