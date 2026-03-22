import importlib.util
import sys
import types

# -----------------------------
# LOAD YOUR PYTHON FILE
# -----------------------------
def load_module(file_path):
    spec = importlib.util.spec_from_file_location("scene_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -----------------------------
# CONVERT LAYERS TO ARDUINO
# -----------------------------
def convert_layers_to_arduino(layers):
    lines = []

    for L in layers:
        m = L.motors
        p = L.pumps

        motion_name = L.motion.__name__

        line = "{" + f"{L.start}, {L.end}, {L.fade_in}, {L.fade_out}, "
        line += "{" + f"{m[0]}, {m[1]}, {m[2]}" + "}, "
        line += "{" + f"{p[0]}, {p[1]}, {p[2]}" + "}, "
        line += f"{motion_name}" + "}, "

        lines.append(line)

    return "\n".join(lines)


# -----------------------------
# MAIN
# -----------------------------
def main():
    if len(sys.argv) < 3:
        print("Usage: python auto_convert.py input.py output.txt")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    module = load_module(input_file)

    # Expect the script defines "layers"
    if not hasattr(module, "layers"):
        print("Error: No 'layers' variable found in input file.")
        return

    layers = module.layers

    # Convert to Arduino
    arduino_code = convert_layers_to_arduino(layers)

    # Write output
    with open(output_file, "w") as f:
        f.write(arduino_code)

    print(f"Converted {len(layers)} layers → {output_file}")


if __name__ == "__main__":
    main()

#Usage: python converter.py visualizer.py output.txt
