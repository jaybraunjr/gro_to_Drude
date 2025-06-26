## GRO to CHARMM File Editor (GUI)

A lightweight Python GUI for converting `.gro` files into CHARMM-compatible `.crd` and `.psf` formats. Useful for Drude and other CHARMM workflows.

### Requirements

- Python 3.10
- `parmed`
- `tkinter` (comes with Python on Windows)

Install dependencies with pip:

```bash
pip install parmed
```

If pip fails, try conda:

```bash
conda install -c conda-forge parmed
```

### Usage

To launch the GUI:

```bash
python scripts/gui_editor.py
```

### Features

- Convert `.gro` to `.crd` or `.psf`
- Optional residue renaming (CRD mode only)
- Automatic segment name and residue number updates

### Instructions

1. Launch the GUI
2. Select input and output file paths
3. Choose output mode (`CRD` or `PSF`)
4. Optionally enable "Replace resnames" (CRD only)
5. Click **Run**

The output file will be saved to your selected path.
