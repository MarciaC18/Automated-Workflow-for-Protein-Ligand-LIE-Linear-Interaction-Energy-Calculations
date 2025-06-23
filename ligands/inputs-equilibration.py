import os

# Template contents for eq1, eq2, eq3
template_eq1 = """[MD]
steps                                         100 ! for total 40ps
random_seed                                       1
temperature                                     10
initial_temperature                             0.1
stepsize                                        1.0 ! 1ps
bath_coupling                                     1
separate_scaling                                 on
lrf                                              on

[cut-offs]
solute_solute                                    10
solvent_solvent                                  10
solute_solvent                                   10

[sphere]
shell_radius                                   20.0
shell_force                                    0.01 !Paper

[solvent]
polarisation                                     on
polarisation_force                             20.0 

[intervals]
non_bond                                         25
output                                           50

[files]
topology                                    {ligand}_w.top
final                                      eq{ligand}_1.re
fep                                         {ligand}.fep
"""

template_eq2 = """[MD]
steps                                         3900 ! for total 40ps
!random_seed                                       1
temperature                                     190
!initial_temperature                             0.1
stepsize                                        1.0 ! 1ps
bath_coupling                                    10
separate_scaling                                 on
lrf                                              on
shake_all_hydrogens                              on
!shake_solvent                                   on

[cut-offs]
solute_solute                                    10
solvent_solvent                                  10
solute_solvent                                   10
!q_atom                                           99

[sphere]
shell_radius                                   20.0
shell_force                                    0.01 !Papers

[solvent]
!radial_force                                    60.0
polarisation                                     on
polarisation_force                             20.0 

[intervals]
non_bond                                         25
output                                           50

[files]
topology                                    {ligand}_w.top
restart                                     eq{ligand}_1.re
final                                      eq{ligand}_2.re
fep                                         {ligand}.fep
"""

template_eq3 = """[MD]
steps                                        16000 ! for total 40ps
!random_seed                                       1
temperature                                     300
!initial_temperature                             0.1
stepsize                                        1.0 ! 1ps
bath_coupling                                    10
separate_scaling                                 on
lrf                                              on
shake_all_hydrogens                              on
!shake_solvent                                   on

[cut-offs]
solute_solute                                    10
solvent_solvent                                  10
solute_solvent                                   10
!q_atom                                           99

[sphere]
shell_radius                                   20.0
shell_force                                    0.01 !Papers

[solvent]
!radial_force                                    60.0
polarisation                                     on
polarisation_force                             20.0 

[intervals]
non_bond                                         25
output                                           50

[files]
topology                                    {ligand}_w.top
restart                                     eq{ligand}_2.re
final                                      eq{ligand}_3.re
fep                                         {ligand}.fep
"""

# Create 3 input files for each ligand from 1 to 38
for i in range(1, 39):
    ligand = str(i)
    with open(f"eq1_{ligand}.inp", "w") as f1:
        f1.write(template_eq1.format(ligand=ligand))
    with open(f"eq2_{ligand}.inp", "w") as f2:
        f2.write(template_eq2.format(ligand=ligand))
    with open(f"eq3_{ligand}.inp", "w") as f3:
        f3.write(template_eq3.format(ligand=ligand))

print("eq1_#.inp, eq2_#.inp, eq3_#.inp generated for ligands 1 to 38.")

