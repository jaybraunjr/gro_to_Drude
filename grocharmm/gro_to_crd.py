import MDAnalysis as mda


def replace_resnames(input_file, output_file=None, replacements=None):
    
    if replacements is None:
        replacements = {
            'TRI': 'TRIO',
            'POP': 'POPC',
            'DOP': 'DOPE',
            'SWM': 'SWM4'
        }

    if output_file is None:
        output_file = input_file

    with open(input_file, 'r') as file:
        file_content = file.read()

    for old_value, new_value in replacements.items():
        file_content = file_content.replace(old_value, new_value)

    with open(output_file, 'w') as file:
        file.write(file_content)

    print(f"Replacements done! File saved to {output_file}")




def update_segment(input_path, output_path):
    """
    Replaces 'SYSTEM' segment name in CHARMM .crd files with correct segment based on residue name.
    Segment name is left-aligned and spacing is preserved elsewhere.
    """
    segment_rules = {
        'TIP3': 'TIP3',
        'SOD': 'IONS',
        'CLA': 'IONS',
        'DOPE': 'MEMB',
        'POPC': 'MEMB',
        'TRIO': 'MEMB',
    }

    def assign_segment(resname):
        return segment_rules.get(resname, 'PROA')

    with open(input_path, 'r') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if 'SYSTEM' not in line:
            updated_lines.append(line)
            continue

        resname = line[20:26].strip()
        new_segment = assign_segment(resname)

        updated_line = line.replace('SYSTEM', new_segment.ljust(6), 1)
        updated_lines.append(updated_line)

    with open(output_path, 'w') as f:
        f.writelines(updated_lines)




def update_segment_number(input_path, output_path):
    """
    Writes a segment-local residue counter to column 10 (char 113–128).
    - Resets to 1 when the segment changes
    - Increments when the left-side resid changes within a segment
    """

    current_segment = None
    current_resid = None
    counter = 0
    updated_lines = []

    with open(input_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("*") or "EXT" in line or not line.strip():
            updated_lines.append(line)
            continue

        segment = line[102:108].strip()
        resid = int(line[10:20].strip())

        if segment != current_segment:
            counter = 1
            current_segment = segment
            current_resid = resid

        elif resid != current_resid:
            counter += 1
            current_resid = resid

        updated_line = line[:112] + f"{counter:<16}" + line[128:]
        updated_lines.append(updated_line)

    with open(output_path, 'w') as f:
        f.writelines(updated_lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Update CHARMM .crd file segments and segment-local resid numbering.")
    parser.add_argument("input", help="Path to input .crd file")
    parser.add_argument("output", help="Path to final output .crd file")
    parser.add_argument("--replace", action="store_true", help="Apply resname replacements before segment updates")

    args = parser.parse_args()

    temp_file1 = args.input
    temp_file2 = args.output + ".step1"
    
    if args.replace:
        print("Running resname replacement...")
        replace_resnames(args.input, temp_file1)
    else:
        temp_file1 = args.input

    print("Running segment update...")
    update_segment(temp_file1, temp_file2)

    print("Running segment number update...")
    update_segment_number(temp_file2, args.output)

    print(f"Done! Final output saved at: {args.output}")
