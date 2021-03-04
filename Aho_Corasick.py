import queue

class Node:
    def __init__(self):
        self.char = None
        self.parent = None
        self.child = {}
        self.fail_arc = None
        self.output_arc = None
        self.isEnd = False


def preprocess(patterns):
    root = Node()
    # build the prefix tree
    for pattern in patterns:
        currentnode = root
        for i in range(len(pattern)):
            char = pattern[i]
            if char not in currentnode.child:
                node = Node()
                node.char = char
                node.parent = currentnode
                currentnode.child[char] = node
                currentnode = node
            else:
                currentnode = currentnode.child[char]
            if i == len(pattern) - 1:
                currentnode.isEnd = True

    # build the fail arcs
    q = queue.Queue()
    q.put(root)
    while not q.empty():
        node = q.get()
        for k in node.child:
            q.put(node.child[k])
        build_fail_arc(node)
    q.put(root)
    while not q.empty():
        node = q.get()
        for k in node.child:
            q.put(node.child[k])
        build_output_arc(node)
    return root


def build_fail_arc(node):
    if node.parent is None:  # root
        return
    cur = node.parent
    if cur.parent is None:  # depth 1
        node.fail_arc = cur
        return
    found = False
    while not found:
        cur_fail_arc = cur.fail_arc
        if node.char in cur_fail_arc.child:
            node.fail_arc = cur_fail_arc.child[node.char]
            found = True
        else:
            cur = cur_fail_arc
    return


def output(node):
    cur = node
    text = ""
    while cur.parent is not None:
        text = cur.char + text
        cur = cur.parent
    return text


def build_output_arc(node):
    if node.parent is None:
        return
    if node.parent.parent is None:
        return
    cur = node
    while True:
        cur = cur.fail_arc
        if cur.parent is None:  # cur is depth 1
            return
        if cur.isEnd:
            node.output_arc = cur
            return


def aho_corasick(seq, patterns):
    node = preprocess(patterns)
    i = 0
    seq_length = len(seq)
    pos = []
    while i < seq_length:
        c = seq[i]
        while seq[i] not in node.child:
            node = node.fail_arc
        node = node.child[seq[i]]
        if node.isEnd:
            pos.append(i)
            print(output(node))
        cur = node
        while cur.output_arc is not None:
            o = output(node)
            pos.append(i)
            print(o)
            cur = cur.output_arc

        i = i + 1
    return pos
