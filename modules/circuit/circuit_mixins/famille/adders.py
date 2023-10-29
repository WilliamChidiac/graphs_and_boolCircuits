from typing import List, Dict, Tuple

class bool_circ_famille_adder_mx():
    @classmethod
    def adder(cls, n:int) -> 'bool_circ':
        """creer un graphe de la famille des adder

        Args:
            n (int): le nombre de sorti sera egal a 2 a la puissance n

        Returns:
            bool_circ: le Adder creer
        """
        if n == 0:
            adder, _ = cls.parse_parenthese("((a)&(b))|((b)&(c))|((a)&(c))", "(a)^(b)^(c)")
            return adder
        else:
            g1 = cls.identity(2 ** (n))
            g1_bis = cls.adder(n - 1)
            g1.iparallel(g1_bis)
            g2 = g1_bis
            g2.iparallel(cls.identity(2 ** (n - 1)))
            g1.icompose(g2)
            inputs_old = g1.get_inputs_ids()
            for i in range(2 ** (n - 1), 2 ** (n)):
                var = inputs_old[i + 2 ** (n - 1)]
                inputs_old[i + 2 ** (n - 1)] = inputs_old[i]
                inputs_old[i] = var
            g1.set_input_ids(inputs_old)
            return cls(g1)
        
    @classmethod
    def Half_Adder(cls, n:int, id:bool=False) -> 'bool_circ':
        """creeer un graph de la famille des half adder

        Args:
            n (int): le nombre de sorti sera egal a 2 a la puissance n

        Returns:
            bool_circ: le half adder creer
        """
        g1 = cls.adder(n)
        inputs = g1.get_inputs_ids()
        nodes = g1.get_id_nodes_map()
        in_enleve = inputs[len(inputs) - 1] 
        inputs.remove(in_enleve)
        in_enleve = nodes[in_enleve]
        in_enleve.set_label("0")
        if id:
            return cls(g1), in_enleve.get_id()
        return cls(g1)

    @classmethod
    def from_entier_to_registre(cls, numero:int, taille_reg:int=8) -> 'bool_circ':
        """genere un registre a partir d'un entier donne

        Args:
            numero (int): l'entier a represente
            taille_reg (int, optional): la taille maximal du registre. Defaults to 8.

        Raises:
            ValueError: si le registre a taille trop petite pour represente l'entier voulu

        Returns:
            bool_circ: le registre cree
        """
        binaire = bin(numero)[2:]
        if (len(binaire) > taille_reg):
            raise ValueError("Imposil fonction calcul entier")
        binaire = '0'*(taille_reg-len(binaire)) + binaire
        g = cls.empty()
        for i in binaire:
            idd = g.add_node(i, {}, {})
            g.add_output_node(idd)
        return cls(g)