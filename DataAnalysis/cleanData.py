import pandas as pd

# Read the CSV file
df = pd.read_csv('WebCrawlerApp/data/output/apartmentsBerlinData.csv')

# Filter out rows with an empty first column
df = df[df['apartmentID'].notna()]

# Save the cleaned data to a new CSV file
df.to_csv('WebCrawlerApp/data/output/apartmentsBerlinData.csv', index=False)

df_url_list = pd.read_csv('WebCrawlerApp/data/output/ADsURLList.csv')

# Remove duplicates from df_url_list
df_url_list = df_url_list.drop_duplicates()


