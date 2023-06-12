from treelib import Tree,Node
from Parse.tokenize import flatten_tokens, give_chidren,find_token




class UDTree(Tree):

    def __init__(self, trankit_output: dict,start =0):
        super().__init__()
        self.text = trankit_output["text"]
        self.__create_from_tokens(flatten_tokens(trankit_output['tokens']), start=0)

    def __create_from_tokens(self, tokens: list, start=0) -> None:
        root = None
        for token in tokens:
            if token["head"] == start:
                self.root = Node(tag=token["text"], identifier=token['id'], data=token)
                root = token
                break

        def __add_tokens(parent):
            children = give_chidren(tokens, parent["id"])
            if children:
                for child in children:
                    node = Node(tag=child['text'], identifier=child['id'], data=child)
                    self.add_node(node, parent=parent)
                    __add_tokens(child)
        if root:
            __add_tokens(root)

    def subtree(self, nid, identifier=None):
        tre = self.subtree(nid)
        nodes = tre.all_nodes()
        tokens = map(lambda x: x.data, nodes)
        


        return UDTree()


