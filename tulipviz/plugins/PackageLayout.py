# This file was written as part of a research projet.
# https://arxiv.org/abs/2507.23425
# 
# Author: Daphné Larrivain

# This plugin performs a nested layout by arranging subgraph hierarchies within their respective bounding boxes.
# Applies a layout algorithm to all subgraphs from the bottom up and creates bounding boxes on the fly.
# This helps size their bounding boxes correctly.
# When laying out a graph, its direct nodes are handled normally.
# Subgraphs and their bounding boxes are abstracted as single nodes.

from tulip import tlp
import tulipplugins

class PackageLayout(tlp.Algorithm):
    def __init__(self, context):
        tlp.Algorithm.__init__(self, context)
        self.addStringCollectionParameter("algorithm",
                                          help='',
                                          defaultValue='fm3;sugiyama',
                                          isMandatory=False,
                                          inParam=True,
                                          outParam=False,
                                          valuesDescription='')
        self.addIntegerParameter("bounding box label size",
                                         help='',
                                         defaultValue='16',
                                         isMandatory=False,
                                         inParam=True,
                                         outParam=False,
                                         valuesDescription='')
        self.addColorParameter("bounding box color",
                               help='Choose a transparent color to see the nested bounding boxes',
                               defaultValue='(255, 0, 0, 15)',
                               isMandatory=True,
                               inParam=True,
                               outParam=False,
                               valuesDescription='')
      
        self._boxer = BoundingBoxManager()

    def check(self):
        return (True, "Ok")

    def run(self):
        self.graph.getBooleanProperty("isBoundingBox")
        self.graph.getStringProperty("bboxLabel")      
        self._boxer.set_color(self.dataSet["bounding box color"])       
        self.layout(self.graph, globals()[self.dataSet["algorithm"]])
        self._boxer.bbox_labels(self.graph, self.dataSet["bounding box label size"])
        return True
       
    def layout(self, graph, layout_func): 
        '''
        Applies a layout algorithm to all subgraphs from the bottom up.
        This helps size their bounding boxes correctly.
        When laying out a graph, its direct nodes are handled normally.
        Subgraphs and their bounding boxes are abstracted as single nodes.
        '''
        alt_layout = self.graph.getLayoutProperty("altLayout")
        view_layout = self.graph.getLayoutProperty("viewLayout")
            
        def _bottom_up(graph):
            subgraphs = graph.getSubGraphs()
            subgraph_list = []
            while subgraphs.hasNext():
                subgraph_list.append(subgraphs.next())

            for subgraph in subgraph_list:
                _bottom_up(subgraph)

            # lay out the graph
            layout_func(graph, alt_layout)
            fast_overlap_removal(graph, alt_layout)
            
            # update the direct node children
            direct_children = direct_nodes(graph)
            for n in direct_children:
                view_layout[n] = alt_layout[n]
                
            # translate all subgraphs to their bbox
            for s in subgraph_list:
                if self._boxer.has_bbox(s): 
                    box = self._boxer.get_bbox(s)
                    diff = alt_layout[box] - view_layout[box]
                    view_layout[box] = alt_layout[box]
                    for n in s.getNodes():
                        view_layout[n] += diff
                        
            # create bounding box   
            if graph.getSuperGraph() != graph:           
                self._boxer.create_bbox(graph) 
                
        _bottom_up(graph)

################################################################################
#### Standalone Funcs
################################################################################

def direct_nodes(graph):
    '''
    Returns the direct child nodes of a given graph.
    Excludes nodes that belong to its subgraphs and bounding boxes nodes.
    '''
    bbox = graph.getBooleanProperty("isBoundingBox")
    descendants = []
    for g in graph.getSubGraphs():
        descendants += list(g.getNodes())
    return [node for node in graph.getNodes() if node not in descendants and bbox[node] == False]

def fm3(graph, property):
    params = tlp.getDefaultPluginParameters('FM^3 (OGDF)', graph)
    params['new initial layout'] = False
    params['edge length measurement'] = "midpoint"
    params['allowed positions'] = "all"
    graph.applyLayoutAlgorithm('FM^3 (OGDF)', property, params)
        
def sugiyama(graph, property):
    params = tlp.getDefaultPluginParameters('Sugiyama (OGDF)', graph)
    graph.applyLayoutAlgorithm('Sugiyama (OGDF)', property, params)
    
def fast_overlap_removal(graph, property):
    params = tlp.getDefaultPluginParameters("Fast Overlap Removal", graph)
    params["initial layout"] = property
    params["x border"] = 10
    params["y border"] = 10
    graph.applyLayoutAlgorithm("Fast Overlap Removal", property, params)

################################################################################
##### Bounding Box Manager
################################################################################

class BoundingBoxManager:
    '''
    Helper class. Handles the bounding boxes manipulations.
    '''
    
    def __init__(self):
        self._boxes = {}
        self.color = tlp.Color(255, 0, 0, 15)
        
    def set_color(self, color):
        self.color = color
                   
    def has_bbox(self, graph):
        return graph in self._boxes.keys()
    
    def get_bbox(self, graph):
        return self._boxes[graph]
                      
    def create_bbox(self, subgraph):
        if subgraph is None:
            raise ValueError("Subgraph is None — cannot create bounding box.")
        parent_graph = subgraph.getSuperGraph()
        label_name = parent_graph.getProperty("bboxLabel")
        layout = parent_graph.getLayoutProperty('viewLayout')
        size = parent_graph.getSizeProperty('viewSize')
        color = parent_graph.getColorProperty('viewColor')
        shape = parent_graph.getIntegerProperty('viewShape')
        border_width = parent_graph.getProperty("viewBorderWidth")

        coords = self.compute_bbox(subgraph)

        box_node = parent_graph.addNode()
        
        layout[box_node] = tlp.Coord(coords["center_x"], coords["center_y"], 0)
        size[box_node] = tlp.Size(coords["width"], coords["height"], 1)
        border_width[box_node] = 5
        color[box_node] = self.color
        shape[box_node] = tlp.NodeShape.Square
        label_name[box_node] = subgraph.getName()
        
        self._boxes[subgraph] = box_node
        bbox = subgraph.getProperty("isBoundingBox") 
        bbox[box_node] = True
        
    def compute_bbox(self, subgraph):
        '''
        Determines the coordinates of the four bounding box corners to fully encapsulate the graph.
        '''
        if subgraph is None:
            raise ValueError("Subgraph is None — cannot compute bounding box.")

        layout = subgraph.getLayoutProperty('viewLayout')
        size = subgraph.getSizeProperty('viewSize')   

        # Compute bounding box of all nodes in the subgraph
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        for n in subgraph.getNodes():
            pos = layout[n]
            sz = size[n]
            x0 = pos[0] - sz[0] / 2
            x1 = pos[0] + sz[0] / 2
            y0 = pos[1] - sz[1] / 2
            y1 = pos[1] + sz[1] / 2
            min_x = min(min_x, x0)
            max_x = max(max_x, x1)
            min_y = min(min_y, y0)
            max_y = max(max_y, y1)

        # Add optional padding
        padding = 10.0
        min_x -= padding
        max_x += padding
        min_y -= padding
        max_y += padding * 4

        # Compute bounding box center and dimensions
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        width = max_x - min_x
        height = max_y - min_y
        
        # Return result
        res = {"center_x": center_x,
            "center_y": center_y,
            "width": width,
            "height": height}
        return res
    
    def bbox_labels(self, graph, fontsize):
        view = graph.getLayoutProperty("viewLayout")
        viewSize = graph.getProperty("viewSize")
        viewLabel = graph.getProperty("viewLabel")
        viewShape = graph.getProperty("viewShape")
        viewColor = graph.getProperty("viewColor")
        externLabel = graph.getProperty("bboxLabel")   
        bbox = graph.getProperty("isBoundingBox")      
                        
        for node in graph.getNodes():
            if bbox[node]:
                label_node = graph.addNode()

                viewSize[label_node] = tlp.Size((len(externLabel[node])) * fontsize, 5 * fontsize, 0)
                viewColor[label_node] = tlp.Color(0, 0, 0, 0)
                viewShape[label_node] = tlp.NodeShape.Square
                viewLabel[label_node] = externLabel[node]
                view[label_node] = view[node] + tlp.Coord(0, viewSize[node][1]/2 - 20, 0)
    
################################################################################

pluginDoc = """
Performs a nested layout by arranging subgraph hierarchies within their respective bounding boxes.
"""

# The line below does the magic to register the plugin into the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("PackageLayout",
                                   "Package Layout",
                                   "Daphné Larrivain",
                                   "07/08/2025",
                                   pluginDoc,
                                   "1.0",
                                   "Python")