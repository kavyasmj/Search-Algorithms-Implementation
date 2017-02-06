# ----------------------------------------------- Data Declarations ---------------------------------------------------
# global variables
graph = []  # to store the vertices
cost = 1    # edge-cost.. defaulted to 1 for dfs and bfs
queue = []  # data structure to traverse the graph
explored_queue = []  # for loop detection
o_num = 0  # order number, to maintain order of input for tie breaking between sibling nodes
e_num = 0  # enqueue number, to maintain order of enqueuing nodes to queue for tie breaking between non-sibling nodes
# ----------------------------------------------- Class Declarations ---------------------------------------------------


class Vertex:  # Vertex class and its methods
    # name, edge list
    def __init__(self, name):
        self._name = name
        self._edges = []
        self._hueristic = 0  # only for A*

    def get_name(self):
        return self._name

    def get_edges(self):
        return self._edges

    def set_edges(self, value):
        self._edges.append(value)

    def set_heuristic(self, value):
        self._hueristic = value

    def get_heuristic(self):
        return self._hueristic


class Edge:  # edge class and its methods
    # neighbor_name, weight
    def __init__(self, neighbor_name, weight, order_no):
        self._neighbor_name = neighbor_name
        self._order_no = order_no
        if srch_algo != "BFS":
            self._weight = weight
        else:
            self._weight = 1

    def get_neighbor_name(self):
        return self._neighbor_name

    def get_weight(self):
        return self._weight

    def get_order_no(self):
        return self._order_no


class Node:  # node class and its methods
    def __init__(self,  enq_no, state, parent, path_cost, heuristic):
        self._enq_no = enq_no
        self._state = state
        self._parent = parent
        self._path_cost = path_cost
        self._heuristic = heuristic

    def get_state(self):
        return self._state

    def get_parent(self):
        return self._parent

    def get_path_cost(self):
        return self._path_cost

    def get_heuristic(self):
        return self._heuristic

    def get_enq_no(self):
        return self._enq_no


# ---------------------------------------------- Method Declarations ---------------------------------------------------
# ---------------------------------------------Create vertex------------------------------------------------------------
# create new vertex and return it
def create_vertex(vertex_name):
    new_vertex = Vertex(vertex_name)
    graph.append(new_vertex)
    return new_vertex


# ---------------------------------------------Return vertex info-------------------------------------------------------
# returns existing Vertex or new Vertex if it doesn't exist
def get_vertex(vertex_name):

    exists = 0
    vertex = None
    # check if Vertex exists
    for n in graph:
        n_name = n.get_name()
        if n_name == vertex_name:
            vertex = n
            exists = 1
            break

    if exists == 0:
        vertex = create_vertex(vertex_name)

    return vertex


# ---------------------------------------------create edge for a Vertex-------------------------------------------------
def create_edge(vertex_name, neighbor_name, weight):
    src_vertex = get_vertex(vertex_name)
    get_vertex(neighbor_name)
    temp_edgelist = src_vertex.get_edges()
    # check if edge already exists
    for e in temp_edgelist:
        e_name = e.get_neighbor_name()
        if e_name == neighbor_name:
            raise ValueError('Something went wrong, input file has duplicates')

    # if it doesn't exist, create it
    global o_num
    o_num += 1
    new_edge = Edge(neighbor_name, weight, o_num)
    src_vertex.set_edges(new_edge)
    # ---graph is directed----

    return


# ---------------------------------------------Create and push node onto queue------------------------------------------
# pushes nodes to queue
def push_to_queue(que, state, parent, path_cost, heuristic):

    rem_eq_node = None
    rem_q_node = None

    for eq in explored_queue:
        if eq.get_state() == state:
            if eq.get_path_cost() <= path_cost:
                return  # don't add this node
            else:  # this cond wont occur for DFS and BFS, cost of step costs, and if path is always positive
                rem_eq_node = eq   # do not return, go on to add this node
                break

    if rem_eq_node is not None:
        explored_queue.remove(rem_eq_node)  # remove the higher cost/same state node from explored q

    for q in que:
        if q.get_state() == state:
            if q.get_path_cost() <= path_cost:
                return  # don't add this node
            else:  # this cond wont occur for DFS and BFS, cost of step costs, and if path is always positive
                rem_q_node = q  # do not return, go on to add this node
                break

    if rem_q_node is not None:
        que.remove(rem_q_node)  # remove the higher cost/same state node from q

    global e_num
    e_num += 1
    if srch_algo == "A*":
        heuristic = path_cost + heuristic

    node = Node(e_num, state, parent, path_cost, heuristic)

    if srch_algo == "DFS":
        que.insert(0, node)
    else:    # BFS, USC, A*
        que.append(node)
    return


# ---------------------------------------------Return queue info--------------------------------------------------------
# returns empty if queue is empty, else returns a node
def pop_from_queue(que):
    node = None

    if que:
        node = que.pop(0)
    return node


# ---------------------------------------------Get the child nodes aka edges info --------------------------------------
def get_children(vertex_name):
    vertex = None
    for n in graph:
        n_name = n.get_name()
        if n_name == vertex_name:
            vertex = n
            break

    if vertex is None:
        # vertex doesn't have an edge
        edge_list = []
    else:
        edge_list = vertex.get_edges()

        if srch_algo != "DFS":
            edge_list.sort(key=lambda x: x.get_order_no())
        elif srch_algo == "DFS":
            edge_list.sort(key=lambda x: x.get_order_no(), reverse=True)

    return edge_list


# ---------------------------------------------Output logic-------------------------------------------------------------
def print_to_output(node):

    # create the output file
    gv_fh_output = open("output.txt", "w")

    op_list = []

    while node is not None:
        op_line = node.get_state() + " " + str(node.get_path_cost()) + "\n"
        op_list.append(op_line)

        node = node.get_parent()

    op_list.reverse()
    for item in op_list:
        gv_fh_output.write(item)

    gv_fh_output.close()


# ---------------------------------------------generic graph search func------------------------------------------------
def gs():

    # find the starting vertex
    vertex = None
    for n in graph:
        if n.get_name() == start_state:
            vertex = n
            break

    # push first vertex to q by creating a node
    push_to_queue(queue, vertex.get_name(), None, 0, vertex.get_heuristic())  # no parent and path cost is 0

    # loop until failure or success
    while 1:
        # pop from q
        if srch_algo == "UCS":
            queue.sort(key=lambda x: (x.get_path_cost(), x.get_enq_no()))

        if srch_algo == "A*":
            queue.sort(key=lambda x: (x.get_heuristic(), x.get_enq_no()))

        temp_node = pop_from_queue(queue)

        # if queue is empty, break from loop and return failure
        if temp_node is None:
            raise ValueError('Something went wrong! No path was found')

        # check if its the destination
        # if yes return success and path, path cost
        if temp_node.get_state() == goal_state:
            print_to_output(temp_node)
            return

        # if not and add children in alphabetical order to q
        edge_list = get_children(temp_node.get_state())
        for edge in edge_list:
            edge_name = edge.get_neighbor_name()
            # don't go back to same node A->A
            if edge_name == temp_node.get_state():
                continue

            # don't go back to parent A->B B->A
            if temp_node.get_parent() is not None:
                if edge_name == temp_node.get_parent().get_state():
                    continue

            edge_weight = edge.get_weight()

            child_vertex = None
            for n in graph:
                if n.get_name() == edge_name:
                    child_vertex = n
                    break

            # push to q
            push_to_queue(queue, edge_name, temp_node, (temp_node.get_path_cost() + edge_weight),
                          child_vertex.get_heuristic())

        explored_queue.append(temp_node)


# ---------------------------------------------Execution Starts Here----------------------------------------------------


# ----------------------------------------------------Fetch input-------------------------------------------------------
# Fetch input from the file
gv_fh_input = open("input.txt", "r")
# read the file and set the global vars
srch_algo = gv_fh_input.readline().rstrip()
start_state = gv_fh_input.readline().rstrip()
goal_state = gv_fh_input.readline().rstrip()
num_ltl = int(gv_fh_input.readline())
i = num_ltl


# ---------------------------------------------Graph created from input-------------------------------------------------
while i > 0:
    temp_list = gv_fh_input.readline().rstrip().split()
    if srch_algo not in ["BFS", "DFS"]:
        cost = int(temp_list[2])
    create_edge(temp_list[0], temp_list[1], cost)
    i -= 1

n1 = 0
try:
    num_stl = int(gv_fh_input.readline())
    n1 = num_stl
except ValueError:
    print ("Sunday traffic info is not given")

# heuristics for A*
if srch_algo == "A*":
    while n1 > 0:
        sun_list = gv_fh_input.readline().rstrip().split()
        temp_vertex = get_vertex(sun_list[0])
        temp_vertex.set_heuristic(int(sun_list[1]))
        n1 -= 1

# ---------------------------------------------Call generic graph search function---------------------------------------
gs()
