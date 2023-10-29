import os
import sys
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
from modules.node.node import node
from random import randint
from typing import List, Dict

def random_int_list(n : int, bound : int) -> List[int]:
    """
    genere une liste de taille n contenant des entiers (aleatoires) entre 0 et bound
    """
    return [ randint(0, bound) for i in range(n)]

def random_int_matrix(n:int, bound:int, null_diag=True)-> List[List[int]]:
    """
    genere une matrice n x n avec ses elements des int tires aleatoirement entre 0 et bound.
    n - taille de la matrice
    bound - nombre de lien maximal entre de noeuds
    null_diag - booleen, quand evalue a vrai, la matrice rendu par la fonction aura une diagonal nulle
    """
    if null_diag:
        return [[randint(0, bound) if i != j else 0 for i in range(n)] for j in range(n)]
    return [random_int_list(n, bound) for i in range(n)]

def random_symetric_int_matrix(n: int , bound:int, null_diag=True) -> List[List[int]]:
    """
    genere une matrice n x n avec ses elements des int tires aleatoirement entre 0 et bound.
    n - taille de la matrice
    bound - nombre de lien maximal entre de noeuds
    null_diag - booleen, quand evalue a vrai, la matrice rendu par la fonction aura une diagonal nulle
    return - matrice symetric => (A[i][j] == A[j][i]) pour tout i,j dans [0, n]
    """
    ma = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(i):
            ma[j][i] = ma[i][j]
    return ma

def random_oriented_int_matrix(n:int, bound:int, null_diag=True) -> List[List[int]]:
    """
    genere une matrice n x n avec ses elements des int tires aleatoirement entre 0 et bound.
    n - taille de la matrice
    bound - nombre de lien maximal entre de noeuds
    null_diag - booleen, quand evalue a vrai, la matrice rendu par la fonction aura une diagonal nulle
    return - matrice representant un graphe oriente =>
                pour tout i,j dans [0,n] : A[i][j] != 0 => A[j][i] == 0

    """
    ma = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(i):
            coin_flip = randint(0, 1)
            if coin_flip:
                ma[i][j] = 0
            else:
                ma[j][i] = 0
    return ma

def random_triangular_int_matrix(n:int, bound:int, null_diag=True) -> List[List[int]]:
    """
    genere une matrice n x n avec ses elements des int tires aleatoirement entre 0 et bound.
    n - taille de la matrice
    bound - nombre de lien maximal entre de noeuds
    null_diag - booleen, quand evalue a vrai, la matrice rendu par la fonction aura une diagonal nulle
    return - matrice representant un DAG (graphe dirige acyclique) =>
            impossible de parcourir l'intégralité du graphique à partir d'un bord. Les bords du graphe orienté ne vont que dans un sens.

    """
    ma = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(i):
            ma[i][j] = 0
    return ma


def random_matrix(n:int , bound: int , null_diag=False, symetric=False, oriented=False, DAG=False) -> List[List[int]]:
    """
    genere une matrice n x n avec ses elements des int tires aleatoirement entre 0 et bound.
    n - taille de la matrice
    bound - nombre de lien maximal entre de noeuds
    null_diag - booleen, quand evalue a vrai, la matrice rendu par la fonction aura une diagonal nulle
    symetric - booleen, quand evalue a vrai, la matrice rendu est symetric (A[i][j] == A[j][i])
    oriented - booleeN, quand evalue a vrai, la matrice rendu represente un graphe oriente =>
                pour tout i,j dans [0,n] : A[i][j] != 0 => A[j][i] == 0
    DAG - booleen, quand evalue a vrai, la matrice rendu represente un graphe dirige acyclique =>
            impossible de parcourir l'intégralité du graphique à partir d'un bord. Les bords du graphe orienté ne vont que dans un sens.
    """
    if DAG or oriented:
        if symetric:
            if null_diag:
                return random_int_matrix(n, 0)
            return [[0 if i != j else randint(0, bound) for i in range(n)] for j in range(n)]
        else:
            if DAG:
                return random_triangular_int_matrix(n, bound, null_diag)
            else:
                return random_oriented_int_matrix(n, bound, null_diag)
    if symetric:
        return random_symetric_int_matrix(n, bound, null_diag)
    return random_int_matrix(n, bound, null_diag)

class open_digraph_matrice_traduction_mx :
    @classmethod
    def graph_from_adjancency_matrix(cls, matrice: List[List[int]]) -> 'open_digraph':
        """
        renvoie un multigraphe a partir d'une matrice. 
        On laissera les attributs inputs et outputs du graphe vides.
        """
        n = len(matrice)
        list_of_nodes = [node(i, '', {},{}) for i in range(n)]
        graph = cls([], [], list_of_nodes)
        for i in range(n):
            for j in range(n):
                i_j = matrice[i][j]
                for _ in range(i_j):
                    graph.add_edge(i, j)
        return graph

    def associate_newId(self) -> Dict[int, int]:
        """
        prend en parametre un graph a n noeud
        et renvoi un dictionaire associant a chaque id de noeud un unique
        entier 0 ≤ i < n
        exemple  : {id_node : unique entier entre 0 et n-1}
        """
        nodes = self.get_nodes_ids()
        dictionnary = {}
        for i, id in enumerate(nodes):
            dictionnary[id] = i
        return dictionnary

    def adjacency_matrix(self) -> List[List[int]]:
        """
        traduit le graph en une matrice d'adjacence
        """
        id_index = self.associate_newId()
        size = len(id_index)
        matrice = [[0]*size for _ in range(size)]
        for id, i in id_index.items():
            nod :node = self.get_node_by_id(id)
            children = nod.get_children_ids()
            for id_child,mul in children.items():
                index_child = id_index[id_child]
                matrice[i][index_child] = mul
        return matrice
    
    @classmethod
    def random(cls, n:int, bound:int, inputs : int=0, outputs : int=0, form : str="free") -> 'open_digraph_matrice_traduction_mx':
        """cree un graphe de maniere aleatoire en suivant certains critere donnes

        Args:
            n (int): le nombre de noeuds dans le graphe
            bound (int): le nombre d'arrete maximal entre deux points
            inputs (int, optional): nombre d'input. Defaults to 0.
            outputs (int, optional): nombre d'output. Defaults to 0.
            form (str, optional): 
                permet de personnaliser le graphe :
                    - 'DAG' pour creer un graphe dirige acyclique.
                    - 'DAG loop-free' pour creer un DAG sans que les noeuds du graphe puissent se lier a eux meme.
                    - 'oriented' pour creer un graphe oriente.
                    - 'oriented loop-free' pour creer un graphe oriente sans que ses noeuds puissent se lier a eux meme.
                    - 'undirected' pour creer un graphe non oriente.
                    - 'undirected loop-free' pour creer un graphe non oriente sans que ses noeuds puissent se lier a eux meme.
                    - 'loop-free' pour creer un graphe sans que ses noeuds puissent se lier a eux meme.
                    - 'free' pour creer un graphe quelquonque. 
                    Defaults to "free".

        Raises:
            Exception: si le choix entree dans form ne fait pas partie des choix propose

        Returns:
            open_digraph: le graphe cree
        """
        if form == "DAG":
            mat = random_triangular_int_matrix(n, bound, False)
        elif form == "DAG loop-free":
            mat = random_triangular_int_matrix(n, bound, True)
        elif form == "oriented":
            mat = random_oriented_int_matrix(n, bound, False)
        elif form == "oriented loop-free":
            mat = random_oriented_int_matrix(n, bound, True)
        elif form == "undirected":
            mat = random_symetric_int_matrix(n, bound, False)
        elif form == "undirected loop-free":
            mat = random_symetric_int_matrix(n, bound, True)
        elif form == "loop-free":
            mat = random_int_matrix(n, bound, True)
        elif form == "free":
            mat = random_int_matrix(n, bound, False)
        else:
            raise Exception("cette forme n'existe pas.")
        graph = cls.graph_from_adjancency_matrix(mat)
        for _ in range(inputs):
            id = randint(0, n)
            graph.add_input_node(id)
        for _ in range(outputs):
            id = randint(0, n)
            graph.add_output_node(id)
        return graph
        
            
        