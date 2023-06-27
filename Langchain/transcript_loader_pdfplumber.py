import pdfplumber
import pandas as pd
import itertools
# Load the PDF file
pdf = pdfplumber.open("/Users/arpit/Python/OpenAI/utilities/Langchain/transcript/Porter_UpToDate_Stroke CMEs_02.24-03.31.2022 (S3) (1).pdf")

# Extract the tables
tables = []
for page in pdf.pages:
    tables.extend(page.extract_tables())

# Convert the tables to a single DataFrame
df = pd.DataFrame.from_records(itertools.chain(*tables))


# Save the DataFrame to a CSV file
df.to_csv("Porter_UpToDate_Stroke CMEs_02.24-03.31.2022.csv", index=False)
