from typing import List, Tuple

class bool_circ_famille_Hammig_mx():
    @classmethod
    def encodeur(cls) -> 'bool_circ' :
        """construit l'encodeur de Hamming

        Returns:
            bool_circ: encodeur
        """
        a, b =  cls.parse_parenthese("(a)^(b)^(d)","(a)^(c)^(d)","a","(b)^(c)^(d)","b","c","d")
        return a
    @classmethod
    def decodeur(cls) -> 'bool_circ':
        """construit le decodeur de Hamming

        Returns:
            bool_circ: le decodeur
        """
        moitie, b = cls.parse_parenthese("(a)^(c)^(e)^(g)","(b)^(c)^(f)^(g)","c","(d)^(e)^(f)^(g)","e","f","g")
        moitie2, b= cls.parse_parenthese("((x0)&(x1)&(~(x3)))^(x2)","((x0)&(~(x1))&(x3))^(x4)","((~(x0))&(x1)&(x3))^(x5)","((x0)&(x1)&(x3))^(x6)")
        moitie.icompose(moitie2)
        return moitie
    
    @classmethod
    def encodeur_decodeur_erreur(cls, *position:int) -> 'bool_circ':
        """construit un circuit encodeur decodeur avec ou sans erreurs de transmission
        
        Args:
            *position (int): les index des outputs change durant la transmission
            
            
        Returns:
            bool_circ: le circuit encodeur decodeur
        """
        encodeur = cls.encodeur()
        decodeur = cls.decodeur()
        output = encodeur.icompose(decodeur)
        if position == [-1]:
            return encodeur
        for pos in position:
            id_erreur = output[pos]
            enfant = encodeur.get_node_by_id(id_erreur)
            parent = list(enfant.get_parent_ids().keys())[0]
            encodeur.add_node('~', {parent:1}, {id_erreur:1})
            encodeur.remove_edge(parent, id_erreur)
        return encodeur
    
    @classmethod
    def envoi_message_hamming(cls, decimal:int, position_erreur:int=-1) -> Tuple['bool_circ', int]:
        """prend le message initial entre dans l'encodeur, l'envoi au decodeur qui le decodera

        Returns:
            Tuple[bool_circ, int]: la premiere valeur designe le registre apres avoir decoder le message, 
                                   la deuxieme valeur designe l'entier represente par ce registre
        """
        self = cls.encodeur_decodeur_erreur(*position_erreur)
        registre:cls = cls.from_entier_to_registre(decimal, 4)
        registre.icompose(self)
        registre.simplifie_arbre()
        number = registre.from_registre_to_number()
        return registre, number  
    
    def from_registre_to_number(self) -> int:
        """pour un circuit de type identite, calcule l'entier decimal qui represente le registre 

        Returns:
            int: l'entier
        """
        outputs_id = self.get_outputs_ids()
        outputs = self.get_nodes_by_ids(outputs_id)
        binaire = ''
        for out in outputs:
            parent_id = list(out.get_parent_ids().keys())[0]
            parent = self.get_node_by_id(parent_id)
            binaire += parent.get_label()
        return int(binaire, 2)
        