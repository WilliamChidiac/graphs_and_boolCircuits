from typing import List, Dict, Tuple

class open_digraph_distance_mx:
    def dijkstra(self, src : int, direction = None, tgt : int = None) -> Tuple[Dict[int, int], Dict[int, int]]: 
        """ applique l'algorithm de dijkstra sur un noeud donne

        Args:
            src (int): l'id du noeud pour lequel on cherche a calculer la distances de tous les chemin possible
            direction (int, optional): quand evalue a 1 le sens des fleche est pris en compte
                                       quand evalue a -1 on prend en compte le sens inverse
                                       Defaults to None : on ne prend pas en compte le sens des fleche

        Returns:
            Tuple[Dict[int, int], Dict[int, int]]: une pair de dictionnaire (dist, prev)
                    dist (Dict[int, int]) : associe a chaque id de noeud la distance qu'il le separe de 'src' 
                    prev (Dict[int, int]) : associe a chaque id de noeud l'id du noeud qui vien juste avant lui pour arrive a 'src
                important -- seul les noeuds pour lesquels il existe un chemin se trouve dans dist
        """
        Q = [src]
        dist = {src : 0} 
        prev = {}
        if tgt == src :
            return dist, prev
        f = lambda u : dist[u]
        while Q != []:
            id_u = min(Q, key=f)
            u = self.get_node_by_id(id_u)
            Q.remove(id_u)
            if direction == 1: # va dans le sens des fleche du graphe dirige
                voisin = u.get_children_ids().keys()
            elif direction == -1: # va a contre sens des fleche
                voisin = u.get_parent_ids().keys()
            else: # ne  prend pas en compte le sens
                voisin = u.get_children_ids()
                voisin.update(u.get_parent_ids())
                voisin = list(voisin.keys())
            
            for v in voisin:
                appartient_pas = v not in dist
                if appartient_pas:
                    Q.append(v)
                if appartient_pas or dist[v] > dist[id_u]+1:
                    dist[v] = dist[id_u]+1
                    prev[v] = id_u
                if tgt  == v: # on se premet de mettre le if ici vu que le arrete ont toute un poids de 1
                    return dist, prev
        return dist, prev
                

    def shortest_path(self, src:int, tgt:int, direction = None) -> List[int]:
        """trouve le chemin le plus cour entre 2 noeuds

        Args:
            src (int): le noeud de depart
            tgt (int): le noeud d'arrive
            direction (int, optional): la direction dans lequel on a le droit de ce deplacer
                                        Defaults to None.

        Returns:
            List[int]: la suite des ids des noeuds par lesquels on passe pour arrive de src a tgt
            
        """
        _, prev = self.dijkstra(src, direction, tgt)
        chemin = []
        def build_path(id):
            if id == src:
                chemin.append(id)
            else :
                build_path(prev[id])
                chemin.append(id)
        try:
            build_path(tgt)
        except:
            raise Exception(f"il n'y a aucun chemin qui reli le noeud d'id {src} au noeud d'id {tgt} en utilisant la direction donne.")
        return chemin
    
    def distance_ancetre_commun(self, id1:int, id2:int) -> Dict[int, Tuple[int, int]]:
        dist1, _ = self.dijkstra(id1, direction=-1) # dist1 : dict[id ancetre de id1, distance jusqu'a id1]
        dist2, _ = self.dijkstra(id2, direction=-1) # dist2 : dict[id ancetre de id2, distance jusqu'a id2]
        res = {}
        dist = dist1 if len(dist1) < len(dist2) else dist2
        for id in dist:
            try:
                res[id] = (dist1[id], dist2[id])
            except:
                pass
        return res