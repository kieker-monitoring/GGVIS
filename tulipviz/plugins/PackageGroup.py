# This file was written as part of a research projet.
# https://arxiv.org/abs/2507.23425
# 
# Author: Daphné Larrivain

from tulip import tlp
import tulipplugins

class PackageGroup(tlp.Algorithm):
    def __init__(self, context):
        tlp.Algorithm.__init__(self, context)
        self.addStringPropertyParameter("full component name",
                                        help='',
                                        defaultValue='viewLabel',
                                        isMandatory=False,
                                        inParam=True,
                                        outParam=False,
                                        valuesDescription='')   
        self.addStringParameter("separator",
                           help='',
                           defaultValue='.',
                           isMandatory=False,
                           inParam=True,
                           outParam=False,
                           valuesDescription='')

    def check(self):
        return (True, "Ok")

    def run(self):
        self.group_clusters(self.graph)
        self.relocate_edges(self.graph)
        return True

    def group_clusters(self, graph):
        _clusters = {}       
        label_prop = self.dataSet["full component name"]       
        for node in graph.getNodes():
            parts = label_prop[node].split(".")
            parent = graph
            for i in range(len(parts) - 1):
                curpart = ".".join(parts[:i+1])
                if curpart not in _clusters:
                    cluster = parent.addSubGraph(curpart)
                    _clusters[curpart] = cluster
                parent = _clusters[curpart]         
            node_key = ".".join(parts[:-1])
            target_cluster = _clusters.get(node_key, graph) 
            if target_cluster.getSuperGraph() != target_cluster:
                target_cluster.addNode(node)
                 
    def relocate_edges(self, graph):
        for edge in graph.getEdges():
            ancestor_name = self.get_common_prefix(graph, edge, self.dataSet["separator"])
            if ancestor_name != "":   
                ancestor = graph.getDescendantGraph(ancestor_name)
                ancestor.addEdge(edge)
           
    def longest_common_prefix(self, label1, label2, separator):
        """Returns the longest common dot-separated prefix between two labels."""
        parts1 = label1.split(separator)
        parts2 = label2.split(separator)
        common_parts = []
        for p1, p2 in zip(parts1, parts2):
            if p1 == p2:
                common_parts.append(p1)
            else:
                break
        return ".".join(common_parts)
    
    def get_common_prefix(self, graph, edge, separator):
        """Returns the longest common dot-separated prefix between source and target node labels."""
        label_prop = self.dataSet["full component name"]
        src = graph.source(edge)
        tgt = graph.target(edge)
        label1 = separator.join(label_prop[src].split(separator)[:-1])
        label2 = separator.join(label_prop[tgt].split(separator)[:-1])
        prefix = self.longest_common_prefix(label1, label2, separator)
        return prefix
  
################################################################################

pluginDoc = """
Converts a flat graph into a hierarchy of nested subgraphs by partitioning nodes based on delimited segments of their component names.
"""  
  
# The line below does the magic to register the plugin into the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("PackageGroup",
                                   "Package Group",
                                   "Daphné Larrivain",
                                   "07/08/2025",
                                   pluginDoc,
                                   "1.0",
                                   "Python")