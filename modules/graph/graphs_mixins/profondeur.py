from typing import List, Dict, Tuple

class open_digraph_profondeur_mx:
    def tri_topologique(self) -> List[List[int]]:
        """fait le tri topologique du graph si ce dernier est acyclique. 

        Raises:
            Exception: si le graph est cyclique

        Returns:
            List[List[int]]: la liste du tri topologique donc pour tout i, li contient les noeud de profondeur i
        """
        graph : open_digraph = self.copy()
        entree_sorti = graph.inputs + graph.outputs
        graph.remove_nodes_by_id(*entree_sorti) # retire tous les input et output nodes
        tri_topo = []
        def tri(): # le nombre d'appel a la fonction est egal a la profondeur du graphe
            if graph.nodes == {}:
                return 
            co_feuille = []
            for id, nod in graph.nodes.items(): # rassemble tous les noeuds qui n'ont pas de parent
                if nod.get_parent_ids() == {}:
                    co_feuille.append(id)
            if co_feuille == []:
                raise Exception("ce graph n'est pas acyclique.")
            graph.remove_nodes_by_id(*co_feuille)
            tri_topo.append(co_feuille)
            tri()
        tri()
        return tri_topo
    
    def get_profondeur_by_id(self, id:int) -> int:
        """etant donne une id calcule la profondeur du noeud associe a cet id dans le graphe

        Args:
            id (int): l'id du noeud en question

        Raises:
            Exception: si l'id n'existe pas dans le graphe ou si le graph est cyclique

        Returns:
            int: la profondeur du noeud
        """
        tri = self.tri_topologique()
        for i in range(len(tri)):
            if id in tri[i]:
                return i
        raise Exception("id inexisante.")
    
    def get_profondeur(self) -> int:
        """ calcule la profondeur du graph

        Returns:
            int: la profondeur
        """
        return len(self.tri_topologique())
    
    def plus_long_chemin(self, src:int, tgt:int) -> Tuple[int, List[int]]:
        def dist_max_prev_max():
            """utilise une methode tre proche de l'algo de dijkstra pour trouve le chemin le plu long

            Raises:
                Exception: si tgt n'est jamais atteint 
            """
            tri = self.tri_topologique()
            prof_src = self.get_profondeur_by_id(src)
            dist = {src:0} # dict[id, distance a src]
            prev = {} # dict[id, id noeud precedent pour arriver a src]
            node_ids = []
            for i in range(prof_src, len(tri)): 
                # on regroupe toutes les ids de noeud de profondeur plus grande que celle de src en un seul iterable
                node_ids += tri[i]
            for w in node_ids:
                parents = list(self.get_node_by_id(w).get_parent_ids().keys()) #  liste des parent de w
                max_dist_id = -1 
                max_dist = -1
                for p_id in parents:
                    try:
                        if dist[p_id] > max_dist:
                            max_dist = dist[p_id]
                            max_dist_id = p_id
                    except:
                        pass
                if max_dist != -1:
                    dist[w] = max_dist+1
                    prev[w] = max_dist_id
                if w == tgt:
                    return dist[w], prev
            raise Exception(" le noeud target n'a pas etait trouve")
        
        chemin = []
        distance, prev = dist_max_prev_max()
        def build_path(id):
            """reconstruit le chemin a partir de prev

            Args:
                id (int): l'id du noeud source
            """
            if id == src:
                chemin.append(id)
            else :
                build_path(prev[id])
                chemin.append(id)
        try:
            build_path(tgt)
        except:
            raise Exception(f"il n'y a aucun chemin qui reli le noeud d'id {src} au noeud d'id {tgt} en utilisant la direction donne.")
        return distance, chemin