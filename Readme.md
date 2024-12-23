Table Partitioning Library
This library provides functionality for partitioning tables in a PostgreSQL database using SQLAlchemy. It allows users to:

Read data from an existing table.
Assign partitions to data based on a column (e.g., patient_id).
Create partitioned tables in the database.
Move data into partitioned tables.
Requirements
Before using the library, ensure that you have the following dependencies installed:

python-dotenv: To load environment variables from a .env file.
psycopg2: PostgreSQL adapter for Python.
SQLAlchemy: ORM for Python to interact with PostgreSQL.
You can install the required dependencies using:

bash
Copy code
pip install python-dotenv psycopg2 sqlalchemy
Library Overview
The library provides an object-oriented approach for working with PostgreSQL tables, including:

Reading from an existing table.
Creating partitioned tables.
Inserting data into partitioned tables.
Partitioning data based on the values in a specified column.
The library uses MD5 hashing to assign rows to specific partitions.

Key Functions:
Reading data: Reads data from an existing table.
Assigning partitions: Uses MD5 hashing to assign each row to a partition.
Creating partitioned tables: Creates partitioned tables in PostgreSQL.
Moving data to partitioned tables: Moves data from a source table to the partitioned table.
Setting Up
1. Environment Variables
To avoid hardcoding database credentials, the library uses environment variables stored in a .env file. The .env file should contain the following variables:

env
Copy code
DB_USER=postgres
DB_PASSWORD=apolo
DB_HOST=localhost
DB_PORT=5432
DB_NAME=partition_project
These variables will be loaded by the python-dotenv library to configure the connection to the database.

2. The .env File
You need to create a .env file in the root directory of your project containing the following database credentials:

env
Copy code
DB_USER=postgres
DB_PASSWORD=apolo
DB_HOST=localhost
DB_PORT=5432
DB_NAME=partition_project
This ensures the library can securely access the database without exposing sensitive information directly in the code.

How to Use the Library
1. Importing the Library
The library provides a TablePartitioner class for handling all operations.

python
Copy code
from partitioning_lib import TablePartitioner
2. Initialize the Partitioning Class
To start using the partitioning functionality, you need to create an instance of the TablePartitioner class by passing the connection string and the number of partitions.

python
Copy code
# Example usage:
connection_string = "postgresql+psycopg2://postgres:apolo@localhost:5432/partition_project"
num_partitions = 15  # Number of partitions you want to create

partitioner = TablePartitioner(connection_string, num_partitions)
Alternatively, if you want to load the connection string from the .env file, use the following function:

python
Copy code
from dotenv import load_dotenv
import os

def get_connection_string():
    load_dotenv()
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise ValueError("One or more database credentials are missing in .env file.")
    
    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return connection_string
3. Reading Data from an Existing Table
Once you have initialized the TablePartitioner object, you can use the read_table() method to load data from an existing table in the database.

python
Copy code
# Example:
table_name = "test_table"
records = partitioner.read_table(table_name)
This will return the data from the table as a list of dictionaries, where each dictionary represents a row.

4. Assigning Partitions
To assign partitions to the records based on a specified column (e.g., patient_id), use the assign_partitions() method.

python
Copy code
records = partitioner.assign_partitions(records, partition_column="patient_id")
This will modify the records by adding a part key, indicating the partition each row belongs to, based on the MD5 hash of the patient_id.

5. Creating a Partitioned Table
Once you've assigned partitions, you can create the partitioned table using the create_partitioned_table() method. This method creates a table in the database with the partitions.

python
Copy code
partitioner.create_partitioned_table("test_partitioned", records)
This will create a partitioned table based on the number of partitions provided.

6. Moving Data to Partitioned Table
To move data from the original table into the newly partitioned table, use the move_data_to_partitioned_table() method.

python
Copy code
partitioner.move_data_to_partitioned_table("test_partitioned", records)
This will insert the data into the partitioned table.

Example Full Script
python
Copy code
from partitioning_lib import TablePartitioner
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()

# Get connection string from environment variables
def get_connection_string():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise ValueError("One or more database credentials are missing in .env file.")
    
    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return connection_string

# Define the partitioning parameters
connection_string = get_connection_string()
num_partitions = 15
table_name = "test_table"

# Initialize partitioner
partitioner = TablePartitioner(connection_string, num_partitions)

# Read data from the existing table
records = partitioner.read_table(table_name)

# Assign partitions to the records
records = partitioner.assign_partitions(records, partition_column="patient_id")

# Create the partitioned table
partitioner.create_partitioned_table("test_partitioned", records)

# Move the data to the partitioned table
partitioner.move_data_to_partitioned_table("test_partitioned", records)
Error Handling
The library handles several types of errors, including:

Missing credentials: If any of the required database credentials are missing from the .env file, it raises a ValueError.
Table reflection errors: If a table doesn’t exist or an error occurs during table reflection, it will raise an exception.
Data insertion errors: If an error occurs during the insertion of data into the partitioned table, it raises an SQLAlchemyError.
