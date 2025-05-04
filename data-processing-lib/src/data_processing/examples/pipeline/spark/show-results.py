import pyarrow.parquet as pq
import pandas as pd
import os

input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "input"))
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "output"))

input_file= input_dir + "/sample1.parquet"
parquet_input_file = pq.ParquetFile(input_file)
print(f"INPUT FILE has {parquet_input_file.metadata.num_rows} rows")
# Load the Parquet file
df = pd.read_parquet(input_file)
print(df)

# Print the schema (column names and data types)
print(f"---> INPUT FILE has \n{df.dtypes}")
print("\n-------------------------------------")
output_file= output_dir + "/sample1_0.parquet"
parquet_input_file = pq.ParquetFile(output_file)
print(f"----> OUTPUT FILE 1 has {parquet_input_file.metadata.num_rows} rows")
# Load the Parquet file
df = pd.read_parquet(output_file)

# Print the schema (column names and data types)
print(df)
print(f"schema: \n{df.dtypes}")

print("\n-------------------------------------")
output_file= output_dir + "/sample1_1.parquet"
parquet_input_file = pq.ParquetFile(output_file)
print(f"----> OUTPUT FILE 2 has {parquet_input_file.metadata.num_rows} rows")
# Load the Parquet file
df = pd.read_parquet(output_file)




# Print the schema (column names and data types)
print(df)
print(f"schema: \n{df.dtypes}")
