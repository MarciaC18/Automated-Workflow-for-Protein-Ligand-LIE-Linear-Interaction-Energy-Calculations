import os
import numpy as np

def extract_qsurr_energies(filename):
    """
    Extracts electrostatic and van der Waals (vdW) Q-surr. energies from a log file.

    Parameters:
        filename (str): Path to the .log file.

    Returns:
        tuple: Two numpy arrays containing electrostatic energies and vdW energies.
    """
    vdws = []
    elecs = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("Q-surr."):
                parts = line.split()
                if len(parts) >= 5:
                    elecs.append(float(parts[3]))
                    vdws.append(float(parts[4]))
    return np.array(elecs), np.array(vdws)

def compute_error_bind_separate(elecs, vdws):
    """
    Computes the error in binding energies separately for electrostatics and vdW.

    The error is half the absolute difference of the mean energies between
    two halves of the trajectory.

    Parameters:
        elecs (np.array): Electrostatic energies.
        vdws (np.array): vdW energies.

    Returns:
        tuple: error_vdw, error_el (both floats)
    """
    half = len(elecs) // 2
    el_b = np.mean(elecs[:half])
    el_f = np.mean(elecs[half:])
    vdW_b = np.mean(vdws[:half])
    vdW_f = np.mean(vdws[half:])
    error_vdw = abs(vdW_f - vdW_b) / 2
    error_el = abs(el_f - el_b) / 2
    return error_vdw, error_el

def main():
    """
    Main function that searches through production log files for each ligand,
    calculates the errors in electrostatic and vdW energies, and writes
    a report listing files where the error exceeds 1 kcal/mol.

    The report suggests extending the MD simulation until the error is below 1.
    """
    ligand_numbers = range(1, 39)  # Adjust based on your ligands count
    log_files = []

    # Adjust these paths to match your directory structure
    for ligand in ligand_numbers:
        path1 = os.path.join("complex", f"complex_{ligand}", "1", f"production1_{ligand}.log")
        path2 = os.path.join("complex", f"complex_{ligand}", "2", f"production2_{ligand}.log")
        if os.path.isfile(path1):
            log_files.append(path1)
        if os.path.isfile(path2):
            log_files.append(path2)

    if not log_files:
        print("No .log files found to process.")
        return

    high_errors = []

    for log_file in log_files:
        elecs, vdws = extract_qsurr_energies(log_file)
        if len(elecs) == 0 or len(vdws) == 0:
            print(f"{log_file}: No Q-surr. energies found.")
            continue

        error_vdw, error_el = compute_error_bind_separate(elecs, vdws)

        if error_vdw > 1.0:
            high_errors.append(
                (log_file, "vdW", error_vdw)
            )
        if error_el > 1.0:
            high_errors.append(
                (log_file, "Electrostatic", error_el)
            )

    if not high_errors:
        print("No errors greater than 1.0 kcal/mol found in the analyzed simulations.")
        return

    # Create output folder if it doesn't exist
    output_dir = "individual_plots"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "high_errors_report.txt")
    with open(output_file, "w") as f:
        f.write("Production log files with errors greater than 1 kcal/mol\n")
        f.write("-------------------------------------------------------\n\n")
        for filename, error_type, value in high_errors:
            msg = (f"File: {filename}\n"
                   f"Error type: {error_type} = {value:.2f} kcal/mol\n"
                   "Recommendation: Extend the MD simulation until the error is below 1 kcal/mol.\n\n")
            print(msg)
            f.write(msg)

if __name__ == "__main__":
    main()

