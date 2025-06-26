import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('Data_RP_LIE.csv')  # adjust sep= and decimal= if needed

# Rename columns if necessary (your file already has these column names)
# Just for safety if you want to unify names:
df.rename(columns={'DG_calculated': 'DG_calc', 'DG_experimental': 'DG_exp'}, inplace=True)

# Convert to numeric, coercing errors if any missing or wrong data
df['DG_calc'] = pd.to_numeric(df['DG_calc'], errors='coerce')
df['DG_exp'] = pd.to_numeric(df['DG_exp'], errors='coerce')

# Drop rows with missing experimental or calculated values
df = df.dropna(subset=['DG_calc', 'DG_exp'])

# Compute absolute error between predicted and experimental
df['abs_error'] = abs(df['DG_calc'] - df['DG_exp'])

# Prepare x values for ideal correlation line (y = x)
x_vals = np.linspace(df['DG_exp'].min(), df['DG_exp'].max(), 100)

# Get unique poses and assign colors
poses = sorted(df['Pose'].unique())
palette = sns.color_palette('tab10', n_colors=len(poses))
pose_colors = dict(zip(poses, palette))

# Calculate mean absolute error per pose
error_por_pose = df.groupby('Pose')['abs_error'].mean()

# Highlight pose with lowest mean error
highlight_pose = error_por_pose.idxmin()

plt.figure(figsize=(8, 6), dpi=300)  # High-res figure

# Scatter plot colored by pose
scatter = sns.scatterplot(data=df, x='DG_exp', y='DG_calc', hue='Pose', palette=pose_colors, s=60, edgecolor='black')

# Plot ideal correlation line
ideal_line, = plt.plot(x_vals, x_vals, 'k--', label='Ideal correlation (y = x)')

# Add error bands per pose
for pose in poses:
    mean_error = error_por_pose.loc[pose]
    y_lower = x_vals - mean_error
    y_upper = x_vals + mean_error
    alpha_val = 0.4 if pose == highlight_pose else 0.15
    plt.fill_between(x_vals, y_lower, y_upper, color=pose_colors[pose], alpha=alpha_val)

# Custom legend labels including mean error
custom_labels = [f"Pose {pose} (Error: {error_por_pose.loc[pose]:.2f})" for pose in poses]

# Get legend handles and labels from scatter
handles, labels = scatter.get_legend_handles_labels()

# Remove default "Pose" legend title added by seaborn
if 'Pose' in labels:
    pose_index = labels.index('Pose')
    handles.pop(pose_index)
    labels.pop(pose_index)

# Combine ideal line + pose legend handles
all_handles = [ideal_line] + handles
all_labels = ['Ideal correlation (y = x)'] + custom_labels

plt.legend(all_handles, all_labels, title='Legend', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.xlabel('Experimental ΔG (kcal/mol)', fontsize=12)
plt.ylabel('Predicted ΔG (kcal/mol)', fontsize=12)
plt.title('Predicted vs Experimental ΔG by Pose\nError Bands & Mean Errors in Legend', fontsize=14)

plt.tight_layout()

# Save figure as high-res PNG
plt.savefig('DG_calc_vs_exp_by_pose.png', dpi=300, bbox_inches='tight')

plt.show()
