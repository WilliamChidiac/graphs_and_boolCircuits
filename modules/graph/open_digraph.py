from modules.graph.open_digraph_mixins import *


class open_digraph(open_digraph_saving_mx,
                   open_digraph_composition_decomposition_mx, 
                   open_digraph_distance_mx,
                   open_digraph_profondeur_mx,
                   open_digraph_matrice_traduction_mx
                   ): 
    def __init__(self, inputs : List[int], outputs : List[int], nodes : List[node]):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        nextId : int ; l'id du prochain noeud a ajouter
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict
        try:
            self.nextId = max(list(self.nodes.keys()))+1
        except:
            self.nextId = 0


    def __str__(self) -> str:
        inputs = "inputs : "
        for i in self.inputs:
            inputs += str(i) + ", "
        outputs = 'outputs : '
        for i in self.outputs:
            outputs += str(i) + ", "
        inputs += '\n'
        outputs += '\n'
        nodes = ''
        for j in self.nodes.values():
            nodes += str(j)
            nodes += "\n"
        return inputs + outputs + nodes      

    def __repr__(self) -> str:
        return str(self)  

    @classmethod
    def empty(cls) -> 'open_digraph':
        """
        rend un graphe vide
        """
        return open_digraph([], [], [])

    def copy(self) -> 'open_digraph':
        """
        rend une copy du graphe
        """
        g = open_digraph.empty()
        g.inputs = self.inputs.copy()
        g.outputs = self.outputs.copy()
        g.nodes = {id : nodes.copy() for id,nodes in self.nodes.items()}
        g.nextId = self.nextId
        return g
    
    #getters
    def get_inputs_ids(self) -> List[int]:
        """
        rend la list des inputs du graphe
        """
        return self.inputs
    def get_outputs_ids(self) -> List[int]:
        """
        rend la list des outputs du graphe
        """
        return self.outputs
    def get_id_nodes_map(self) -> Dict[int, node]:
        """
        rend un dictionnaire de la forme (id du noeud : noeud)
        """
        return self.nodes
    def get_nodes(self) -> List[node]:
        """
        rend la liste de tous les noeud du graphe
        """
        return list(self.nodes.values())
    def get_nodes_ids(self) -> List[int]:
        """
        rend la list de toute les ids de noeud du graphe
        """
        return list(self.nodes.keys())
    def get_node_by_id(self, id : int) -> node:
        """
        etant donnee un noeud, la fonction rend le son associe
        param :
        id - int l'id du noeud a cherche
        return node"""
        return self.nodes[id]
    def get_nodes_by_ids(self, ids : List[int]) -> List[node]:
        """
        etant donnee une liste de ids, la fonction rend la liste de noeud associe au ids.
        param:
        ids - int list
        return node list
        """
        return [self.nodes[i] for i in ids]
    
    def __getitem__(self, id:int) -> node:
        return self.get_node_by_id(id)
    
    def min_id(self) -> int:
        """cherche la plus petite id occupe par un noeud

        Returns:
            int: l'id trouve
        """
        return min(self.get_nodes_ids())
    
    def max_id(self) -> int:
        """cherche la plus grande id occupe par un noeud

        Returns:
            int: l'id trouve
        """
        return max(self.get_nodes_ids())
    
    def new_id(self) -> int:
        """
        rend une id encore inexsistante dans le graphe
        """
        id = self.nextId
        self.nextId += 1
        return id

    #setters
    def set_input_ids(self, inputs :List[int]) -> None:
        """
        associe au graphe ces inputs
        param :
        inputs - int list
        """
        self.inputs = inputs
    def set_outputs_ids(self, outputs : List[int]) -> None:
        """
        associe au graphe ces outputs
        param :
        outputs - int list
        """
        self.outputs = outputs

    def add_input_id(self, id : int) -> None:
        """
        rajoute un nouvel input a la list des inputs du graphe
        param :
        id - int l'id du nouvel input
        """
        self.inputs.append(id)
    def add_output_id(self, id : int) -> None:
        """
        rajoute un nouvel output a la list des ouputs du graphe
        param :
        id - int l'id du nouvel output
        """
        self.outputs.append(id)

    #method

    #add functions
    def new_id(self) -> int:
        """
        rend une id encore inexsistante dans le graphe
        """
        id = self.nextId
        self.nextId += 1
        return id
    def add_edge(self, src : int, tgt : int) -> None:
        """
        lie 2 noeuds entre eux
        param :
        src - int; l'id du noeud parent
        tgt - int; l'id du noeud enfant
        """
        n1 = self.get_node_by_id(src)
        n1.add_child_id(tgt)
        n2 = self.get_node_by_id(tgt)
        n2.add_parent_id(src)
        self.nodes[src] = n1
        self.nodes[tgt] = n2
    def add_edges(self, edges : List[Tuple[int, int]]) -> None:
        """
        prend en parametre une liste de pair d'ids (id_parent, id_enfant) et les lie ensemble
        param:
        edges - (int * int) list ; la list de pair d'id des noeud a lier
        """
        for src, tgt in edges:
            self.add_edge(src, tgt)
    def add_node(self, label : str="", parents : Dict[int, int]=None, children : Dict[int, int]=None) -> int:
        """
        rajoute un noeud au graphe en creer tous les liens demande
        param :
        label - str;
        parents/children - (int * int) dict;  les couples (id : multiplicite) des parents/enfants du noeud a rajoute
        return l'id de noeud ajoute
        """
        if (parents is None):
            parents = {}
        if (children is None):
            children = {}
        id = self.new_id()
        n = node(id, label, parents, children)
        self.nodes[id] = n
        for p in parents:
            self.nodes[p].children[id] = parents[p]
        for c in children:
            self.nodes[c].parents[id] = children[c]
        return id

    def add_input_node(self,id : int) -> None :
        """
        fonction qui rajoute un nouvel input au graphe relie a un noeud choisi
        param : 
        id - int , l'id du fils du nouvel inputs
        IMPORTANT : il est important de note que si le noeud donnee en parametre est un input le graph ne sera pas bien forme
        """
        inputs = self.get_inputs_ids()
        if (id in inputs) :
            print('sncdkj')
            raise ValueError("Erreur un noeux en input ne peut pas avoir de parent")
        new_id = self.add_node("", {}, {id : 1})
        self.add_input_id(new_id)

    def add_output_node(self,id : int ) -> None:
        """
        fonction qui rajoute un nouvel output au graphe relie a un noeud choisi
        param : 
        id - int , l'id du parent du nouvel output
        IMPORTANT : il est important de note que si le noeud donnee en parametre est un output le graph ne sera pas bien forme
        """
        outputs = self.get_outputs_ids()
        if(id in outputs) :
            raise ValueError("Erreur un noeux en output ne peut pas avoir de fils")
        new_id = self.add_node("",{id : 1}, {})
        self.add_output_id(new_id)
    
    # remove functions
    def remove_edges(self, *args : List[Tuple[int, int]] ) -> None:
        """
        enleve un lien parent/enfant entre les pairs d'id donnee en parametre
        Si apres avoir retire les liens, un des 2 noeud (par pair) n'a plus aucun lien il n'est pas retire de self.node 
        (On assume qu'il peut peut etre etre reutilise dans le future)
        param:
        args - (int * int) list; list de pair src/tgt
                src - int , l'id du parent/enfant du lien a enlever
                tgt - int , l'id de l'enfant/parent du lien a enlever
        """
        if len(args) == 1:
            pair = args[0]
            src, tgt = pair[0], pair[1]
            n1 = self.get_node_by_id(src) 
            n2 = self.get_node_by_id(tgt)
            res = False
            if tgt in n1.get_children_ids().keys():
                res = n1.remove_child_once(tgt)
                n2.remove_parent_once(src)
            return res
        for src, tgt in args:
            n1 = self.get_node_by_id(src) 
            n2 = self.get_node_by_id(tgt)
            if tgt in n1.get_children_ids().keys():
                n1.remove_child_once(tgt)
                n2.remove_parent_once(src)
                self.nodes[src] = n1
                self.nodes[tgt] = n2
    def remove_edge(self, src:int, tgt:int) ->bool:
        """
        enleve un lien parent/enfant entre src/tgt d'id donnee en parametre
        Si apres avoir retire le lien, un des 2 noeud n'a plus aucun lien il n'est pas retire de self.node 
        (On assume qu'il peut peut etre etre reutilise dans le future)
        param:
        src - int , l'id du parent/enfant du lien a enlever
        tgt - int , l'id de l'enfant/parent du lien a enlever
        return bool si une seul pair est donne en parametre sinon None; true si il exsistait un lien entre les 2 noeud, false sinon
        """
        return self.remove_edges((src, tgt))

    def remove_several_parallel_edges(self, *args : List[Tuple[int, int]]) -> None:
        """
        enleve tous les liens entre les pairs d'id donnee en parametre
        Si apres avoir retire les liens , un des 2 noeud n'a plus aucun lien il n'est pas retire de self.node 
        (On assume qu'il peut peut etre etre reutilise dans le future)
        param:
        args - (int * int) list; list de pair src/tgt
                src - int , l'id du parent/enfant du lien a enlever
                tgt - int , l'id de l'enfant/parent du lien a enlever
        """
        for (src, tgt) in args:
            while(self.remove_edge(src, tgt)):
                pass
    def remove_parallel_edge(self, src:int, tgt:int)->None:
        """
        enleve tous les liens entre les noeud src/tgt d'id donnee en parametre
        Si apres avoir retire les liens , un des 2 noeud n'a plus aucun lien il n'est pas retire de self.node 
        (On assume qu'il peut peut etre etre reutilise dans le future)
        param:
        src - int , l'id du parent/enfant du lien a enlever
        tgt - int , l'id de l'enfant/parent du lien a enlever
        """
        self.remove_several_parallel_edges((src, tgt))

    def remove_nodes_by_id(self, *args : List[int]) -> None:
        """
        retire les aretes associees aux noeuds donnee en parametre comme il faut
        et les retire de self.nodes et self.inputs/self.outputs si ils en font partie
        param:
        *args- int list ; la list d'id 
        """
        for i in args:
            n = self.nodes.pop(i)
            parents = n.get_parent_ids()
            enfant = n.get_children_ids()
            for id in parents: # retire toute les liaisons entre le noeud d'id i et ses parents
                n1 = self.get_node_by_id(id)
                n1.remove_child_id(i)
                self.nodes[id] = n1
            for id in enfant: # retire toute les liaisons entre le noeud d'id i et ses enfants
                n1 = self.get_node_by_id(id)
                n1.remove_parent_id(i)
                self.nodes[id] = n1
            if i in self.inputs: # retire le noeud d'id i des inputs si il en fait partie
                self.inputs.remove(i)
            if i in self.outputs:# retire le noeud d'id i des outputs si il en fait partie
                self.outputs.remove(i)
    def remove_node_by_id(self, id:int) -> None:
        """
        retire les aretes associees au noeud donnee en parametre comme il faut;
        et les retirer de self.nodes et self.inputs/self.outputs si ils en font partie
        param:
        id- int ; l'id du noeud 
        """
        self.remove_nodes_by_id(id)

    #testing
    def is_well_formed(self) -> bool:
        """
        pour qu'un graphe soit bien il doit respecter les 4 propriete suivante:
        — chaque noeud d'inputs et d'outputs doit etre dans le graphe (i.e. son
        id comme cle dans nodes)
        — chaque noeud input doit avoir un unique fils (de multiplicite 1) et pas de
        parent
        — chaque noeud output doit avoir un unique parent (de multiplicite 1) et
        pas de fils
        — chaque cle de nodes pointe vers un noeud d'id la cle
        — si j a pour fils i avec multiplicite m, alors i doit avoir pour parent j avec
        multiplicite m, et vice-versa

        return vrai si les 4 propriete sont respecte, faux sinon
        """
        try:
            inputs = self.get_inputs_ids()
            outputs = self.get_outputs_ids()
            id_nodes = self.get_id_nodes_map()
            for i in inputs: # verifie si tout les inputs on bien 0 parents et 1 fils
                inp = id_nodes[i]
                if len(inp.parents) != 0 or len(inp.children) != 1:
                    print("erreur en rapport avec les inputs")
                    return False
            for i in outputs:# verifie si tout les outputs on bien 1 parents et 0 fils
                out = id_nodes[i]
                if len(out.children) != 0 or len(out.parents) != 1:
                    print("erreur en rapport avec les outputs")
                    return False
            for id in id_nodes: # verifie si les arrete sont bien construite
                n = id_nodes[id]
                if n.get_id() != id:
                    print("erreur en rapport avec le dict id : node")
                    return False
                for id_parent in n.parents:
                    parent = id_nodes[id_parent]
                    if (parent.children[id] != n.parents[id_parent]):
                        print("erreur en rapport avec les relation pere/fils")
                        return False
            return True
        except:
            print("probleme d'id dans id_node ou relation parent/enfant")
            return False
    
    # cycle function
    
    def is_cyclic(self) -> bool:
        """verifie si un graph dirige est bien cyclic

        Returns:
            bool: rend true si il est cyclic, false sinon
        """
        graph = self.copy()
        def function(g:open_digraph):
            id_node = g.get_id_nodes_map()
            if id_node == {}: 
                return False
            for id, node in id_node.items():
                if node.get_parent_ids() == {}:
                    g.remove_node_by_id(id)
                    return function(g)
            return True # si a un moment pendant l'appel recursif de la fonction tous les noeuds du graphe ont des parents
        return function(graph)
    
    
    