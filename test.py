import pandas as pd

# Define the file path
file_path = 'ulta-salons.csv'

df = pd.read_csv(file_path)
print("Columns in the CSV file:", df.columns)
df_cleaned = df.drop_duplicates(subset='location ID', keep='last')

df_cleaned.to_csv('ulta-salons-cleaned.csv', index=False)

print("Duplicates removed and cleaned data saved to 'ulta-salons-cleaned.csv'.")