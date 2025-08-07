from tulip import tlp
from tulipviz.TulipImporter import TulipImporter
from tulipviz.TulipExporter import TulipExporter
from tulipviz.TulipStyler import TulipStyler
from tulipviz.utils import *

class TulipVisualization:
    def __init__(self, input, output):
        self._importer = TulipImporter(input)
        self._exporter = TulipExporter(output)
        self._styler = TulipStyler()
        self._graph = self._importer.graph
            
        tlp.initTulipLib()
        tlp.loadPlugins()  
        tlp.loadPlugin("GGVIS/tulipviz/plugins/package_group.py")
        tlp.loadPlugin("GGVIS/tulipviz/plugins/package_layout.py")
               
        # preprocess graph
        self._styler.style_graph(self._graph)
        
        # group graph
        algorithm = "Package Group"
        params = tlp.getDefaultPluginParameters(algorithm, self._graph)
        self._graph.applyAlgorithm(algorithm, params)
        
        # layout
        algorithm = "Package Layout"
        params = tlp.getDefaultPluginParameters(algorithm, self._graph)
        #params["algorithm"] = "sugiyama"
        self._graph.applyAlgorithm(algorithm, params)
        self._curve_edges(self._graph)
        self._edge_bundling(self._graph)
        
    def export(self, type="svg", no_fix=False):
        self._exporter._export_graph(self._graph, type, no_fix)
        
    def _edge_bundling(self, graph):
        algorithm = "Edge bundling"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)
        
    def _curve_edges(self, graph):
        algorithm = "Curve edges"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)    