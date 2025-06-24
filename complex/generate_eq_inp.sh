#!/bin/bash

for i in {1..38}; do
    # eq1.inp
    sed -e "s/complexdiz_w.top/complex_${i}_w.top/g" \
        -e "s/final\s\+eq1.re/final eq1_${i}.re/g" \
        -e "s/fep\s\+diz.fep/fep ${i}.fep/g" \
        eq1.inp > eq1_${i}.inp

    # eq2.inp
    sed -e "s/complexdiz_w.top/complex_${i}_w.top/g" \
        -e "s/restart\s\+eq1.re/restart eq1_${i}.re/g" \
        -e "s/final\s\+eqoxo2.re/final eq2_${i}.re/g" \
        -e "s/fep\s\+diz.fep/fep ${i}.fep/g" \
        eq2.inp > eq2_${i}.inp

    # eq3.inp
    sed -e "s/complexdiz_w.top/complex_${i}_w.top/g" \
        -e "s/restart\s\+eqoxo2.re/restart eq2_${i}.re/g" \
        -e "s/final\s\+eqdiz3.re/final eq3_${i}.re/g" \
        -e "s/fep\s\+diz.fep/fep ${i}.fep/g" \
        eq3.inp > eq3_${i}.inp
done

