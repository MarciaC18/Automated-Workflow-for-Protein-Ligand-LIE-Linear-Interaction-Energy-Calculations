#!/bin/bash

for i in {1..38}; do
    echo "Processing ligand $i..."
    Qprep6 < generate_complex_${i}.inp > generate_complex_${i}.log
done

