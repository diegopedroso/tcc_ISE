import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import linregress
import seaborn as sns

try:
    df = pd.read_csv('data.csv', sep=';')
except FileNotFoundError:
    print("Error: The file 'data.csv' was not found.")
    exit()

df['ROE'] = df['ROE'].str.replace(',', '.').astype(float)
df['ROA'] = df['ROA'].str.replace(',', '.').astype(float)

output_folder_combined = 'combined_indicator_vs_year_with_regression'
os.makedirs(output_folder_combined, exist_ok=True)

plt.figure(figsize=(12, 7))
sns.scatterplot(data=df, x='year', y='ROE', hue='company_id', alpha=0.6)

slope_all_roe, intercept_all_roe, r_value_all_roe, p_value_all_roe, std_err_all_roe = linregress(df['year'], df['ROE'])
line_all_roe = slope_all_roe * df['year'] + intercept_all_roe
plt.plot(df['year'], line_all_roe, color='black', linestyle='--', label=f'Overall ROE Trend\ny = {slope_all_roe:.2f}x + {intercept_all_roe:.2f}\nR² = {r_value_all_roe**2:.2f}')

plt.xlabel('Year')
plt.ylabel('Return on Equity (ROE)')
plt.title('All Companies - ROE Over Time with Overall Trend')
plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_folder_combined, 'all_companies_roe_vs_year_with_overall_regression.png'))
plt.close()

plt.figure(figsize=(12, 7))
sns.scatterplot(data=df, x='year', y='ROA', hue='company_id', alpha=0.6)

slope_all_roa, intercept_all_roa, r_value_all_roa, p_value_all_roa, std_err_all_roa = linregress(df['year'], df['ROA'])
line_all_roa = slope_all_roa * df['year'] + intercept_all_roa
plt.plot(df['year'], line_all_roa, color='black', linestyle='--', label=f'Overall ROA Trend\ny = {slope_all_roa:.2f}x + {intercept_all_roa:.2f}\nR² = {r_value_all_roa**2:.2f}')

plt.xlabel('Year')
plt.ylabel('Return on Assets (ROA)')
plt.title('All Companies - ROA Over Time with Overall Trend')
plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_folder_combined, 'all_companies_roa_vs_year_with_overall_regression.png'))
plt.close()

print(f"Combined indicator vs year charts with overall linear regression have been generated in the '{output_folder_combined}' folder.")