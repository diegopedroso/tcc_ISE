import os
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_impact_ise(file_path, output_folder="charts"):
    """
    Analyzes the relationship between ROA and ROE before and after ISE entry for each company
    and saves the comparison charts to a specified folder.
    """
    try:
        df = pd.read_csv(file_path, sep=";")

        for col in ['ROE', 'ROA']:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False).astype(float)

        os.makedirs(output_folder, exist_ok=True)

        grouped = df.groupby('company_id')

        for company_id, data in grouped:
            print(f"\n==== Analysis for Company: {company_id} ====")

            ise_year = data['ise_entry'].iloc[0]
            before_ise = data[data['year'] < ise_year]
            after_ise = data[data['year'] >= ise_year]

            if before_ise.empty or after_ise.empty:
                print(f"Not enough data for before/after comparison for {company_id}.")
                continue

            X_before = sm.add_constant(before_ise['ROA'])
            y_before = before_ise['ROE']
            model_before = sm.OLS(y_before, X_before).fit()

            X_after = sm.add_constant(after_ise['ROA'])
            y_after = after_ise['ROE']
            model_after = sm.OLS(y_after, X_after).fit()

            print("\n--- Before ISE Entry ---")
            print(model_before.summary())

            print("\n--- After ISE Entry ---")
            print(model_after.summary())

            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            sns.regplot(x=before_ise['ROA'], y=before_ise['ROE'], ax=axes[0], line_kws={"color": "red"})
            axes[0].set_title(f"{company_id} - Before ISE (entry {ise_year})")
            axes[0].set_xlabel("ROA")
            axes[0].set_ylabel("ROE")

            sns.regplot(x=after_ise['ROA'], y=after_ise['ROE'], ax=axes[1], line_kws={"color": "blue"})
            axes[1].set_title(f"{company_id} - After ISE (entry {ise_year})")
            axes[1].set_xlabel("ROA")
            axes[1].set_ylabel("ROE")

            plt.suptitle(f"ROA vs ROE for {company_id}", fontsize=16)
            plt.tight_layout()

            filename = os.path.join(output_folder, f"{company_id.replace(' ', '_')}_ROA_ROE_ISE.png")
            plt.savefig(filename)
            plt.close()

            print(f"Chart saved to {filename}")

        # ========== GENERAL ANALYSIS ==========

        print("\n==== General analysis with all companies ====")

        df['period'] = df.apply(lambda row: 'Before ISE' if row['year'] < row['ise_entry'] else 'After ISE', axis=1)

        plt.figure(figsize=(10, 7))

        sns.scatterplot(data=df, x='ROA', y='ROE', hue='period', palette={'Before ISE': 'red', 'After ISE': 'blue'})

        sns.regplot(data=df[df['period'] == 'Before ISE'], x='ROA', y='ROE', scatter=False, label='Regression Before ISE', color='red')
        sns.regplot(data=df[df['period'] == 'After ISE'], x='ROA', y='ROE', scatter=False, label='Regression After ISE', color='blue')

        plt.title("ROA vs ROE - All Companies (Before and After ISE Entry)", fontsize=16)
        plt.xlabel("ROA")
        plt.ylabel("ROE")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        general_chart_path = os.path.join(output_folder, "All_Companies_ROA_ROE_ISE.png")
        plt.savefig(general_chart_path)
        plt.close()

        print(f"General chart saved to {general_chart_path}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_impact_ise("data.csv")
