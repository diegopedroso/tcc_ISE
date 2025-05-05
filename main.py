import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import linregress

try:
    df = pd.read_csv('data.csv', sep=';')
except FileNotFoundError:
    print("Error: The file 'data.csv' was not found.")
    exit()

df['ROE'] = df['ROE'].str.replace(',', '.').astype(float)
df['ROA'] = df['ROA'].str.replace(',', '.').astype(float)

output_folder = 'indicator_vs_year_with_regression'
os.makedirs(output_folder, exist_ok=True)

for company in df['company_id'].unique():
    company_df = df[df['company_id'] == company].copy()
    ise_entry_year = company_df['ise_entry'].iloc[0] 

    company_folder = os.path.join(output_folder, company.replace(" ", "_"))
    os.makedirs(company_folder, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.scatter(company_df['year'], company_df['ROE'], label='ROE Data')
    plt.axvline(x=ise_entry_year, color='r', linestyle='--', label=f'ISE Entry: {ise_entry_year}')

    slope_roe_year, intercept_roe_year, r_value_roe_year, p_value_roe_year, std_err_roe_year = linregress(company_df['year'], company_df['ROE'])
    line_roe_year = slope_roe_year * company_df['year'] + intercept_roe_year
    plt.plot(company_df['year'], line_roe_year, color='blue', label=f'ROE Trend\ny = {slope_roe_year:.2f}x + {intercept_roe_year:.2f}\nR² = {r_value_roe_year**2:.2f}')

    plt.xlabel('Year')
    plt.ylabel('Return on Equity (ROE)')
    plt.title(f'{company} - ROE Over Time with Trend')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(company_folder, 'roe_vs_year_with_regression.png'))
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.scatter(company_df['year'], company_df['ROA'], label='ROA Data')
    plt.axvline(x=ise_entry_year, color='g', linestyle='--', label=f'ISE Entry: {ise_entry_year}')

    slope_roa_year, intercept_roa_year, r_value_roa_year, p_value_roa_year, std_err_roa_year = linregress(company_df['year'], company_df['ROA'])
    line_roa_year = slope_roa_year * company_df['year'] + intercept_roa_year
    plt.plot(company_df['year'], line_roa_year, color='orange', label=f'ROA Trend\ny = {slope_roa_year:.2f}x + {intercept_roa_year:.2f}\nR² = {r_value_roa_year**2:.2f}')

    plt.xlabel('Year')
    plt.ylabel('Return on Assets (ROA)')
    plt.title(f'{company} - ROA Over Time with Trend')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(company_folder, 'roa_vs_year_with_regression.png'))
    plt.close()

print(f"Indicator vs Year charts with linear regression have been generated in the '{output_folder}' folder.")