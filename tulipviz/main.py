import sys
from TulipVisualization import TulipVisualization

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python render_flat_graph.py <input.dot> <output.svg>")
        sys.exit(1)
    graph = TulipVisualization(sys.argv[1], sys.argv[2])
    