from tulip import tlp

class TulipStyler:
    def __init__(self):
        self._fontsize = 8
                   
    def style_graph(self, graph):       
        self._style_nodes(graph)
        self._style_edges(graph)
        
    def _style_nodes(self, graph):
        viewSize = graph.getProperty("viewSize")
        viewLabel = graph.getProperty("viewLabel")
        viewBorderWidth = graph.getProperty("viewBorderWidth")
        viewShape = graph.getProperty("viewShape")
        viewColor = graph.getProperty("viewColor")
        
        for node in graph.getNodes():
            viewSize[node] = tlp.Size((len(viewLabel[node])) * self._fontsize, 5 * self._fontsize, 0)
            viewBorderWidth[node] = 5.0
            viewShape[node] = tlp.NodeShape.Square
            if viewColor[node] != tlp.Color(255, 192, 255, 255):
                viewColor[node] = tlp.Color(255, 255, 255, 255)
       
    def _style_edges(self, graph):
        viewColor = graph.getProperty("viewColor")
        viewBorderWidth = graph.getProperty("viewBorderWidth")
            
        for edge in graph.getEdges():
            viewBorderWidth[edge] = 5.0
            viewColor[edge] = tlp.Color.Gray