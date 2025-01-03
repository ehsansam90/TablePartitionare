# Table Partitioning Library

![Library Workflow](flowchart.png "Workflow Diagram")

This library provides functionality for partitioning tables in a PostgreSQL database using SQLAlchemy. It allows users to:

- Read data from an existing table.
- Assign partitions to data based on a column (e.g., `patient_id`).
- Create partitioned tables in the database.
- Move data into partitioned tables.

## Requirements

The library automatically installs its dependencies when you install it. The following dependencies are included:

- `python-dotenv`: To load environment variables from a .env file.
- `psycopg2`: PostgreSQL adapter for Python.
- `SQLAlchemy`: ORM for Python to interact with PostgreSQL.

## Library Overview

The library provides an object-oriented approach for working with PostgreSQL tables, including:

- Reading from an existing table.
- Creating partitioned tables.
- Inserting data into partitioned tables.
- Partitioning data based on the values in a specified column.

The library uses MD5 hashing to assign rows to specific partitions.

## Key Features

- **Reading Data**: Load data from an existing table.
- **Assigning Partitions**: Use MD5 hashing to assign rows to partitions.
- **Creating Partitioned Tables**: Create partitioned tables in PostgreSQL.
- **Moving Data**: Transfer data from a source table to partitioned tables.

## Setting Up

### Environment Variables

To avoid hardcoding database credentials, the library uses environment variables stored in a .env file. This file should contain the following variables:

```bash
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=your_port
DB_NAME=your_database_name

How to Use the Library
1. Importing the Library
The library provides a TablePartitioner class to handle all operations:

python
Copy code
from partitioning_lib import TablePartitioner
2. Initialize the Partitioning Class
Create an instance of the TablePartitioner class by providing the path to the .env file and the number of partitions:

python
Copy code
num_partitions = 15  # Number of partitions you want to create
partitioner = TablePartitioner("path/to/.env", num_partitions)
3. Reading Data from an Existing Table
Use the read_table() method to load data from an existing table:

python
Copy code
table_name = "test_table"
records = partitioner.read_table(table_name)
This returns the table data as a list of dictionaries, where each dictionary represents a row.

4. Assigning Partitions
Assign partitions to the records based on a specified column (e.g., patient_id) using the assign_partitions() method:

python
Copy code
records = partitioner.assign_partitions(records, partition_column="patient_id")
This adds a partition_key to each row, indicating the assigned partition.

5. Creating a Partitioned Table
Create a partitioned table using the create_partitioned_table() method:

python
Copy code
partitioner.create_partitioned_table("test_partitioned", records)
This creates a table in the database with the specified partitions.

6. Moving Data to the Partitioned Table
Move data into the partitioned table using the move_data_to_partitioned_table() method:

python
Copy code
partitioner.move_data_to_partitioned_table("test_partitioned", records)
Full Example Script
python
Copy code
from partitioning_lib import TablePartitioner

if __name__ == "__main__":
    # Define the path to the .env file and parameters
    env_path = "path/to/.env"
    num_partitions = 15
    table_name = "test_table"

    # Initialize partitioner
    partitioner = TablePartitioner(env_path, num_partitions)

    # Read data from the existing table
    records = partitioner.read_table(table_name)

    # Assign partitions to the records
    records = partitioner.assign_partitions(records, partition_column="patient_id")

    # Create the partitioned table
    partitioner.create_partitioned_table("test_partitioned", records)

    # Move the data to the partitioned table
    partitioner.move_data_to_partitioned_table("test_partitioned", records)
Error Handling
The library includes error-handling mechanisms for common issues:

Missing Credentials: Raises a ValueError if required environment variables are missing.
Table Reflection Errors: Raises an exception if the specified table does not exist or if an error occurs during reflection.
Data Insertion Errors: Raises an SQLAlchemyError if an error occurs while inserting data into the partitioned table.
Example of Error Handling:
python
Copy code
try:
    partitioner.read_table("non_existent_table")
except Exception as e:
    print(f"Error: {e}")