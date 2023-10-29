from typing import List, Dict, Tuple

class node:
    def __init__(self, identity : int , label : str, parents : Dict[int, int], children : Dict[int, int]):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children
    def __str__(self) -> str:
        return str(self.parents)+ " ->  " + str(self.id) + " -> " + str(self.children)

    def __repr__(self) -> str:
        return str(self)

    def copy(self):
        """
        rend une copie du noeud
        """
        children = self.children.copy()
        parent = self.parents.copy()
        id = self.id
        label = self.label
        return node(id, label, parent, children)

    #gettters
    def get_id(self) -> int:
        """
        rend l'id du noeud
        """
        return self.id
    def get_label(self) -> str:
        """
        rend le label du noeud
        """
        return self.label
    def get_parent_ids(self) -> Dict[int, int]:
        """
        rend le dictionnaire des (id : multiplicite) des parents du noeud
        """
        return self.parents
    def get_children_ids(self) -> Dict[int, int]:
        """
        rend le dictionnaire des (id : multiplicite) des enfants du noeud
        """
        return self.children
    #setters
    def set_id(self, id : int) ->None : 
        """
        associe au noeud une id donnee en parametre
        param : 
        id - int
        """
        self.id = id
    def set_label(self, label : str) ->None : 
        """
        associe au noeud un label donnee en parametre
        param : 
        label - str
        """
        self.label = label
    def set_parents_ids(self, pids : Dict[int, int]) -> None : 
        """
        associe au noeud ces parents donnee en parametre
        param : 
        pids - (int : int) dict
        """
        self.parents = pids
    def set_children_ids(self, cids : Dict[int, int]) :
        """
        associe au noeud ces enfants donnee en parametre
        param : 
        cids - (int : int) dict
        """
        self.children = cids
    def add_child_id(self, id : int) -> None:
        """
        rajoute au enfant du noeud, le noeud d'id donne en parametre
        id - int l'id du nouvel enfant
        """
        if id in self.children.keys():
            self.children[id] += 1
        else :
            self.children[id] = 1
    def add_parent_id(self, id : int) -> None:
        """
        rajoute au parent du noeud, le noeud d'id donnee en parametre
        id - int l'id du nouveau parent
        """
        if id in self.parents.keys():
            self.parents[id] += 1
        else :
            self.parents[id] = 1
    
    #methode
    def remove_parent_once(self, id : int) -> bool:
        """
        enleve un lien entre le noeud son parent d'id donnee
        parametre:
        id - int ; l'id du parent en question
        return bool ; true si un lien a ete enleve, false sinon (c'est a dire il n'y avait de lien entre le noeud source et le d'id "id") 
        """
        parents = self.get_parent_ids()
        if id in parents.keys():
            if parents[id] == 1:
                del parents[id]
            else:
                parents[id] -= 1
            self.set_parents_ids(parents)
            return True
        return False
    def remove_child_once(self, id : int) -> bool:
        """
        enleve un lien entre le noeud son enfant d'id donnee
        parametre:
        id - int ; l'id de l'enfant en question
        return bool ; true si un lien a ete enleve, false sinon (c'est a dire il n'y avait de lien entre le noeud source et le d'id "id") 
        """
        children = self.get_children_ids()
        if id in children.keys():
            if children[id] == 1:
                del children[id]
            else:
                children[id] -= 1
            self.set_children_ids(children)
            return True
        return False
    def remove_parent_id(self, id : int ) -> bool:
        """
        enleve tous les liens entre le noeud et son parent d'id donnee
        parametre:
        id - int ; l'id du parent en question
        return bool ; true si un lien a ete enleve, false sinon (c'est a dire il n'y avait de lien entre le noeud source et le d'id "id") 
        """
        parents = self.get_parent_ids()
        try :
            del parents[id]
            self.set_parents_ids(parents)
            return True
        except:
            return False
    def remove_child_id(self, id : int ) -> bool:
        """
        enleve tous les liens entre le noeud et son enfant d'id donnee
        parametre:
        id - int ; l'id de l'enfant en question
        return bool ; true si un lien a ete enleve, false sinon (c'est a dire il n'y avait de lien entre le noeud source et le d'id "id") 
        """
        children = self.get_children_ids()
        try :
            del children[id]
            self.set_children_ids(children)
            return True
        except:
            return False

    #degree function
    def indegree(self) -> int:
        return sum(self.parents.values())
    def outdegree(self) -> int:
        return sum(self.children.values())
    def degree(self) -> int:
        return self.indegree() + self.outdegree()