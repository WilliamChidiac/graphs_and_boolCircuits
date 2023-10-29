import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.graph.open_digraph import *
from modules.circuit.bool_circ import *

class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node) 

    def test_init_open_digraph(self):
        n0 = node(0, 'x1', {}, {3:1})
        n1 = node(1, 'x2', {}, {2:1})
        n2 = node(2, '~', {1:1}, {3:1})
        n3 = node(3, '&', {0:1, 2:1}, {})
        graph = open_digraph([0, 1], [3], [n0, n1, n2, n3])
        self.assertEqual(graph.inputs, [0, 1])
        self.assertEqual(graph.outputs, [3])
        self.assertEqual(graph.nodes, {0:n0, 1:n1, 2:n2, 3:n3})
        self.assertEqual(graph.nextId, 4)
        self.assertIsInstance(graph, open_digraph)

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {}, {1 : 1, 3 : 2})
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')    
    def test_copy(self):
        self.assertIsNot(self.n0.copy(), self.n0)
        print("\n test node.copy")
        print(self.n0.copy())
        print(self.n0)

    def test_add_childNparent_id(self):
        self.n0.add_child_id(1)
        self.n0.add_parent_id(2)
        self.assertEqual(self.n0.children, {1 : 2, 3 : 2})
        self.assertEqual(self.n0.parents, {2 : 1})

    def test_remove_childNParent_once(self):
        self.n0.remove_child_once(1)
        self.n0.remove_child_once(3)
        self.n0.remove_parent_once(2)
        self.assertEqual(self.n0.children, {3 : 1})
        self.assertEqual(self.n0.parents, {})
    def test_remove_childNparent_id(self):
        self.n0.remove_child_id(1)
        self.assertEqual(self.n0.children, {3 : 2})
        self.n0.remove_child_id(3)
        self.assertEqual(self.n0.children, {})
        self.n0.remove_parent_id(2)
        self.assertEqual(self.n0.parents, {})
    


class OpenDigraphTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'x1', {}, {3:1})
        self.n1 = node(1, 'x2', {}, {2:1})
        self.n2 = node(2, '~', {1:1}, {4:2})
        self.n3 = node(3, '&', {0:1, 4:1}, {5:1})
        self.n4 = node(4, '&', {2:2}, {3:1})
        self.n5 = node(5,  '~', {3 : 1}, {})
        self.graph = open_digraph([0, 1], [5], [self.n0, self.n1, self.n2, self.n3, self.n4, self.n5])
        self.n6 = node(0, "", {}, {5:1})
        self.n7 = node(5, '', {0:1}, {})
        self.g = open_digraph([0], [5], [self.n6, self.n7])
        ni1 = node(10, "", {}, {0:1})
        ni2 = node(11, "", {}, {2:1})
        no1 = node(12, '', {7 : 1}, {})
        n0 = node(0, "", {10:1}, {3 : 1})
        n1 = node(1, "", {}, {5 : 1, 4 : 1, 8:1})
        n2 = node(2, "", {11:1}, {4 : 1})
        n3 = node(3, "", {0 : 1}, {5 : 1, 6:1, 7:1})
        n4 = node(4, "", {1 :1, 2: 1}, {6 : 1})
        n5 = node(5, "", {1 : 1, 3 : 1}, {7:1})
        n6 = node(6, "", {3 : 1, 4 : 1}, {8:1, 9:1})
        n7 = node(7, "", {3:1, 5:1}, {12:1})
        n8 = node(8, "", {1 :1 , 6:1}, {})
        n9 = node(9, "", {6:1}, {})
        self.graph_complexe = open_digraph([10, 11],[12], [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9, ni1, ni2, no1])


    def test_get_inputs_ids(self):
        self.assertEqual(self.graph.get_inputs_ids(), [0, 1])
    def test_get_outputs_ids(self):
        self.assertEqual(self.graph.get_outputs_ids(), [5])
    def test_get_nodes_ids(self):
        self.assertEqual(self.graph.get_id_nodes_map(), {0:self.n0, 1:self.n1, 2:self.n2, 3:self.n3, 4:self.n4, 5 : self.n5})
    def test_copy(self):
        copy = self.graph.copy()
        self.assertIsNot(copy, self.graph)
        self.assertEqual(copy.inputs, [0, 1])
        self.assertEqual(copy.outputs, [5])
        print("\ntest open_digrpah.copy")
        print(self.graph.nodes)
        print(copy.nodes)

    def test_add_edge(self):
        self.graph.add_edge(2, 4)
        self.graph.add_edge(0, 1)
        self.assertEqual(self.graph.nodes[0].children, {3:1, 1:1})
        self.assertEqual(self.graph.nodes[1].parents, {0:1})
        self.assertEqual(self.graph.nodes[2].children, {4:3})
        self.assertEqual(self.graph.nodes[4].parents, {2:3})
    def test_add_edges(self):
        self.graph.add_edges([(2, 4), (0, 1)])
        self.assertEqual(self.graph.nodes[0].children, {3:1, 1:1})
        self.assertEqual(self.graph.nodes[1].parents, {0:1})
        self.assertEqual(self.graph.nodes[2].children, {4:3})
        self.assertEqual(self.graph.nodes[4].parents, {2:3})
    def test_add_node(self):
        id = self.graph.add_node("test", {2 : 1}, {4 : 2})
        self.assertEqual(self.graph.nodes[2].children, {4:2, 6 : 1})
        self.assertEqual(self.graph.nodes[6].parents, {2 : 1})
        self.assertEqual(self.graph.nodes[6].children, {4:2})
        self.assertEqual(self.graph.nodes[4].parents, {2:2, 6:2})

    def test_remove_edges(self):
        self.graph.remove_edges((2, 4), (0,3))
        self.assertEqual(self.graph.nodes[2].children, {4:1})
        self.assertEqual(self.graph.nodes[4].parents, {2 : 1})
        self.assertEqual(self.graph.nodes[0].children, {})
        self.assertEqual(self.graph.nodes[3].parents, {4 :1})
    def test_remove_several_parallel_edges(self):
        self.graph.remove_several_parallel_edges((2, 4), (0,3))
        self.assertEqual(self.graph.nodes[2].children, {})
        self.assertEqual(self.graph.nodes[4].parents, {})
        self.assertEqual(self.graph.nodes[0].children, {})
        self.assertEqual(self.graph.nodes[3].parents, {4 :1})
    def test_remove_nodes_by_id(self):
        self.graph.remove_nodes_by_id(4, 1)
        self.assertEqual(self.graph.nodes[2].children, {})
        self.assertEqual(self.graph.nodes[3].parents, {0:1})
        self.assertEqual(self.graph.nodes[2].parents, {})
        self.assertEqual(self.graph.inputs, [0])
        self.assertEqual(self.graph.nodes.pop(4, None), None)

    def test_is_well_formed(self):
        self.assertEqual(self.graph.is_well_formed(), True)
        self.graph.inputs = [2]
        self.assertEqual(self.graph.is_well_formed(), False)
        self.setUp()
        self.graph.outputs = [2]
        self.assertEqual(self.graph.is_well_formed(), False)
        self.setUp()
        self.n2.parents = {0 : 1, 1 : 1}
        graph = open_digraph([0, 1], [5], [self.n0, self.n1, self.n2, self.n3, self.n4, self.n5])
        self.assertEqual(graph.is_well_formed(), False)
        self.setUp()
        self.n2.parents = {1 : 2}
        graph = open_digraph([0, 1], [5], [self.n0, self.n1, self.n2, self.n3, self.n4, self.n5])
        self.assertEqual(graph.is_well_formed(), False)

    def test_add_inputNoutput_id(self):
        """
        les fonction input et output etant code de la maniere si l'une marche alors l'autre aussi
        """
        graphe = self.graph
        try:
            graphe.add_input_node(0)
            self.assertEqual(True, False)
        except:
            self.assertEqual(graphe, self.graph)
            pass
        self.graph.add_input_node(3)
        self.assertEqual(self.graph.inputs, [0, 1, 6])
        self.assertEqual(self.graph.nodes[6].children, {3:1})
        self.assertEqual(self.graph.nodes[6].parents, {})
        self.assertEqual(self.graph.nodes[3].parents, {0:1, 4:1, 6:1})

    def test_final(self):
        self.assertEqual(self.graph.is_well_formed(), True)
        self.graph.add_node("", {2 : 1}, {3 : 1})
        self.assertEqual(self.graph.is_well_formed(), True)
        self.graph.remove_node_by_id(4)
        self.assertEqual(self.graph.is_well_formed(), True)
        self.graph.add_input_node(2)
        self.assertEqual(self.graph.is_well_formed(), True)
        
    #def test_from_dot_file(self):
    #    self.graph.save_as_dot_file("input_file.dot")
    #    g = open_digraph.from_dot_file("input_file.dot")
    #    g.save_as_dot_file("test_file.dot")
    #    
    #def test_display(self):
    #    self.graph.display()

    def test_shift_indices(self):
        self.graph.shift_indices(3)
        self.assertEqual(self.graph.inputs, [3, 4])
        self.assertEqual(self.graph.outputs, [8])
        self.assertEqual(list(self.graph.nodes.keys()), [3,4,5,6,7,8])
        self.assertEqual(self.graph.nodes[6].parents, {3:1, 7:1} )
        self.assertEqual(self.graph.nodes[6].children,  {8:1})
        
    def test_iparallel(self):
        self.graph.iparallel(self.g)
        self.assertEqual(self.graph.inputs, [0, 1, 6]) #input ajoute
        self.assertEqual(self.graph.outputs, [5, 11]) # output ajoute
        self.assertEqual(self.graph.nextId, 12) # nextId modifie
        self.assertEqual(self.graph.get_nodes_ids(), [0, 1, 2, 3, 4, 5, 6, 11]) #noeud ajoute
        self.assertEqual(self.g.get_nodes_ids(), [0,5]) # graph donne en parametre pas modifie
        
    def test_icompose(self):
        self.graph.icompose(self.g)
        self.assertEqual(self.graph.inputs, [0, 1]) #input pas modifie
        self.assertEqual(self.graph.outputs, [11]) # output modifie
        self.assertEqual(self.graph.nextId, 12) #nextId modifie
        self.assertEqual(self.graph.get_nodes_ids(), [0, 1, 2, 3, 4, 11]) # noeud ajoute et output enleve
        self.assertEqual(self.graph.get_node_by_id(3).children, {11:1}) # verifie le lien entre graph.output et g.input
        self.assertEqual(self.g.get_nodes_ids(), [0,5])# g ne change pas
        
    def test_connected_components(self):
        self.graph.iparallel(self.g)
        nombre, dictoinnaire = self.graph.connected_components()
        self.assertEqual(nombre, 2)
        self.assertEqual(dictoinnaire, {0: 0, 3: 0, 5: 0, 4: 0, 2: 0, 1: 0, 6: 1, 11: 1})
        
    def test_djkstra(self):
        self.graph.icompose(self.g)
        dist, prev = self.graph.dijkstra(3)
        dist_tgt, prev_tgt = self.graph.dijkstra(3, tgt=11)
        self.assertEqual(dist,{3: 0, 0: 1, 4: 1, 2: 2, 11: 1, 1: 3})
        self.assertEqual(prev, {0: 3, 4: 3, 2: 4, 11:3, 1: 2})
        self.assertEqual(dist_tgt,{3: 0, 11: 1})
        self.assertEqual(prev_tgt, {11: 3})
        
    def test_shortest_path(self):
        self.graph.iparallel(self.g)
        chemin = self.graph.shortest_path(2, 3)
        self.assertEqual(chemin, [2, 4, 3])
        try:
            self.graph.shortest_path(3, 6)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)
        
    def distance_ancetre_commun(self):
        chemin = self.graph_complexe.distance_ancetre_commun(5, 8)
        self.assertEqual(chemin, {0 : (2, 3), 3 : (1, 2), 1 : (1, 1)})
        
    def test_tri_topologique(self):
        tri = self.graph_complexe.tri_topologique()
        self.assertEqual(tri, [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]])
        
    def test_get_profondeur_AND_profondeur_by_id(self):
       profondeur_graph = self.graph_complexe.get_profondeur() 
       profondeur_node_5 = self.graph_complexe.get_profondeur_by_id(5)
       self.assertEqual(profondeur_graph, 4)
       self.assertEqual(profondeur_node_5, 2)
       
    def test_plus_long_chemin(self):
        distance_1_5, chemin_1_5 = self.graph_complexe.plus_long_chemin(1, 5)
        distance_1_8, chemin_1_8 = self.graph_complexe.plus_long_chemin(1, 8)
        distance_0_7, chemin_0_7 = self.graph_complexe.plus_long_chemin(0, 7)
        self.assertEqual(distance_1_5, 1)
        self.assertEqual(distance_1_8, 3)
        self.assertEqual(distance_0_7, 3)
        self.assertEqual(chemin_1_5, [1, 5])
        self.assertEqual(chemin_1_8, [1, 4, 6, 8])
        self.assertEqual(chemin_0_7, [0, 3, 5, 7])
        
    def test_fusion(self):
        graph = self.graph_complexe
        graph.fusion(0, 2)
        nod = graph.get_node_by_id(0)
        self.assertEqual(nod.get_children_ids(), {3:1, 4:1})
        self.assertEqual(nod.get_parent_ids(), {10:1, 11:1})
        
    
        
       

class MatrixTest(unittest.TestCase):
    
    def test_graph_from_adjacency(self):
        matrice = random_oriented_int_matrix(5, 3)
        graphe : open_digraph = open_digraph.graph_from_adjancency_matrix(matrice)
        id_nodes = graphe.get_id_nodes_map()
        for i in range(5):
            for j in range(5):
                inod = id_nodes[i]
                jnod = id_nodes[j]
                if matrice[i][j] != 0:
                    self.assertEqual(j in inod.get_children_ids(), True)
                    self.assertEqual(i in jnod.get_parent_ids(), True)
                    self.assertEqual(inod.get_children_ids()[j], matrice[i][j])
                    self.assertEqual(jnod.get_parent_ids()[i], matrice[i][j])
                else :
                    self.assertEqual(j not in inod.get_children_ids(), True)
                    self.assertEqual(i not in jnod.get_parent_ids(), True)
    def test_random(self):
        graphe_DAG : open_digraph = open_digraph.random(5, 4, 0, 0, "DAG")
        graphe_oriented : open_digraph = open_digraph.random(5, 4, 0, 0, "oriented loop-free")
        graphe_non_dirige : open_digraph = open_digraph.random(5, 4, 0, 0, "undirected")
        graphe_loop_free : open_digraph = open_digraph.random(5, 4, 0, 0, "loop-free")
        def test_random_symetric():
            graph = graphe_non_dirige.adjacency_matrix()
            for i in range(5):
                for j in range(5):
                    self.assertEqual(graph[i][j], graph[j][i])
        def test_random_oriented():
            graph = graphe_oriented.adjacency_matrix()
            for i in range(5):
                for j in range(5):
                    if i == j:
                        self.assertEqual(graph[i][j], 0)
                    else:
                        self.assertEqual(graph[i][j] *graph[j][i], 0)
        def test_random_DAG():
            graph = graphe_DAG.adjacency_matrix()
            for i in range(5):
                for j in range(5):
                    if i > j:
                        self.assertEqual(graph[i][j], 0)
        def test_random_loop_free():
            graph = graphe_loop_free.adjacency_matrix()
            for i in range(5):
                self.assertEquals(graph[i][i], 0)
                
        test_random_DAG()
        test_random_loop_free()
        test_random_oriented()
        test_random_symetric()
        
        

class circ_boolTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, '1', {}, {3:1})
        self.n1 = node(1, '0', {}, {2:1})
        self.n2 = node(2, '~', {1:1}, {4:1})
        self.n3 = node(3, '&', {0:1, 4:1}, {5:1})
        self.n4 = node(4, '&', {2:1}, {3:1})
        self.n5 = node(5, '', {3 : 1}, {6 : 1, 7:1})
        self.n6 = node(6, '', {5:1}, {})
        self.n7 = node(7, '', {5:1}, {})
        self.graph = open_digraph([0, 1], [6, 7], [self.n0, self.n1, self.n2, self.n3, self.n4, self.n5, self.n6, self.n7])
        self.circ_booleen = bool_circ(self.graph)
        
        
    def test_is_well_formed(self):
        self.assertEqual(self.circ_booleen.is_well_formed(), True) # ce test ne sert a rien vu que pour creer la variable circ_booleen on appel cet fonction dans le constructeur de bool_circ.
        self.circ_booleen.add_node("~", {4 : 1}, {3:1})
        self.assertEqual(self.circ_booleen.is_well_formed(), False) # verifi les propriete du ou/et/ou exclusif -- &/|/^
        self.circ_booleen.add_edge(3, 4)
        self.assertEqual(self.circ_booleen.is_cyclic(), True) #verifie que la fonction is_cyclic marche bien
        self.circ_booleen = bool_circ(self.graph)
        self.circ_booleen.add_edge(1,2)
        self.assertEqual(self.circ_booleen.is_well_formed(), False) #
        self.circ_booleen = bool_circ(self.graph)            # verifie les propriete du non "~"
        self.circ_booleen.add_edge(2, 4)                            #         
        self.assertEqual(self.circ_booleen.is_well_formed(), False) #
        self.circ_booleen = bool_circ(self.graph)
        self.circ_booleen.add_edge(0,5)
        self.assertEqual(self.circ_booleen.is_well_formed(), False) # verifie les propriete de la copie
        
    def test_parse_parenthese(self):
        graph, variable = bool_circ.parse_parenthese("((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)") # le fait que la fonction ne rend pas une erreur montre deja que le circuit est bien un circuit booleen
        inputs = graph.get_inputs_ids()
        outputs = graph.get_outputs_ids()
        self.assertEqual(variable, ['x0', 'x1', 'x2'])
        self.assertEqual(len(inputs), 3)
        self.assertEqual(len(outputs), 2)

    def test_generate(self):
        graph = bool_circ.generate(4, 2, 2) # le fait que la fonction ne rend pas une erreur montre deja que le circuit est bien un circuit booleen
        inputs = graph.get_inputs_ids()
        outputs = graph.get_outputs_ids()
        self.assertEqual(len(inputs), 2)
        self.assertEqual(len(outputs), 2)
        
    def test_adder_halfAdder(self):
        graph = bool_circ.adder(2) # le fait que la fonction ne rend pas une erreur montre deja que le circuit est bien un circuit booleen
        self.assertEqual(len(graph.get_inputs_ids()), 9) # verifie nombre d'entre bien egal 2**(n+1)+1
        self.assertEqual(len(graph.get_outputs_ids()), 5) # verifie nombre de sorti bien egal a 2**n +1
        graph, id = bool_circ.Half_Adder(3, True) # le fait que la fonction ne rend pas une erreur montre deja que le circuit est bien un circuit booleen
        self.assertEqual(len(graph.get_inputs_ids()), 16) # verifie nombre d'entre bien egal 2**(n+1)+1
        self.assertEqual(len(graph.get_outputs_ids()), 9) # verifie nombre de sorti bien egal a 2**n +1
        self.assertEqual(graph.get_node_by_id(id).get_label(), '0') # verifie que la valeur du noeud a bien ete change a 0
    
    def test_from_entier_to_registre(self):
        graph:bool_circ = bool_circ.from_entier_to_registre(11)
        self.assertEqual(len(graph.get_outputs_ids()), 8) # taille du registre respecte
        binair = ''
        for i, n in graph.get_id_nodes_map().items():
            binair += n.get_label()
        self.assertEqual("00001011", binair) # s'assure que le registre creer est bien celui representant l'entier 11
        
    def test_copie(self):
        graph = bool_circ(
            [],
            [2, 3],
            [
                node(0, '0', {},{1:1}),
                node(1, '', {0:1},{2:1, 3:1}),
                node(2, '', {1:1},{}),
                node(3, '', {1:1},{})
            ]
        )
        cof = graph.copie(0)
        self.assertEqual(graph.get_inputs_ids(), [])
        self.assertEqual(graph.get_outputs_ids(), [2, 3])
        self.assertEqual(graph.get_node_by_id(2).get_parent_ids(), {4:1})
        self.assertEqual(graph.get_node_by_id(3).get_parent_ids(), {5:1})
        self.assertEqual(graph.get_node_by_id(4).get_label(), '0')
        self.assertEqual(graph.get_node_by_id(5).get_label(), '0')
        self.assertEqual(cof, [4, 5])
    
    def test_non(self):
        graph0 = bool_circ( [], [2],[ node(0, '0', {},{1:1}), node(1, '~', {0:1},{2:1}), node(2, '', {1:1},{})])
        graph1 = bool_circ( [], [2],[ node(0, '1', {},{1:1}), node(1, '~', {0:1},{2:1}), node(2, '', {1:1},{})])
        co0 = graph0.non(0)
        co1 = graph1.non(0)
        self.assertEqual(graph0.get_inputs_ids(), [])
        self.assertEqual(graph0.get_outputs_ids(), [2])
        self.assertEqual(graph0.get_node_by_id(0).get_parent_ids(), {})
        self.assertEqual(graph0.get_node_by_id(0).get_children_ids(), {2:1})
        self.assertEqual(graph0.get_node_by_id(0).get_label(), '1')
        self.assertEqual(graph1.get_node_by_id(0).get_label(), '0')
        self.assertEqual(co0, 0)
        self.assertEqual(co1, 0)
        
    def test_et(self):
        graphet = open_digraph(
            [],
            [3],
            [
                node(0, '0', {},{2:1}),
                node(1, '1', {},{2:1,  4:1}),
                node(2, '&', {1:1, 0:1},{3:1}),
                node(3, '', {2:1},{}),
                node(4, '', {1:1},{})
            ]
        )
        graph = bool_circ(graphet.copy())
        co0 = graph.et(0) # cas 1 du td
        self.assertEqual(graph.get_inputs_ids(), [])
        self.assertEqual(graph.get_outputs_ids(), [3])
        self.assertEqual(graph.get_node_by_id(3).get_parent_ids(), {0:1})
        self.assertEqual(graph.get_node_by_id(1).get_children_ids(), {4:1})
        self.assertEqual(graph.get_node_by_id(1).get_label(), '1')
        graph = bool_circ(graphet.copy())
        graph.get_node_by_id(0).set_label('1')
        c10 = graph.et(1) # cas 2 du td
        self.assertEqual(graph.get_inputs_ids(), [])
        self.assertEqual(graph.get_outputs_ids(), [3])
        self.assertEqual(graph.get_node_by_id(3).get_parent_ids(), {2:1})
        self.assertEqual(graph.get_node_by_id(2).get_parent_ids(), {0:1})
        c00 = graph.et(c10)
        self.assertEqual(co0, 0)
        self.assertEqual(c10, 0)
        self.assertEqual(c00, 2)
        
    def test_ou(self):
        graphet = open_digraph(
            [],
            [3],
            [
                node(0, '1', {},{2:1}),
                node(1, '0', {},{2:1}),
                node(2, '|', {1:1, 0:1},{3:1}),
                node(3, '', {2:1},{})
            ]
        )
        graph = bool_circ(graphet.copy())
        c0 = graph.ou(0) #cas 2 du td
        self.assertEqual(graph.get_inputs_ids(), [])
        self.assertEqual(graph.get_outputs_ids(), [3])
        self.assertEqual(graph.get_node_by_id(3).get_parent_ids(), {0:1})
        graph = bool_circ(graphet.copy())
        graph.get_node_by_id(0).set_label('0')
        c10 = graph.ou(1) # cas 1 du td
        self.assertEqual(graph.get_inputs_ids(), [])
        self.assertEqual(graph.get_outputs_ids(), [3])
        self.assertEqual(graph.get_node_by_id(3).get_parent_ids(), {2:1})
        self.assertEqual(graph.get_node_by_id(2).get_parent_ids(), {0:1})
        c11 = graph.ou(0)
        self.assertEqual(c0, 0)
        self.assertEqual(c10, 0)
        self.assertEqual(c11, 2)
        
    def test_ou_exclusif(self):
        graphet = open_digraph(
            [],
            [3],
            [
                node(0, '1', {},{2:1}),
                node(1, '0', {},{2:1}),
                node(2, '^', {1:1, 0:1},{3:1}),
                node(3, '', {2:1},{})
            ]
        )
        graph = bool_circ(graphet.copy())
        c00 = graph.ou_exlusif(0) # cas 2 du td
        self.assertEqual(graph.get_inputs_ids(), [])
        self.assertEqual(graph.get_outputs_ids(), [3])
        self.assertEqual(graph.get_node_by_id(3).get_parent_ids(), {4:1})
        self.assertEqual(graph.get_node_by_id(4).get_parent_ids(), {2:1})
        self.assertEqual(graph.get_node_by_id(4).get_label(), '~')
        c01 = graph.ou_exlusif(1)
        graph = bool_circ(graphet.copy())
        c10 = graph.ou_exlusif(1) # cas 1 du td
        self.assertEqual(graph.get_inputs_ids(), [])
        self.assertEqual(graph.get_outputs_ids(), [3])
        self.assertEqual(graph.get_node_by_id(3).get_parent_ids(), {2:1})
        self.assertEqual(graph.get_node_by_id(2).get_parent_ids(), {0:1})
        c11 = graph.ou_exlusif(0)
        self.assertEqual(c00, 1)
        self.assertEqual(c10, 0)
        self.assertEqual(c01, 2)
        self.assertEqual(c11, 2)
        
    def test_neutre(self):
        g1 = bool_circ([],[], [node(0, '&', {}, {1:1}), node(1, '', {0:1},{})])
        g2 = bool_circ([],[], [node(0, '^', {}, {1:1}), node(1, '', {0:1},{})])
        g3 = bool_circ([],[], [node(0, '|', {}, {1:1}), node(1, '', {0:1},{})])
        g1.neutre(0) # cas 2 du td
        g2.neutre(0) # csa 1.2 du td
        g3.neutre(0) # cas 1.1 du td
        self.assertEqual(g1.get_node_by_id(0).get_label(), '1')
        self.assertEqual(g2.get_node_by_id(0).get_label(), '0')
        self.assertEqual(g3.get_node_by_id(0).get_label(), '0')
    
    
    def test_associativite_xor(self):
        g = bool_circ(
            [],
            [3],
            [
                node(0, '1', {},{2:1}),
                node(1, '0', {},{2:1}),
                node(5, '0', {},{4:1}),
                node(6, '0', {},{4:1}),
                node(2, '^', {1:1, 0:1},{4:1}),
                node(4, '^', {6:1, 5:1, 2:1},{3:1}),
                node(3, '', {4:1},{})
            ]
        )
        c = g.associativite_Xor(2)
        nod = g.get_node_by_id(*c)
        self.assertEqual(nod.get_parent_ids(), {0:1, 1:1, 6:1, 5:1} )
        self.assertEqual(nod.get_children_ids(), {3:1} )
    
    def test_associativite_copi(self):
        g = bool_circ(
            [],
            [0, 1, 5, 6],
            [
                node(0, '',{2:1}, {}),
                node(1, '',{2:1}, {}),
                node(5, '',{4:1}, {}),
                node(6, '',{4:1}, {}),
                node(2, '',{4:1}, {1:1, 0:1}),
                node(4, '',{3:1}, {2:1, 6:1, 5:1}),
                node(3, '1',{}, {4:1})
            ]
        )
        
        c = g.associativite_copie(4)
        c = g.associativite_copie(4)
        nod = g.get_node_by_id(*c)
        self.assertEqual(nod.get_parent_ids(), {3:1} )
        self.assertEqual(nod.get_children_ids(), {6:1, 5:1, 1:1, 0:1} )    

    def test_involution_xor(self):
        g = bool_circ(
            [],
            [3],
            [
                node(1, '0', {},{2:1}),
                node(5, '0', {},{4:1}),
                node(6, '0', {},{4:1}),
                node(2, '', {1:1},{4:2, 7:1}),
                node(4, '^', {6:1, 5:1, 2:2},{3:1}),
                node(3, '', {4:1},{}),
                node(7, '', {2:1},{})
            ]
        )
        g.involution_Xor(2, 4)
        nodou = g.get_node_by_id(4)
        nodcop = g.get_node_by_id(2)
        self.assertEqual(nodou.get_children_ids(), {3:1} )
        self.assertEqual(nodcop.get_children_ids(), {7:1})
        self.assertEqual(nodou.get_parent_ids(), {6:1, 5:1}) 
        self.assertEqual(nodcop.get_parent_ids(), {1:1}) 
    
    def test_effacement(self):
        graphet = bool_circ([],[3],[node(0, '1', {},{2:1}),node(1, '0', {},{2:1}),node(2, '|', {1:1, 0:1},{3:1}),node(3, '', {2:1},{})])
        l = graphet.effacement(2)
        self.assertEqual(graphet.get_outputs_ids(),[3])
        self.assertEqual(graphet.get_node_by_id(2).get_children_ids(),{3:1})
        graphet.set_outputs_ids([])
        l = graphet.effacement(2)
        self.assertEqual(l,[1, 0])
        self.assertEqual(graphet.get_node_by_id(0).get_children_ids(),{})
        self.assertEqual(graphet.get_node_by_id(1).get_children_ids(),{})
    
    def test_non_xor(self):
        graphet = bool_circ(
            [],
            [3],
            [
                node(0, '1', {},{4:1}),
                node(4, '~', {0:1},{2:1}),
                node(1, '0', {},{2:1}),
                node(2, '^', {1:1, 4:1},{3:1}),
                node(3, '', {2:1},{})
            ]
        )
        graphet.non_xor(4)
        self.assertEqual(graphet.get_node_by_id(2).get_children_ids(),{5:1})
        self.assertEqual(graphet.get_node_by_id(2).get_parent_ids(),{1:1, 0:1})
        
    def test_non_copy(self):
        graph = bool_circ(
            [],
            [2, 3],
            [
                node(0, '0', {},{4:1}),
                node(4, '~', {0:1},{1:1}),
                node(1, '', {4:1},{2:1, 3:1}),
                node(2, '', {1:1},{}),
                node(3, '', {1:1},{})
            ]
        )
        graph.non_copie(4)
        copy = graph.get_node_by_id(1)
        self.assertEqual(copy.get_children_ids(), {5:1, 6:1})
        self.assertEqual(copy.get_parent_ids(), {0:1})
        self.assertEqual(graph.get_node_by_id(2).get_parent_ids(), {5:1})
        self.assertEqual(graph.get_node_by_id(3).get_parent_ids(), {6:1})
        
    def test_non_non(self):
        graph0 = bool_circ( [], [2],[ node(0, '0', {},{3:1}),node(3, '~', {0:1},{1:1}), node(1, '~', {3:1},{2:1}), node(2, '', {1:1},{})])    
        graph0.non_non(3)
        self.assertEqual(graph0.get_node_by_id(0).get_children_ids(), {2:1})
    
    def test_evaluate_simplifie_arbre(self):
        g : bool_circ = bool_circ.adder(2)
        registre:bool_circ = bool_circ.from_entier_to_registre(11, 9)
        registre.display(True, path='reg.pdf')
        registre1:bool_circ = bool_circ.from_entier_to_registre(11, 9)
        registre.icompose(g)
        registre1.icompose(g)
        registre.display(True, path='adder.pdf')
        original_outputs = registre.get_outputs_ids().copy()
        registre.evaluate()
        print(registre.from_registre_to_number())
        registre.display(True)
        registre1.simplifie_arbre()
        output = registre.get_outputs_ids()
        inputs = registre.get_inputs_ids()
        nNodes = len(registre.get_id_nodes_map())
        output1 = registre1.get_outputs_ids()
        inputs1 = registre1.get_inputs_ids()
        nNodes1 = len(registre1.get_id_nodes_map())
        self.assertEqual(output, original_outputs)
        self.assertEqual(inputs, [])
        self.assertEqual(nNodes, 10)
        self.assertEqual(output1, original_outputs)
        self.assertEqual(inputs1, [])
        self.assertEqual(nNodes1, 10)
    
    def test_encodeur_decodeur_1erreur(self):
        for message in range(16):
            for pos_erreur in range(7):
                hamming, number = bool_circ.envoi_message_hamming(message, [pos_erreur])
                self.assertEqual(number, message)
        
    def test_encodeur_decodeur_2erreur(self):
        for message in range(16):
            for pos_erreur1 in range(7):
                for pos_erreur2 in range(pos_erreur1+1, 7):
                    erreur = [pos_erreur1, pos_erreur2]
                    hamming, number = bool_circ.envoi_message_hamming(message, erreur)
                    self.assertNotEqual(number, message)
                    
if __name__ == '__main__': 
    unittest.main()




