from modules.circuit.bool_circ_mixins import *


class bool_circ(open_digraph,
                bool_circ_famille_adder_mx,
                bool_circ_reecriture_feuille_mx,
                bool_circ_reecriture_noeud_mx,
                bool_circ_famille_Hammig_mx):
    def __init__(self, *args):
        if len(args) == 1:
            digraph = args[0]
        else:
            digraph = open_digraph(*args)
        self.inputs = digraph.inputs.copy()
        self.outputs = digraph.outputs.copy()
        self.nextId = digraph.nextId
        self.nodes ={id : nodes.copy() for id,nodes in digraph.nodes.items()}
        if not self.is_well_formed():
            raise Exception("ce graph ne peut pas etre en un circuit booleen")
        
    
    
    def is_well_formed(self) -> bool:
        """verifie si la structure du graph est bien celle d'un circuit de booleen

        Returns:
            bool: true si c'est un graph de booleen false sinon
        """
        if self.is_cyclic():
            return False
        inputs = self.get_inputs_ids()
        nodes = self.get_nodes()
        for nod in nodes:
            nod = nod.copy()
            if nod.get_id() in inputs:
                if nod.indegree() != 0:
                    return False
            elif nod.get_label() == "":
                if nod.indegree() != 1 :
                    return False
            elif nod.get_label() == "&" or nod.get_label() == "|" or nod.get_label() == "^":
                if nod.outdegree() != 1:
                    return False
            elif nod.get_label() == "~":
                if nod.indegree() != 1 or nod.outdegree() != 1:
                    return False
            elif nod.get_label() != '0' and nod.get_label() != '1':
                
                return False
        return True
    
    @classmethod
    def parse_parenthese(cls, *args) -> Tuple['bool_circ', List[str]]:
        """
        prend en parametre une d'expressions booleenne, les fusionnes et creer leur circuit respectif si possible

        Raises:
            Exception: si c'est impossible de le convertir

        Returns:
            Tuple[bool_circ, List[str]]: le circuit booleen creer et une liste des labels de ses variable dans le meme ordre que celui des input du graph
        """
        key_words = ["&", "|", "~", "1", "0", "^", '']
        g = cls.empty()
        for s in args:
            current_node = g.add_node()
            g.add_output_node(current_node)
            s2 : str = ''
            for c in s:
                if c == '(':
                    nods = g.get_id_nodes_map()
                    n = nods[current_node]
                    if (n.get_label() == ''):
                        n.set_label(s2)
                    elif (n.get_label() != s2):
                        raise Exception("Impossible")
                    par = g.add_node(label='', parents={}, children={current_node: 1})
                    current_node = par
                    s2 = ''
                elif c == ')':
                    n = g.get_id_nodes_map()[current_node]
                    n.set_label(n.get_label() + s2)

                    current_node = list(n.get_children_ids().keys())[0]
                    s2 = ''
                else:
                    if(len(s) ==1):
                        n = g.get_id_nodes_map()[current_node]
                        n.set_label(c)
                    s2 += c
        pfua = g.get_id_nodes_map().copy()
        dic = {}
        for id, n in pfua.items():
            label = n.get_label()
            if (label not in key_words):
                if label in dic:
                    g.fusion(dic[label], id)
                else:
                    dic[label] = id
                n.set_label('') 
        sorted_dict = {}
        for key in sorted(dic.keys()):
            sorted_dict[key] = dic[key]
        for ids in sorted_dict.values():
            g.add_input_id(ids)
        return bool_circ(g), list(sorted_dict.keys())
    
    @classmethod
    def generate(cls, n:int, num_inputs:int=2, num_outputs:int=2, bound:int=3) -> 'bool_circ':
        """genere aleatoirement un circuit booleen etant donne des parametre

        Args:
            n (int): le nombre de noeud que son graph 'ancetre' aura
            num_inputs (int, optional): nombre de inputs qu'il contiendra. Defaults to 2.
            num_outputs (int, optional): nombre d'outputs qu'il contiendra. Defaults to 2.
            bound (int, optional): nombre maximal d'arrete par lien que son graph contiendra. Defaults to 3.

        Returns:
            bool_circ: le circuit booleen creer 
        """
        g:open_digraph = open_digraph.random(n, bound, form="DAG loop-free")
        op_b = ["&", "|", "^"]
        op_u = "~"
        op_c = ""
        graph_nodes = g.get_id_nodes_map().copy()
        for id, node in graph_nodes.items(): # ajoute des inputs/output nodes a tous les noeud qui n'ont pas de parent/enfant
            if node.get_children_ids() == {}:
                g.add_output_node(id)
            if node.get_parent_ids() == {}:
                g.add_input_node(id)
        
        inputs = g.get_inputs_ids()
        outputs =g.get_outputs_ids()
        while len(inputs) < num_inputs: # ajoute des input tant que le nombre de input desirer n a pas etait atteint
            id = randint(0, n-1)
            g.add_input_node(id)
        while len(outputs) < num_outputs: # ajoute des outputs tant que le nombre de outputs n'a pas ete atteint
            id = randint(0, n-1)
            g.add_output_node(id)
        while len(inputs) > num_inputs: # enleve des inputs tant que le nombre de inputs du graphe est supperieur a celui voulu
            n_inp = len(inputs)-1
            id2 = inputs.pop(randint(0, n_inp))
            id1 = inputs[randint(0, n_inp-1)]
            g.fusion(id1, id2)
        while len(outputs) > num_outputs: # enleve des outputs tant que le nombre de outputs du graphe est supperieur a celui voulu
            n_inp = len(outputs)-1
            id2 = outputs.pop(randint(0, n_inp))
            id1 = outputs.pop(randint(0, n_inp-1))
            g.fusion(id1, id2)
            nod = g.get_node_by_id(id1)
            nod.set_label(op_b[randint(0, 2)])
            g.add_output_node(id1)
        for id, node in graph_nodes.items():
            degp = node.indegree()
            degm = node.outdegree()
            if degp*degm == 1:
                node.set_label(op_u)
            elif degp == 1 and degm > 1:
                node.set_label(op_c)
            elif degp == 2 and degm == 1:
                operation = op_b[randint(0, 2)]
                node.set_label(operation)
            else:
                parents = node.get_parent_ids().copy()
                children = node.get_children_ids().copy()
                operation = op_b[randint(0, 2)]
                uop = g.add_node(operation, parents)
                g.add_node(op_c, {uop:1}, children)
                nop = g.get_node_by_id(uop)
                while nop.indegree() > 2:
                    p = list(nop.get_parent_ids().copy().items())
                    i1 = p[0][0]
                    if p[0][1] >1:
                        i2 = p[0][0]
                    else:
                        i2 = p[1][0]
                    g.remove_edge(i1, uop)
                    g.remove_edge(i2, uop)
                    op = op_b[randint(0, 2)]
                    g.add_node(op, {i1:2} if i1==i2 else {i1:1, i2:1}, {uop:1})
                g.remove_node_by_id(id)
        return bool_circ(g)