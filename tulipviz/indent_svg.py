import xml.dom.minidom
import argparse

def pretty_print_svg(input_path, output_path):
    # Read the SVG file
    with open(input_path, 'r', encoding='utf-8') as file:
        svg_content = file.read()

    # Parse and pretty-print the SVG
    dom = xml.dom.minidom.parseString(svg_content)
    pretty_svg = dom.toprettyxml(indent="  ")

    # Remove empty lines added by toprettyxml
    pretty_svg = "\n".join([line for line in pretty_svg.splitlines() if line.strip()])

    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(pretty_svg)

    print(f"SVG has been pretty-printed and saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pretty-print an SVG file with proper indentation.")
    parser.add_argument("-i", "--input", type=str, help="Path to the input SVG file")
    parser.add_argument("-o", "--output", type=str, help="Path to the output SVG file")
    
    args = parser.parse_args()
    pretty_print_svg(args.input, args.output)
