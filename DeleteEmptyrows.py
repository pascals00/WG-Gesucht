import pandas as pd

# Read the CSV file
df = pd.read_csv('WebCrawlerApp/data/output/ADsURLList.csv')

# Drop empty rows
df.dropna(inplace=True)

# Save the modified DataFrame back to the CSV file
df.to_csv('WebCrawlerApp/data/output/ADsURLList.csv', index=False)