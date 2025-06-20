import re

def extract_ligand_sections(prm_lines):
    """
    Extrae las secciones del ligando del archivo prm.
    Devuelve un dict con clave = nombre de sección y valor = lista de líneas.
    """
    sections = {
        'vdw': ('! Ligand vdW parameters', '! End ligand vdW parameters'),
        'bond': ('! Ligand bond parameters', '! End ligand bond parameters'),
        'angle': ('! Ligand angle parameters', '! End ligand angle parameters'),
        'torsion': ('! Ligand torsion parameters', '! End Ligand torsion parameters'),
        'improper': ('! Ligand improper parameters', '! End ligand improper parameters'),
    }
    
    extracted = {}
    
    for key, (start_marker, end_marker) in sections.items():
        start_idx = None
        end_idx = None
        for i, line in enumerate(prm_lines):
            if start_marker in line:
                start_idx = i
            if end_marker in line and start_idx is not None and i > start_idx:
                end_idx = i
                break
        if start_idx is not None and end_idx is not None:
            # Incluye línea de inicio y fin
            extracted[key] = prm_lines[start_idx:end_idx+1]
        else:
            print(f"Sección {key} no encontrada correctamente.")
            extracted[key] = []
    return extracted

def replace_ligand_sections(base_lines, ligand_sections):
    """
    Reemplaza las secciones de ligando en base_lines con ligand_sections.
    """
    sections = {
        'vdw': ('! Ligand vdW parameters', '! End ligand vdW parameters'),
        'bond': ('! Ligand bond parameters', '! End ligand bond parameters'),
        'angle': ('! Ligand angle parameters', '! End ligand angle parameters'),
        'torsion': ('! Ligand torsion parameters', '! End Ligand torsion parameters'),
        'improper': ('! Ligand improper parameters', '! End ligand improper parameters'),
    }
    
    # Para cada sección, buscar en base_lines y reemplazar
    new_lines = base_lines.copy()
    
    for key, (start_marker, end_marker) in sections.items():
        start_idx = None
        end_idx = None
        for i, line in enumerate(new_lines):
            if start_marker in line:
                start_idx = i
            if end_marker in line and start_idx is not None and i > start_idx:
                end_idx = i
                break
        if start_idx is not None and end_idx is not None:
            # Reemplaza el bloque completo (incluye inicio y fin)
            new_lines = new_lines[:start_idx] + ligand_sections.get(key, []) + new_lines[end_idx+1:]
        else:
            print(f"No se encontró la sección {key} para reemplazar en el archivo base.")
    
    return new_lines

def main():
    base_file = "OPLS2005_all.prm"
    for i in range(1, 39):
        ligand_file = f"{i}.prm"
        
        with open(base_file, 'r') as f:
            base_lines = f.readlines()
        
        with open(ligand_file, 'r') as f:
            ligand_lines = f.readlines()
        
        ligand_sections = extract_ligand_sections(ligand_lines)
        
        new_content = replace_ligand_sections(base_lines, ligand_sections)
        
        output_file = f"OPLS2005_{i}_all.prm"
        with open(output_file, 'w') as f:
            f.writelines(new_content)
        
        print(f"Archivo guardado: {output_file}")

if __name__ == "__main__":
    main()

