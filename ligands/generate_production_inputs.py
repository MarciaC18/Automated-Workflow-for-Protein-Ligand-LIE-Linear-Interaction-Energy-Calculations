import os

# Read the base production input
with open("production.inp", "r") as f:
    template = f.read()

# Generate production_#.inp for ligands 1 to 38
for i in range(1, 39):
    content = template

    # Replacements in [files]
    content = content.replace("topology                                     2_w.top",
                              f"topology                                     {i}_w.top")
    content = content.replace("restart                                       eq3.re",
                              f"restart                                       eq{i}_3.re")
    
    # Replace any line with 'prod1_nut2.re', 'prod1_nut2.dcd', or 'prod1_nut2.en'
    content = content.replace("prod1_nut2.re", f"prod1_{i}.re")
    content = content.replace("prod1_nut2.dcd", f"prod1_{i}.dcd")
    content = content.replace("prod1_nut2.en", f"prod1_{i}.en")

    # Replace lig.fep with i.fep
    content = content.replace("fep                                          lig.fep",
                              f"fep                                          {i}.fep")

    # Write new input file
    with open(f"production_{i}.inp", "w") as out:
        out.write(content)

    print(f"✅ production_{i}.inp written.")

