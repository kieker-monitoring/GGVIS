# Grouped Graph Visualizer (GGVIS)

## Author

- Daphné Larrivain <daphne.larrivain@ecole.ensicaen.fr>

## About

This tool works alongside the Kieker [MVIS](https://github.com/kieker-monitoring/kieker/tree/main/tools/mvis/) tool.
It uses the [Tulip Framework](https://tulip.labri.fr/) to read `.dot` and `.graphml` files and renders nested graphs based on dot-separated component names, e.g., `urllib3.util.timeout.Timeout`.
Other Graphviz layout engines, such as `dot` and `fdp`, are available for comparison.
Run with `--help` to see available options.

## Generating Nested Graphs

### Algorithms

- **Algorithm 1**: Cluster Nodes to Hierarchical Subgraphs

```text
clusters ← empty dictionary

for each node in graph:
    segments ← split node name by "."
    parent ← main graph

    // Create missing parent subgraphs
    for each segment except last:
        clusterName ← join segments up to current

        if clusterName not in clusters then
            Create subgraph clusterName
            Add to parent
            clusters[clusterName] ← new subgraph
        end if

        parent ← clusters[clusterName]
    end for

    // Add node to current subgraph
    clusterKey ← join segments except last
    targetCluster ← clusters[clusterKey]
    Add node to targetCluster

end for
```

- **Algorithm 2**: Bounding Box Layout Strategy

```text
list ← List recursively from bottom up all subgraphs

for each graph in list:
    Apply layout algorithm and store result away
    
    for each direct node of graph:
        Update the old coordinates to the new ones
    end for

    for each bounding box node box:
        Update the old coordinates to the new ones
        diff ← new position - old position
        
        for each node inside box:
            Translate node position by diff
        end for
    end for

    Create bounding box node for graph
    Add it to its parent graph
end for
```

### Implementations

- **[Tulip](https://github.com/kieker-monitoring/GGVIS/tree/main/tulipviz)**
  - Algorithm 1: [PackageGroup.py](https://github.com/kieker-monitoring/GGVIS/blob/main/tulipviz/plugins/PackageGroup.py)
  - Algorithm 2: [PackageLayout.py](https://github.com/kieker-monitoring/GGVIS/blob/main/tulipviz/plugins/PackageLayout.py)

- **[Graphviz](https://github.com/kieker-monitoring/GGVIS/tree/main/dotviz)**:
  - Algorithm 1: [ClusterDotGraph.py](https://github.com/kieker-monitoring/GGVIS/blob/main/dotviz/ClusteredDotGraph.py)
  - Algorithm 2: _Not needed for Graphviz tools_
