from tulip import tlp
from indent_svg import pretty_print_svg
from layer_svg import push_white_groups_to_end

class TulipExporter:
    def __init__(self, output):             
        tlp.initTulipLib()
        tlp.loadPlugins()  
              
        self._output = output
        
    def _export_graph(self, graph):
        self.export_svg(graph, self._output)
        #pretty_print_svg(self._output, self._output)
        push_white_groups_to_end(self._output, self._output)
        
    def export_svg(self, graph, name):
        params = tlp.getDefaultPluginParameters("SVG Export", graph)
        params['edge color interpolation'] = False
        params['edge size interpolation'] = False
        params['edge extremities'] = True
        params['no background'] = False
        params['makes SVG output human readable'] = False
        params['export edge labels'] = True
        params['export metanode labels'] = True
        tlp.exportGraph("SVG Export", graph, name, params)