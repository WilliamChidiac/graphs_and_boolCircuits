from typing import List


class bool_circ_reecriture_feuille_mx():    
    def copie(self, id:int) -> List[int]:
        """simplifie l'operation copie

        Args:
            id (int): l'id du noeud qui a la copie pour enfant. Ce noeud est en realite une feuille evalue a 0 ou 1

        Returns:
            List[int]: la list des enfant de la copie qui sont devenu des feuille evalue a 0 ou 1 apres simplification
        """
        nod = self.get_node_by_id(id)
        enfant = list(nod.get_children_ids().keys())[0] #recupere l'enfant
        value = nod.get_label()
        e = self.get_node_by_id(enfant)
        children_mul = e.get_children_ids().copy()
        self.remove_nodes_by_id(id, enfant)
        new_cof = []
        for id, mul in children_mul.items():
            for i in range(mul):
                new_cof.append(self.add_node(value, {}, {id:1}))
        return new_cof
        
    def non(self, id1:int) -> int:
        """simplifie l'operation negation

        Args:
            id (int): l'id du noeud qui a la negation pour enfant. Ce noeud est en realite une feuille evalue a 0 ou 1

        Returns:
            int: l'enfant du non qui est devenu une feuille evalue a 0 ou 1 apres simplification
        """
        n1 = self.get_node_by_id(id1)
        label = str((int(n1.get_label())+1)%2)
        n_not_id = list(n1.get_children_ids().keys())[0]
        n_not = self.get_node_by_id(n_not_id)
        enf = list(n_not.get_children_ids().keys())[0]
        
        self.remove_node_by_id(n_not_id)
        n1.set_label(label)
        self.add_edge(id1, enf)
        return id1

    def et(self, id1:int) -> int:
        """simplifie l'operation 'et paresseu'

        Args:
            id1 (int): l'id du noeud qui a le noeud 'et' pour enfant. Ce noeud est en realite une feuille evalue a 0 ou 1

        Returns:
            int: l'enfant du 'et' qui est devenu une feuille evalue a 0 ou 1 apres simplification
        """
        n1 = self.get_node_by_id(id1)
        operation_et_id = list(n1.get_children_ids().keys())[0]
        operation_et = self.get_node_by_id(operation_et_id)
        if (n1.get_label() == "1"):
            self.remove_node_by_id(id1)
            try:
                brother = list(operation_et.get_parent_ids().keys())[0]
                return brother
            except:
                return operation_et_id
        else:
            
            enf = list(operation_et.get_children_ids().keys())[0]
            par = operation_et.get_parent_ids().copy()
            self.remove_node_by_id(operation_et_id)
            for id in par.keys():
                if (id != id1):
                    copi_vide = self.add_node('', {id: 1}, {})
                    self.simplifie_copy_vide(copi_vide)
            
            self.add_edge(id1, enf)
            
            return id1

    def ou(self, id1:int) -> int:
        """simplifie l'operation 'ou paresseu'

        Args:
            id1 (int): l'id du noeud qui du ou pour enfant. Ce noeud est en realite une feuille evalue a 0 ou 1

        Returns:
            int: l'enfant du ou qui est devenu une feuille evalue a 0 ou 1 apres simplification
        """
        nb = self.get_node_by_id(id1)
        current_label = nb.get_label()
        new_label = str((int(current_label)+1)%2)
        nb.set_label(new_label)
        co_f = self.et(id1)
        if co_f == id1:
            nb.set_label(current_label)
        return co_f
       
        
    def ou_exlusif(self, id1) -> int:
        """simplifie l'operation 'ou exclusif'

        Args:
            id1 (int): l'id du noeud qui du ou pour enfant. Ce noeud est en realite une feuille evalue a 0 ou 1

        Returns:
            int: l'enfant du ou qui est devenu une feuille evalue a 0 ou 1 apres simplification
        """
        n1 = self.get_node_by_id(id1)
        operation_xor_id = list(n1.get_children_ids().keys())[0]
        operation_xor = self.get_node_by_id(operation_xor_id)
        if (n1.get_label() == "0"):
            return self.ou(id1)
        else:
            co_f = self.et(id1)
            enf = list(operation_xor.get_children_ids().keys())[0]
            self.add_node('~', {operation_xor_id:1}, {enf:1})
            self.remove_edge(operation_xor_id, enf)
            return co_f

    def neutre(self, id1) -> int:
        """simplifie les operateur binaire une lorsqu'il n'ont plus de parents

        Args:
            id1 (int): l'id de l'operateur binaire

        Raises:
            ValueError: si l'id donne ne represente pas un operateur binaire

        Returns:
            int: la valeur de la nouvelle feuille
        """
        n1 = self.get_node_by_id(id1)
        label = n1.get_label()
        if (label == "|" or label == "^"):
            n1.set_label('0')
        elif label == "&":
            n1.set_label('1')
        else:
            raise ValueError("le noeud n'est pas une operation binaire")
        return id1

        
    def simplifi_feuille(self, id : int) -> List[int]:
        """simplifie la partie du graph connecter a un noeud si ce dernier est une feuille (pas de parent)
        
        Args:
            id (int): l'id du noeud en question
            
        Returns:
            List[int]: list des 'voisins' du noeud apres simplification
        """
        outp = self.get_outputs_ids()
        co_f = self.get_node_by_id(id)
        lab = co_f.get_label()
        parent = co_f.get_parent_ids().keys()
        # if 62 in parent:
        #     print('bdckjsdbcdscbkj')
        #     print(co_f)
        #     print(co_f.get_label())
        #     self.display(True)
        enf_ids = list(co_f.get_children_ids().keys()).copy()
        noeud_adja = []
        if len(enf_ids) == 0:
            self.remove_node_by_id(id)
            return []
        for enf_id in enf_ids:
            enf = self.get_node_by_id(enf_id)
            lab_enf = enf.get_label()
            if len(co_f.get_parent_ids()) != 0:
                return []
            if (lab == "|" or lab == "&" or lab == "^"):
                newId = self.neutre(id)
                noeud_adja += self.simplifi_feuille(newId)
            elif enf_id not in outp:
                if lab_enf == "&":
                    noeud_adja += [self.et(id)]
                elif lab_enf == "|":
                    noeud_adja += [self.ou(id)]  
                elif lab_enf == "^":
                    noeud_adja += [self.ou_exlusif(id)]
                elif lab_enf == "~":
                    newId = self.non(id)
                    noeud_adja += self.simplifi_feuille(newId)
                elif lab_enf == '':
                    newIds = self.copie(id)
                    for i in newIds:
                        noeud_adja += self.simplifi_feuille(i) 
            else:
                return []
        return noeud_adja    
        
        
    def evaluate(self) -> None:
        """
        calcule la valeur des outputs du circuit

        """
        feuille = [id for id, n in self.get_id_nodes_map().items() if n.get_parent_ids() == {}]
        while len(feuille) != 0:
            fid = feuille.pop(0)
            try:
                noeud_adja = self.simplifi_feuille(fid)
                feuille += noeud_adja
            except:
                continue