from typing import List

class bool_circ_reecriture_noeud_mx():
    def associativite_OU_ET(self,id1:int) -> List[int]:
        """COMME POUR L'ASSOCIATIVITE DU XOR LE OU/ET SUIVENT CETTE MEME REGLE, IL EST POSSIBLE DE TOUT FAIRE DANS UNE MEME FONCTION MEME ETANT DONNE QUE NOUS L'AVONS RAJOUTE
            IL EST DEMANDE DE LA METTRE EN VALEUR DANS LA DOC STRING
            EN EFFET, 
                                     A    B                A  B  C
            ASSOCIATIVITE DU ET :     \  /                  \ | / 
                                        &    C    --->>       &
                                         \  /  
                                           & 
                                     A    B                A  B  C
            ASSOCIATIVITE DU OU :     \  /                  \ | / 
                                       OU    C    --->>       OU
                                         \  /  
                                          OU           
                                           
        
        Args:
            id1 (int): l'id du et/ou parent
        Returns:
            (int): id du noeud emergeant
        """
        return self.associativite_Xor(id1)

    
    
    def associativite_Xor(self,id1:int) -> List[int]:
        """fusionne de xor adjacent. c'est une propriete du xor

        Args:
            id1 (int): l'id du xor parent
        Returns:
            (int): id du noeud emergeant
        """
        n_ou = self.get_node_by_id(id1)
        n_ou2 = list(n_ou.get_children_ids().keys())[0]
        self.remove_edge(id1, n_ou2)
        self.fusion(id1,n_ou2)
        return [id1]
    
    def associativite_copie(self,*args:List[int])-> List[int]:
        """fusionne de copi adjacente.

        Args:
            args (List[int]): soit l'id de la copi parent soit les ids des 2 copie adjacentes
        Returns:
            (int): id du noeud emergeant
        """
        if len(args) == 2:
            self.remove_edges((args[0], args[1]), (args[1], args[0]))
            self.fusion(args[0], args[1])
            return args[0]
        copi = self.get_node_by_id(args[0])
        child = copi.get_children_ids().copy()
        for id in child.keys():
            nod = self.get_node_by_id(id)
            if nod.get_label() == '' and id not in self.get_outputs_ids():
                self.associativite_copie(args[0], id)
        return [args[0]]
    
    def involution_Xor(self,id2:int, id1:int)->List[int]:
        """applique l'involution du xor lorsqu'un noeud d copi est connecte au xor plus d'une fois

        Args:
            id2 (int): l'id de la copi
            id1 (int): l'id du xor
        Returns:
            List[int]: le id du xor
        """
        id_ou =self.get_node_by_id(id1)
        copy = id_ou.get_parent_ids()
        mul = copy[id2]
        if(mul%2 == 1):
            while(mul!=1):
                self.remove_edge(id2, id1)
                mul-=1
        else :
            self.remove_parallel_edge(id2, id1)
        return [id1]

    def effacement(self,id1:int)->List[int]:
        """lorsqu'une operation pointe vers une copi vide elle est efface ainsi que tous les parent qui sont connecter a ce noeud
        voir la documentation de la fonction self.simplifie_copy_vide 
        pour plus de detaille et une meilleur explication

        Args:
            id1 (int): l'operation

        Returns:
            List[int]: liste des ids des noeud pour lesques il exsiste un chemin qui les relis a la copi vide, 
            mais tel que se n'est pas l'unique chemin
        """
        n_op = self.get_node_by_id(id1)
        par = n_op.get_parent_ids().copy()
        n_enf =list(n_op.get_children_ids().keys())[0]
        if n_enf in self.get_outputs_ids():
            return []
        new =[]
        for id in par :
            copi_vide = self.add_node('',{id:1},{})
            new += self.simplifie_copy_vide(copi_vide)
        self.remove_node_by_id(id1)
        self.remove_node_by_id(n_enf)
        return new
    
    def non_xor(self, id:int)->List[int]:
        """simplifie le pattern non xor (n -> ~ -> ^)

        Args:
            id (int): l'id du non qui le xor pour enfant
        Returns:
            List[int]: l'id du xor et de son fils devenu un non
        """
        non = self.get_node_by_id(id)
        xor_id = list(non.get_children_ids().keys())[0]
        xor = self.get_node_by_id(xor_id)
        par_non = list(non.get_parent_ids().keys())[0]
        self.add_edge(par_non, xor_id)
        non.set_label("1")
        self.ou_exlusif(id)
        new_non = list(xor.get_children_ids().keys())[0]
        return [new_non, xor_id]
        
    def non_copie(self,id:int)->List[int]:
        """simplifie le pattern non copie (n -> ~ -> '' => _ )

        Args:
            id (int): l'id du non qui la copi pour enfant
        Returns:
            List[int]: l'id de la copie
        """
        non = self.get_node_by_id(id)
        copyId = list(non.get_children_ids().keys())[0]
        par_non = list(non.get_parent_ids().keys())[0]
        self.add_edge(par_non, copyId)
        self.remove_node_by_id(id)
        copy = self.get_node_by_id(copyId)
        children = copy.get_children_ids().copy()
        for ids, mul in children.items():
            self.remove_parallel_edge(copyId, ids)
            for i in range(mul):
                self.add_node('~', {copyId:1}, {ids:1})
        return [copyId]
                
    def non_non(self, id:int) -> List[int]:
        """simplifie le pattern non non (n -> ~ -> ~ -> )

        Args:
            id (int): l'id du non qui le xor pour enfant
        Returns:
            List[int]: l'id de l'enfant du deuxieme non
        """
        non_p = self.get_node_by_id(id)
        non_cId = list(non_p.get_children_ids().keys())[0]
        non_c = self.get_node_by_id(non_cId)    
        gp = list(non_p.get_parent_ids().keys())[0]
        pe = list(non_c.get_children_ids().keys())[0]
        self.remove_nodes_by_id(id, non_cId)
        self.add_edge(gp, pe)
        return [pe]
    
    def simplifie_copy_vide(self, id) -> List[int]:
        """prend une copie vide qui n'est pas un output et supprime tous les noeud exclusivement attache a ceux noeud

        Args:
            id (int): id de la copie vide

        Returns:
            List[int]: liste des ids des noeud pour lesques il exsiste un chemin qui les relis a la copi vide, mais tel que se n'est pas
            l'unique chemin
            
        """
        cv = self.get_node_by_id(id)
        parent_id = list(cv.get_parent_ids().keys())
        return_val = []
        for pid in parent_id:
            parent = self.get_node_by_id(pid)
            if parent.outdegree() == 1:
                return_val += self.simplifie_copy_vide(pid)
            else:
                return_val += [pid]
        self.remove_node_by_id(id)
        return return_val
        
    
    def simplifie_copi(self, id:int) -> List[int]:
        """simplifie un noeud de copi si possible

        Args:
            id (int): l'id de la copie

        Returns:
            List[int]: la liste des noeuds qui appartiennt toujours au circuit mais qui ont ete modifie
        """
        noeud = self.get_node_by_id(id)
        children = noeud.get_children_ids().copy()
        if len(children) == 0: # verifie si ce noeud (id = id) est une copi vide
            return self.simplifie_copy_vide(id)
        res = []
        a_change = False
        for id_child, mul in children.items():
            child =  self.get_node_by_id(id_child)
            if id_child in self.get_outputs_ids():
                continue
            elif child.get_label() == '':
                self.simplifie_copi(id_child)
                self.associativite_copie(id, id_child)
                a_change = True
            elif child.get_label() == '^' and mul>1:
                res += self.involution_Xor(id, id_child)
        if a_change:
            res += [id]
        return res
            
    def simplifie_xor_et_ou(self, id:int):
        """simplifie les noeud ou/et/xor si possible

        Args:
            id (int): l'id du noeud qui est un et/ou/xor

        Returns:
            List[int]: la liste des noeud qui ont ete modifie
        """
        this = self.get_node_by_id(id)
        this_label = this.get_label()
        id_child = list(this.get_children_ids().keys())[0]
        child =self.get_node_by_id(id_child)
        child_label = child.get_label()
        if id_child in self.get_outputs_ids():
            return []
        elif child.outdegree() == 0:
            return self.effacement(id)
        elif child_label == this_label:
            res = self.associativite_Xor(id)
        return res
        
    def simplifie_non(self, id:int):
        """simplifie un noeud evalue a non

        Args:
            id (int): l'id du noeud evalue a non

        Returns:
            List[int]: liste des noeuds qui ont ete modifie
        """
        non = self.get_node_by_id(id)
        children_id = list(non.get_children_ids().keys())[0]
        children = self.get_node_by_id(children_id)
        label = children.get_label()
        res = []
        if children in self.get_outputs_ids():
            return res
        elif children.outdegree() == 0:
            return self.effacement(id)
        elif label == '':
            res += self.non_copie(id)
        elif label == '~':
            res += self.non_non(id)
        elif label == '^':
            res += self.non_xor(id)
        return res
        
    def simplifie_noeud(self, id:int)->List[int]:
        """prend un noeud quelquonque, feuille ou pas et cherche a se s'en servir pour simplifier le graph

        Args:
            id (int): l'id du noeud

        Returns:
            List[int]: la list des noeud qui ont ete modifie
        """
        noeud = self.get_node_by_id(id)
        label = noeud.get_label()
        if len(noeud.get_parent_ids()) == 0:
            res = self.simplifi_feuille(id)
        elif label == '':
            res = self.simplifie_copi(id)
        elif label == '~':
            res = self.simplifie_non(id)
        else:                                   # '&' '^' '|'
            res = self.simplifie_xor_et_ou(id)
        return res
        
    def simplifie_arbre(self) -> None:
        """
        calcule la valeur des outputs du circuit

        """
        select = list(self.get_id_nodes_map().keys())
        peut_simplifier = []
        for id in select:   #   onessaye de simplifier tous les noeuds
            if id not in self.get_outputs_ids():
                try:
                    peut_simplifier += self.simplifie_noeud(id)
                except:# si sa fail c'est que fid ne fait plus parti du graph car il a ete simplifie 
                    continue
        while len(peut_simplifier) != 0: # cette liste contient tous les noeud qui ont une chance d'etre simplifiable
            fid = peut_simplifier.pop(0)
            
            try:
                
                noeud_adja = self.simplifie_noeud(fid) # simplifie un noeud va changer l'etat d'autre noeud dans le processus
                peut_simplifier += noeud_adja # on ajoute les noeud ces noeud la liste 
            except: # si sa fail c'est que fid ne fait plus parti du graph car il a ete simplifie 
                continue