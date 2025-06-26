import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grocharmm.gro_to_psf import PSFeditor

# Step 1: Generate PSF from topol and crd
editor = PSFeditor("data/tld1_generated.psf")
editor.load_inp(
    topol_file="data/topol.top",
    crd_file="data/tld1_final.crd",
    output_psf="data/tld1_generated.psf"
)

# Step 2: Read, modify, write
editor.read_lines()
editor.update_psf_segments()
editor.update_psf_resids()
editor.write_lines("data/output.psf")

print("Final PSF saved to test/output.psf")
