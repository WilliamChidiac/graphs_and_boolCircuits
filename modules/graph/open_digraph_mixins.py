import os
import sys
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
from typing import List, Dict, Tuple
from modules.node.node import *
from modules.graph.graphs_mixins.matrix_traduction import *
from modules.graph.graphs_mixins.saving import *
from modules.graph.graphs_mixins.composition_decomposition import *
from modules.graph.graphs_mixins.distance import *
from modules.graph.graphs_mixins.profondeur import *