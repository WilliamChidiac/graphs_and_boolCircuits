from os import path as os_path
from sys import path as sys_path
root = os_path.normpath(os_path.join(__file__, './../..'))
sys_path.append(root)# allows us to fetch files from the project root
from typing import List, Dict, Tuple
from modules.graph.open_digraph import *
from modules.circuit.circuit_mixins.famille.adders import *
from modules.circuit.circuit_mixins.reecriture.reecriture_feuille import *
from modules.circuit.circuit_mixins.reecriture.reecriture_noeud import *
from modules.circuit.circuit_mixins.famille.hammig import *