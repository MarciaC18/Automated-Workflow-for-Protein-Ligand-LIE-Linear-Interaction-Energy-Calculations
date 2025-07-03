import os
import shutil
import re

LIGAND_BASE = "ligands"
COMPLEX_BASE = "complex"
CHECK_ERRORS_DIR = "check_errors"
CHECK_LIGAND_DIR = os.path.join(CHECK_ERRORS_DIR, LIGAND_BASE)
CHECK_COMPLEX_DIR = os.path.join(CHECK_ERRORS_DIR, COMPLEX_BASE)

def get_ligand_numbers():
    ligand_nums = []
    if not os.path.isdir(LIGAND_BASE):
        raise FileNotFoundError(f"No se encontró la carpeta: {LIGAND_BASE}")
    for file in os.listdir(LIGAND_BASE):
        match = re.match(r"production_(\d+)(-2)?\.inp", file)
        if match:
            ligand_nums.append(int(match.group(1)))
    return sorted(set(ligand_nums))

def copy_production_scripts():
    os.makedirs(CHECK_LIGAND_DIR, exist_ok=True)
    os.makedirs(CHECK_COMPLEX_DIR, exist_ok=True)
    for src, dst in [
        (os.path.join(LIGAND_BASE, "production.sh"), os.path.join(CHECK_LIGAND_DIR, "production_ligands.sh")),
        (os.path.join(COMPLEX_BASE, "production.sh"), os.path.join(CHECK_COMPLEX_DIR, "production_complex.sh"))
    ]:
        if os.path.isfile(src):
            shutil.copy(src, dst)

def replace_steps(content):
    return re.sub(r"(steps\s+)(\d+|a\s+\d+)", r"\1                      40000 ! for total 40ps", content)

def adjust_ligand_content(content, i, is_minus_2=False):
    if not is_minus_2:
        # Ajustes para production_#.inp
        content = content.replace("prod1_nut2.re", f"prod1_{i}.re")
        content = content.replace("prod1_nut2.dcd", f"prod1_{i}.dcd")
        content = content.replace("prod1_nut2.en", f"prod1_{i}.en")

        content = content.replace(
            "topology                                     2_w.top",
            f"topology                                     ../../{LIGAND_BASE}/{i}_w.top")
        content = content.replace(
            "restart                                       eq3.re",
            f"restart                                       ../../{LIGAND_BASE}/eq{i}_3.re")
        content = content.replace(
            "fep                                          lig.fep",
            f"fep                                          ../../{LIGAND_BASE}/{i}.fep")

        content = replace_steps(content)
    else:
        # Ajustes para production_#-2.inp (Reemplazo especial [files] bloque)
        # Primero los nombres de archivos 'prod2' en vez de 'prod1'
        content = content.replace("prod1_nut2.re", f"prod2_{i}.re")
        content = content.replace("prod1_nut2.dcd", f"prod2_{i}.dcd")
        content = content.replace("prod1_nut2.en", f"prod2_{i}.en")

        # Reemplazo estándar (igual que antes) para estas líneas
        content = content.replace(
            "topology                                     2_w.top",
            f"topology                                     ../../{LIGAND_BASE}/{i}_w.top")
        content = content.replace(
            "restart                                       eq3.re",
            f"restart                                       ../../{LIGAND_BASE}/eq{i}_3.re")
        content = content.replace(
            "fep                                          lig.fep",
            f"fep                                          ../../{LIGAND_BASE}/{i}.fep")

        # Reemplazo del bloque [files] completo con el formato especial para production_#-2.inp:
        # Vamos a usar una expresión regular para reemplazar todo el bloque [files] con el bloque correcto

        files_block_pattern = r"(\[files\](?:\n.+?)+)(?:\n\n|$)"  # Captura el bloque [files]
        
        # Construimos el nuevo bloque [files] con el índice i:
        new_files_block = (
            f"[files]\n"
            f"topology                                     ../../{LIGAND_BASE}/{i}_w.top\n"
            f"restart                                       ../../{LIGAND_BASE}/eq{i}_3.re\n"
            f"final                                   prod2_{i}.re\n"
            f"fep                                          ../../{LIGAND_BASE}/{i}.fep\n"
            f"trajectory                             prod2_{i}.dcd\n"
            f"energy                                  prod2_{i}.en\n"
        )
        # Reemplazamos el bloque completo [files]
        content = re.sub(files_block_pattern, new_files_block + "\n", content, flags=re.MULTILINE)

        content = replace_steps(content)

    return content

def generate_ligand_inp_files(ligand_nums):
    template_path = os.path.join(LIGAND_BASE, "production.inp")
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"No se encontró: {template_path}")
    with open(template_path, "r") as f:
        template = f.read()

    os.makedirs(CHECK_LIGAND_DIR, exist_ok=True)

    for i in ligand_nums:
        out_path = os.path.join(CHECK_LIGAND_DIR, f"production_{i}.inp")
        with open(out_path, "w") as f:
            f.write(adjust_ligand_content(template, i, is_minus_2=False))

        alt_file = os.path.join(LIGAND_BASE, f"production_{i}-2.inp")
        if os.path.isfile(alt_file):
            with open(alt_file, "r") as f:
                alt_content = f.read()
            alt_out_path = os.path.join(CHECK_LIGAND_DIR, f"production_{i}-2.inp")
            with open(alt_out_path, "w") as f:
                f.write(adjust_ligand_content(alt_content, i, is_minus_2=True))

def adjust_complex_content(content, i):
    replacements = {
        "complexdiz_w.top": f"../../{COMPLEX_BASE}/complex_{i}_w.top",
        "eqdiz3.re": f"../../{COMPLEX_BASE}/eq3_{i}.re",
        "prod1_complexdiz.re": f"prod1_complex_{i}.re",
        "prod2_complexdiz.re": f"prod2_complex_{i}.re",
        "diz.fep": f"../../{COMPLEX_BASE}/{i}.fep",
        "prod1_complexdiz.dcd": f"prod1_complex_{i}.dcd",
        "prod2_complexdiz.dcd": f"prod2_complex_{i}.dcd",
        "prod1_complexdiz.en": f"prod1_complex_{i}.en",
        "prod2_complexdiz.en": f"prod2_complex_{i}.en",
    }
    for old, new in replacements.items():
        content = content.replace(old, new)

    content = replace_steps(content)
    return content

def generate_complex_inp_files(ligand_nums):
    prod1_template_path = os.path.join(COMPLEX_BASE, "production.inp")
    prod2_template_path = os.path.join(COMPLEX_BASE, "production2.inp")
    if not os.path.isfile(prod1_template_path) or not os.path.isfile(prod2_template_path):
        raise FileNotFoundError("No se encontraron los templates de producción en 2.complex.")

    with open(prod1_template_path, "r") as f:
        prod1_template = f.read()
    with open(prod2_template_path, "r") as f:
        prod2_template = f.read()

    os.makedirs(CHECK_COMPLEX_DIR, exist_ok=True)

    for i in ligand_nums:
        out_path1 = os.path.join(CHECK_COMPLEX_DIR, f"production1_{i}.inp")
        out_path2 = os.path.join(CHECK_COMPLEX_DIR, f"production2_{i}.inp")
        with open(out_path1, "w") as f:
            f.write(adjust_complex_content(prod1_template, i))
        with open(out_path2, "w") as f:
            f.write(adjust_complex_content(prod2_template, i))

def main():
    ligand_nums = get_ligand_numbers()
    generate_ligand_inp_files(ligand_nums)
    generate_complex_inp_files(ligand_nums)
    copy_production_scripts()

if __name__ == "__main__":
    main()
