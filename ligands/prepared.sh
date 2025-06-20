#!/bin/bash

for i in {1..38}; do
    echo "Procesando ligando $i..."
    Qprep6 < generate_${i}.inp > generate${i}.log
done

