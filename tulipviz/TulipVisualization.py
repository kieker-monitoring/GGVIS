from tulip import tlp
from tulipviz.TulipImporter import TulipImporter
from tulipviz.TulipExporter import TulipExporter
from tulipviz.TulipStyler import TulipStyler

class TulipVisualization:
    def __init__(self, input, output, algorithm, no_curves=False, no_bundle=False):
        self.no_curves = no_curves
        self.no_bundle = no_bundle
        self.algorithm = algorithm
        self._importer = TulipImporter(input)
        self._exporter = TulipExporter(output)
        self._styler = TulipStyler()
        self._graph = self._importer.graph
            
        tlp.initTulipLib()
        tlp.loadPlugins()  
        tlp.loadPlugin("GGVIS/tulipviz/plugins/PackageGroup.py")
        tlp.loadPlugin("GGVIS/tulipviz/plugins/PackageLayout.py")
               
        self._process_graph()    
        
    def export(self, type="svg", no_fix=False):
        self._exporter._export_graph(self._graph, type, no_fix)    
               
    def _process_graph(self):
        self._styler.style_graph(self._graph)
        self._package_group(self._graph) 
        self._package_layout(self._graph)  
        if not self.no_curves: 
            self._curve_edges(self._graph)
        if not self.no_bundle:
            self._edge_bundling(self._graph)
  
    def _package_group(self, graph):
        algorithm = "Package Group"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)
    
    def _package_layout(self, graph):
        algorithm = "Package Layout"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        params["algorithm"] = self.algorithm
        graph.applyAlgorithm(algorithm, params)  
  
    def _curve_edges(self, graph):
        algorithm = "Curve edges"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)    
        
    def _edge_bundling(self, graph):
        algorithm = "Edge bundling"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)  