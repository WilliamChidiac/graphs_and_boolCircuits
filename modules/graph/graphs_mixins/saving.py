import os
import sys
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
from typing import List, Dict

class open_digraph_saving_mx:
    #saving functions
    
    def save_as_dot_file(self, path : str, verbose : bool=False) -> None:
        """cree un fichier .dot lequel on stock le graph

        Args:
            path (str): le chemin du fichier .dot dans lequel sera stocker le graph
            verbose (bool, optional): si mis a vrai on affiche le label et l'id, sinon que l'id. Defaults to False.
        """
        file = open(path, "w")
        file.write("digraph G{\n")
        nodes_id = self.get_id_nodes_map()
        set_labels = lambda n, i : "i" if i in self.get_inputs_ids() \
                                    else "o" if i in self.get_outputs_ids() \
                                    else "  " if n.get_label() == ''\
                                    else n.get_label()                                                                              
        if verbose:
            set_labels = lambda n, i : n.get_label() + "  " + str(i)
        # exemple : si noeud = node(1, "label", ...)
        # si verbose = true :: set_labels(noeud, id_noeud) = "label v1" 
        # si vebose = false :: set_label(noeud, id_noeud) = "label"
        for i, n in nodes_id.items(): # on ecrit d'abord pour tous noeud(ID, "exemple", {},{}) les lignes  vID [label="exemple"]
            new_label = set_labels(n, i)
            file.write(f"\t{i} [label=\"{new_label}\"];\n")
        for i, n in nodes_id.items(): 
            for child, mul in n.get_children_ids().items(): # on ecrit ensuite pour tous noeud(ID, "exemple", parents, enfants = {ID2 : X, ...}) les lignes vID -> vID2
                for _ in range(mul): # on ecrit la ligne X fois, le nombre d'arrete de ID vers ID2
                    file.write(f"\t{i} -> {child};\n")
        file.write("}")
        file.close()
    
    @classmethod
    def from_dot_file(cls, path:str) -> 'open_digraph':
        """creer un graph stocke dans un .dot file

        Args:
            path (str): le chemin du fichier .dot dans lequel se trouve le graph

        Returns:
            open_digraph : le graph decrit dans le fichier  .dot
        """
        file = open(path, "r")
        string_labels = {}
        string_child = {}
        string_id = {}
        nodes = []
        f = file.read().strip("digraph G {\n\t").split(";\n\t")
        id = 1
        for i in range(len(f)):
            if f[i].find("label") != -1: # si la ligne lu est du type vID [label="exemple"]
                sl = f[i].split(" [label=\"") # "vID [label="exemple"]" -> ["vID", "exemple\"]"]
                string_labels[sl[0]] = sl[1][:-2] # {"vID" : "exemple"}
            else: # si la ligne lu est du type vID -> vID2
                sub = f[i].split(";\n}")
                sub = sub[0]
                sc = sub.split(" -> ") # sc = ["vID", "vID2"]
                if sc[0] in string_child:
                    string_child[sc[0]].append(sc[1])
                else:
                    string_child[sc[0]] = [sc[1]]
                if sc[0] not in string_id:
                    string_id[sc[0]] = id
                    nodes.append(node(id, string_labels[sc[0]] if sc[0] in string_labels else "", {},{}))
                    id = id + 1
                if sc[1] not in string_id:
                    string_id[sc[1]] = id
                    nodes.append(node(id, string_labels[sc[1]] if sc[1] in string_labels else "", {},{}))
                    id = id + 1
        graph = cls([], [], nodes)
        for parent, children in string_child.items():
            parent_id = string_id[parent]
            for child in children:
                child_id = string_id[child]
                graph.add_edge(parent_id, child_id)     
        file.close()
        return graph
    
    def display(self, verbose :bool=False, path : str="output_file.pdf") -> None:
        """cree un fichier output_file.pdf dans lequel on pourra visualiser le graph

        Args:
            verbose (bool, optional): si verbose est mis a vrai on affiche l'id et le label de chaque noeud,
                                    sinon que le label. Defaults to False.
        """
        self.save_as_dot_file("input_file.dot",verbose) # creer le fichier.dot
        os.system(f"dot -Tpdf input_file.dot -o {path}") # creer le fichier.pdf
        os.system("rm input_file.dot") # supprime le fichier.dot