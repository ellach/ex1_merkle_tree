import hashlib
import queue
import math
import sys


class Node:
    def __init__(self, data, side):
        self.left = None
        self.right = None
        self.data = data
        self.side = side


class MerkleTree:

    def __init__(self, leafs):
        self.root = None
        self.leafs = leafs
        self.n_nodes = 2 * len(leafs) - 1  # All nods in the tree
        self.depth = int(math.log2(self.n_nodes)) + 1
        self.tree_layers = {}
        self.nodes = queue.Queue()
        # self.generate_tree_layers(leafs)

    def generate_tree_layers(self, nodes):
        """
        function compute value for each node
        :param nodes:
        :return:
        """
        self.tree_layers[0] = [node for node in nodes]
        self.__generate_tree_layers(nodes, depth=1)

    def __generate_tree_layers(self, nodes, depth=1):
        """
        :param nodes:
        :param depth:
        :return:
        """
        try:
            if len(nodes) == 1:
                return
            self.tree_layers[depth] = []
            for i in range(0, len(nodes), 2):
                if len(nodes) % 2 is 0:
                    self.tree_layers[depth].append(self.do_hash(nodes[i:i + 2][0], nodes[i:i + 2][1]))
                else:
                    if (i + 2) < len(nodes):
                        self.tree_layers[depth].append(self.do_hash(nodes[i:i + 2][0], nodes[i:i + 2][1]))
                    else:
                        self.tree_layers[depth].append(nodes[-1])
            self.__generate_tree_layers(self.tree_layers[depth], depth + 1)
        except Exception as error:
            print("Error:   ", error)
        # self.add_key()

    def add_key(self):
        """
        function add key to each node in order build binary tree
        :return:
        """
        try:
            holder = {}
            for i in reversed(range(len(self.tree_layers))):
                holder[i] = []
                for j, data in enumerate(self.tree_layers[i]):
                    n = self.n_nodes
                    if j % 2 is 0:
                        n = 2 * j + 1.5 * i
                        holder[i].append((data, n))
                    else:
                        n = 2 * j + 3 * i
                        holder[i].append((data, n))
            self.tree_layers = holder
            self.generate_tree()
        except Exception as error:
            print("Error:   ", error)

    def generate_tree(self):
        """
        function generate binary tree
        :return:
        """
        try:
            for i in reversed(range(len(self.tree_layers))):
                for j, data in enumerate(self.tree_layers[i]):
                    if j % 2 is 0:
                        side = 'l'
                    else:
                        side = 'r'
                    self.root = self.__generate_tree(self.root, data, side)
        except Exception as error:
            print("Error:   ", error)

    def __generate_tree(self, node, data, side):
        """
        :param node:
        :param data:
        :param side:
        :return:
        """
        try:
            if node is None:
                node = Node(data, None)
            elif data[1] <= node.data[1]:
                if node.left:
                    node.left = self.__generate_tree(node.left, data, side)
                else:
                    node.left = Node(data, 'l')
            else:
                if node.right:
                    node.right = self.__generate_tree(node.right, data, side)
                else:
                    node.right = Node(data, 'r')
            return node
        except Exception as error:
            print("Error:   ", error)

    def postorder(self):
        self.__postorder(self.root)

    def __postorder(self, node):
        """
        :param node:
        :return:
        """
        try:
            if self:
                if node.left:
                    self.__postorder(node.left)
                if node.right:
                    self.__postorder(node.right)
                self.nodes.put(node)
        except Exception as error:
            print("Error:   ", error)

    def proof_of_inclusion(self, node_index):
        """
        :param node_index:
        :param nosde_index:
        :return:
        """
        try:
            ans = []
            list_of_nodes = list(self.nodes.queue)
            if list_of_nodes[node_index].side is 'l':  # Left side
                ans.append(list_of_nodes[node_index + 1].side)
                ans.append(list_of_nodes[node_index + 1].data[0])
            elif list_of_nodes[node_index].side is 'r':  # Right side
                ans.append(list_of_nodes[node_index - 1].side)
                ans.append(list_of_nodes[node_index - 1].data[0])
            for i in range(2, self.n_nodes - 3, 3):
                ans.append(list_of_nodes[i + 3].side)
                ans.append(list_of_nodes[i + 3].data[0])
            return ans
        except Exception as error:
            print("Error:   ", error)

    def check_proof_of_inclusion(self, input_data):
        """
        :param input_data: string contain node data (char), root, proof of inclusion
        :return:
        """
        try:
            self.nodes.queue.clear()
            self.postorder()
            poi = input_data[2:]
            node = self.find_node(input_data[0])
            data = self.proof_of_inclusion(self.nodes.queue.index(node))
            for i in range(len(data)):
                if poi[i] != data[i]:
                    return False
            return True
        except Exception as error:
            print("Error:   ", error)

    def find_node(self, input_data):
        return self.__find_node(self.root, input_data)

    def __find_node(self, node, input_data):
        """
        :param node:
        :param input_data:
        :return:
        """
        try:
            if node is None:
                return None
            if node.data[0] is input_data:
                return node
            tmp = self.__find_node(node.left, input_data)
            if tmp is None:
                tmp = self.__find_node(node.right, input_data)
            return tmp
        except Exception as error:
            print("Error:   ", error)

    def find_nonce(self, user_input):
        """
        :param user_input:
        :return:
        """
        return self.__find_nonce(user_input, nonce=0)

    def __find_nonce(self, user_input, nonce=0):
        """
        :param user_input:
        :param nonce:
        :return: nonce:
        """
        try:
            non = str(nonce)
            hashed_nonce = self.do_hash(non, self.root.data[0])
            if hashed_nonce[:user_input] == '0' * user_input:
                return nonce, hashed_nonce
            else:
                return self.__find_nonce(user_input, nonce + 1)
        except RuntimeError as error:
            print('I recursed {} times!'.format(nonce))

    @staticmethod
    def do_hash(a, b):
        """
        :param a: string
        :param b: string
        :return:
        """
        try:
            if a is None or b is None:
                return
            else:
                return hashlib.sha256(str(a + b).encode('utf-8')).hexdigest()
        except Exception as error:
            print("Error:   ", error)


input_string = list(sys.stdin.readline().strip())
input_string = [a for a in input_string if a.isalpha()]
tree = MerkleTree(input_string)
tree.generate_tree_layers(input_string)
tree.add_key()
print(tree.root.data[0])

tree.postorder()
index = int(list(sys.stdin.readline().strip())[-1])
poi = tree.proof_of_inclusion(index)
print(' '.join([str(item) for item in poi]))

input_char = sys.stdin.readline().strip()
ans = tree.check_proof_of_inclusion(input_char[2:].strip().split(' '))
print(ans)

number = int(list(sys.stdin.readline().strip())[-1])
nonce, hashed = tree.find_nonce(number)
print(' '.join([str(nonce), str(hashed)]))
exit_ = int(sys.stdin.readline())
if exit_ is 5:
    sys.exit(0)
