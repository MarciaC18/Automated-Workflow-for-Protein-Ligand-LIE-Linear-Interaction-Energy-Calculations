template = """
rl {i}.lib
rl OPLS2005.lib

#Read the parameter 
rff OPLS2005_{i}_all.prm
#Read the starting, usually precleaned pdb file.
rp {i}.pdb

ls
lr 1
preferences

#you need to create the sulfur-sulfur bridges.
#addbond atomnum atomnum y

#Create water sphere
boundary sphere 1:C9 20
solvate 1:C9 20 1 HOH

mt {i}_w
wt {i}_w.top

#checkbonds 6
#checkangs  6
#checktors  6
#checkimps  6

wp {i}_w.pdb y
quit
"""

for i in range(1, 39):
    with open(f"generate_{i}.inp", "w") as f:
        f.write(template.format(i=i))

