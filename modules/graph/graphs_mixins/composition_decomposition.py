from typing import List, Dict, Tuple
from modules.node.node import *

class open_digraph_composition_decomposition_mx:
    def shift_indices(self, n:int) -> None:
        """ ajoute n a tous les indices du graph

        Args:
            n (int): _description_
        """
        def list_addition(i):
            return i+n
        def dic_addition(pair):
            new_id = pair[0] + n
            new_node : node = pair[1]
            new_node.parents  = {i+n :j for i,j in new_node.parents.items()}
            new_node.children = {i+n :j for i,j in new_node.children.items()}
            new_node.set_id(new_id)
            return (new_id, new_node)
        self.inputs = list(map(list_addition, self.inputs)) 
        self.outputs = list(map(list_addition, self.outputs))
        self.nodes = dict(map(dic_addition, self.nodes.items()))
        self.nextId += n
        
    def iparallel(self, g : 'open_digraph') -> None:
        """ change l'objet tel qu'il devient la composition parallele de lui meme et du graph donne en parametre

        Args:
            g (open_digraph): le graph qui servira a la composition. notons que ce dernier ne sera modifie
        """
        graph = g.copy()
        graph.shift_indices(self.nextId)
        self.inputs = self.inputs + graph.inputs
        self.outputs = self.outputs + graph.outputs
        self.nodes.update(graph.nodes)
        self.nextId = graph.nextId
        
    @classmethod
    def parallel(cls, f : 'open_digraph', g : 'open_digraph') -> 'open_digraph':
        """fait la composition sequentielle de 2 graph donne en parametre
            les graph donnee en parametre ne serons pas modifie

        Args:
            f (open_digraph): les deux graph a fusonne
            g (open_digraph): les deux graph a fusonne

        Returns:
            open_digraph :  la composition parallel de f et g
        """
        f1 = f.copy()
        f1.iparallel(g)
        return f1
    
    @classmethod
    def identity(cls, n : int) -> 'open_digraph':
        """cree un open_digraph representant l'identite sur n fils

        Args:
            n (int): le nomrbe de fils

        Returns:
            open_digraph : open_digraph representant l'identite sur n fils
        """
        input_id = [i for i in range(n)]
        ouput_id = [i for i in range(n, 2 * n)]
        tab = [node(0, 0, {}, {}) for _ in range(2 * n)]
        for i in range(n):
            n_par = node(i, '', {}, {i + n: 1})
            n_child = node(i + n, '', {i: 1}, {})
            tab[i] = n_par
            tab[i + n] = n_child
        g = cls(input_id, ouput_id, tab)
        return g
        
    def icompose(self, f : 'open_digraph') -> List[int]:
        """change l'objet tel qu'il devient la composition sequentielle de lui meme et du graph donne en parametre

        Args:
            f (open_digraph): le graph qui servira a la composition. notons que ce dernier ne sera modifie

        Raises:
            Exception: si le nombre de inputs de f n'est pas egal au nombre de outputs de l'objet
            
        Returns:
            List[int]: l'id des noeuds qui ont servi de soudur entre les deux graphes
        """
        if len(self.outputs) != len(f.inputs) :
            raise Exception(f"le graph entree en parametre a {len(f.inputs)} porte d'entree alors que {len(self.outputs)} etais attendu")
        graph = f.copy()
        inputs_ids = graph.get_inputs_ids().copy()
        outputs_ids = self.get_outputs_ids().copy()
        inputs = graph.get_nodes_by_ids(inputs_ids)
        outputs = self.get_nodes_by_ids(outputs_ids)
        graph.set_input_ids([
            (list(inp_nod.get_children_ids().keys())[0], graph.remove_node_by_id(inp_nod.get_id()))[0] \
            if inp_nod.outdegree() == 1 \
            else inp_nod.get_id() \
            for inp_nod in inputs \
                ])
        self.set_outputs_ids([list(out_nod.get_parent_ids().keys())[0] for out_nod in outputs])
        self.remove_nodes_by_id(*outputs_ids)
        graph.shift_indices(self.nextId)
        self.nodes.update(graph.nodes)
        soude = graph.inputs
        n_nodes = zip(self.outputs, graph.inputs)
        for inp, out in n_nodes:
            self.add_edge(inp, out)
        self.outputs = graph.outputs 
        self.nextId = graph.nextId
        return soude
    
    @classmethod
    def compose(cls, f : 'open_digraph', g : 'open_digraph') -> 'open_digraph':
        """fait la composition sequentielle de 2 graph donne en parametre
            les graph donnee en parametre ne serons pas modifie
        Args:
            g (open_digraph): le graphe "enfant"
            f (open_digraph): le graph "parent"

        Returns:
            open_digraph : la composition sequetielle de f et g
        """
        f1 = f.copy()
        f1.icompose(g)
        return f1
        
        
    def connected_components(self) -> Tuple[int, Dict[int,int]]:
        """
        le nombre de composantes connexes, et un dictionnaire
        qui associe a chaque id de noeuds du graphe un int qui correspond a une
        composante connexe.
        
        Returns:
            tulpe[int, dict]: int - le nombre de composants annexe
                              dict - un dictionnaire qui associe a chaque id de noeuds 
                                    du graphe un int qui correspond a la composante connexe 
                                    a laquel il appartient
        """
        graph = self.copy()
        id_composant_dict = {}
        def join(id:int, l:list):
            
            if id in l:
                return
            l.append(id)
            nod = graph.get_node_by_id(id)
            connection = nod.get_children_ids()
            connection.update(nod.get_parent_ids())
            connection = connection.keys()
            graph.remove_node_by_id(id)
            for i in connection:
                join(i, l)
        nombre_composant_connexe = 0 # compteur du nombre de composante annexe
        while graph.nodes != {}:
            l = []
            id = list(graph.nodes.keys())[0]
            join(id, l)
            id_composant_dict.update({i : nombre_composant_connexe for i in l})
            nombre_composant_connexe += 1
        return nombre_composant_connexe, id_composant_dict
    
    def split_in_components(self) -> List['open_digraph']:
        """ divise le graphe en plusieurs  graphes representant les composante connexe de ce dernier
        important -- les graphes creer n'ont pas de input et/ou output 

        Returns:
            List[open_digraph]: la liste des composantes creer 
        """
        n, d = self.connected_components()
        divise = [[]*n]
        for id, component in d.items():
            divise[component].append(self.get_node_by_id(id))
        return [open_digraph([], [], l) for l in divise]
    
    
    
    def fusion(self, id1:int, id2:int) -> None:
        """
        fusion deux noeud d'un graph,
        noter que le noeud emergeant est en realite le premier donne en parametre 
        donc l'id du premier noeud sera toujours accessible dans le graphe
        alors que celle du deuxieme noeud est supprime du graphe
        
        Args:
            id1 (int): l'id du premier noeud
            id2 (int): l'id du deuxieme noeud
        """
        N = self.get_id_nodes_map()
        n2 = N[id2]
        child2 = n2.get_children_ids().copy()
        par2 = n2.get_parent_ids().copy()
        for ids in child2:
            if(ids != id1) :
                self.add_edge(id1, ids)
        for ids in par2:
            if(ids != id1):
                self.add_edge(ids, id1)
        self.remove_node_by_id(id2)


    