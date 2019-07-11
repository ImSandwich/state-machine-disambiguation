from copy import copy, deepcopy

MAX_EDGES = 2 

class Tree:
    def __init__(self, *args):
        
        if len(args) == 1:
            pass
        else:
            root = args[0]
            s_ids = args[1]
            self.root = Node(root) 
            self.subsequence_ids = copy(s_ids)
            self.subsequence_last_node = {} 
            for key in self.subsequence_ids:
                self.subsequence_last_node[key] = self.root 
            self.all_nodes = [self.root]

    def __str__(self):
        return str(self.root)

class Node:
    next_id = 0
    def __init__(self, val):
        self.val = val 
        self.id = Node.next_id 
        Node.next_id += 1
        self.conn = {}

    def __str__(self):
        out = str("[" + str(self.val) + "]") 
        for n in self.conn:
            out += "\n"
            out += str(n) + "->\n"
            lines = str(self.conn[n]).split("\n")
            for l in lines:
                out += " " + l + "\n"
        return out


def merge_subsequences(S):
    assert(all([S[0][1] == S[i][1]] for i in range(len(S))))
    combined_tree = Tree(S[0][1])
    longest_path = max([len(s) for s in S])
    parent_node = {}
    for Si in range(len(S)):
        parent_node[Si] = combined_tree.root

    for index in range(1, longest_path):
        for Si in range(len(S)):
            if len(S[Si]) <= index:
                continue 
            edge, node_val = S[Si][index]
            if edge not in parent_node[Si].conn:
                new_node = Node(node_val) 
                combined_tree.all_nodes += [new_node]
                parent_node[Si].conn[edge] = new_node
            else:
                if parent_node[Si].conn[edge].val != node_val:
                    return None 
            parent_node[Si] = parent_node[Si].conn[edge]

    return combined_tree

def create_forest(subseq):
    assert(all([S[0][0][1].val == S[i][0][1].val] for i in range(len(S))))
    root_seed = Tree(S[0][0][1].val, [s[0][1].id for s in S])
    print(root_seed.subsequence_ids)
    forest = [root_seed]
    grow_tree(forest, root_seed, subseq, 1, 0, [])
    return forest 
    
# new set of parent nodes for every new tree
def grow_tree(forest, seed, subseq, depth, subseq_index, skip):
 
    longest_path = max([len(s) for s in subseq])
    if depth >= longest_path:
        return 
    
    for Si in range(subseq_index, len(subseq)):
        subseq_id = subseq[Si][0][1].id
        # Only analyze the subseqs we care about
        if subseq_id not in seed.subsequence_ids:
            continue
        if len(subseq[Si]) <= depth:
            continue 
        if subseq_id in skip:
            continue
        edge = subseq[Si][depth][0]
        node_val = subseq[Si][depth][1].val 
        # Check if already hit end end
        current_node_id = subseq[Si][depth][1].id
        if current_node_id in seed.subsequence_ids and depth > 1:
            skip += [subseq_id]
        if edge not in seed.subsequence_last_node[subseq_id].conn:
            new_node = Node(node_val)
            seed.all_nodes += [new_node]
            seed.subsequence_last_node[subseq_id].conn[edge] = new_node
            seed.subsequence_last_node[subseq_id] = new_node
        else:
            if seed.subsequence_last_node[subseq_id].conn[edge].val == node_val:
                seed.subsequence_last_node[subseq_id] = seed.subsequence_last_node[subseq_id].conn[edge]
            else:
                conflict_subseq = -1
                for CSi in range(subseq_index, Si):
                    c_subseq_id = subseq[CSi][0][0]
                    if c_subseq_id not in seed.subsequence_ids:
                        continue
                    if seed.subsequence_last_node[c_subseq_id] == seed.subsequence_last_node[subseq_id].conn[edge]:
                        conflict_subseq = c_subseq_id
                        break 
                
                alternative_tree = deepcopy(seed)
               
                # Create an alternative version where the first option is removed, restart!
                alternative_tree.subsequence_ids.remove(conflict_subseq)
                alternative_tree.all_nodes.remove(alternative_tree.subsequence_last_node[subseq_id].conn[edge])
                new_node = Node(node_val)
                alternative_tree.all_nodes += [new_node]
                alternative_tree.subsequence_last_node[subseq_id].conn[edge] = new_node
                alternative_tree.subsequence_last_node[subseq_id] = new_node
                forest += [alternative_tree]
                grow_tree(forest, alternative_tree, subseq, depth, subseq_index+1, skip)
                # In this version, remove the second option
                seed.subsequence_ids.remove(subseq_id)
    grow_tree(forest, seed, subseq, depth+1, 0, skip)

                
A = Node(1)
B = Node(2)
C = Node(2)
D = Node(2)
E = Node(1)
F = Node(1)
G = Node(2)
A.conn[1] = B 
B.conn[1] = C
C.conn[1] = D
D.conn[2] = E
E.conn[2] = F 
F.conn[2] = G 

S1 = [(0, A), (1, B), (1, C), (1, D), (2, E), (2, F), (2, G)]
S2 = [(1, E), (1, F), (2, G)]
S = [S1, S2]
forest = create_forest(S)
print(forest[1])
