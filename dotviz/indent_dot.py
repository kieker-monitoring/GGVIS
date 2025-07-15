import sys

def indent_dot(input_file, output_file=None):
    """
    Reads a .dot file, formats it with indentation, and writes to the output file.
    If no output file is specified, it overwrites the input file.
    """
    with open(input_file, "r") as f:
        dot_text = f.read()

    output = []
    indent = 0
    for line in dot_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("}"):
            indent -= 1
        output.append("    " * indent + stripped)
        if stripped.endswith("{"):
            indent += 1

    formatted = "\n".join(output)

    out_file = output_file if output_file else input_file
    with open(out_file, "w") as f:
        f.write(formatted)

    print(f"Indented DOT file written to: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python indent_dot.py <input.dot> [output.dot]")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) == 3 else None
    indent_dot(in_file, out_file)
