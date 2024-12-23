from funcs import read_from_existing_table, create_partitioned_table, partition_existing_empty_table
from help_funcs import map_python_to_sql, assign_segment_md5
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, MetaData, Table

# num_partition = 20

# connection_string = "postgresql+psycopg2://postgres:apolo@localhost:5432/partition_project"

# dict_res = read_from_existing_table(connection_string=connection_string, table_name="test_table")


# for record in dict_res:
#     record['part'] = assign_segment_md5(record['patient_id'],num_partition)



# columns = {c: type(t) for c, t in zip(dict_res[0].keys(), dict_res[0].values())}
# columns = map_python_to_sql(columns)
# print(columns)

# create_partitioned_table(connection_string, "test", columns, num_partition)


class TablePartitioner:
    def __init__(self, connection_string, num_partition):
        self.connection_string = connection_string
        self.num_partition = num_partition
        self.engine = create_engine(self.connection_string)
        self.metadata = MetaData()
        
    def read_table(self, table_name):
        return read_from_existing_table(self.engine, table_name=table_name)

    def assign_partitions(self, records, partition_column):

        for record in records:
            record["part"] = assign_segment_md5(
                record[partition_column], self.num_partition
            )
        return records

    def create_partitioned_table(self, table_name, records):

        columns = {c: type(t) for c, t in zip(records[0].keys(), records[0].values())}
        sql_columns = map_python_to_sql(columns)
        print(f"Inferred SQL columns: {sql_columns}")
        
        create_partitioned_table(
            self.engine, table_name, sql_columns, self.num_partition
        )
        
    def move_data_to_partitioned_table(self, table_name, data):

        if not data:
            raise ValueError("Data is empty. Nothing to insert.")
        
        try:
            # Reflect the table structure from the database
            self.metadata.reflect(bind=self.engine)
            table = self.metadata.tables.get(table_name)
            
            if table is None:
                raise ValueError(f"Table {table_name} does not exist.")
            
            # Insert data using SQLAlchemy's connection
            with self.engine.connect() as connection:
                connection.execute(table.insert(), data)
            
            print(f"Data successfully inserted into {table_name}.")
        
        except SQLAlchemyError as e:
            print(f"Error inserting data into {table_name}: {e}")
            raise

# Example usage
if __name__ == "__main__":
    connection_string = "postgresql+psycopg2://postgres:apolo@localhost:5432/partition_project"
    num_partitions = 15
    table_name = "test_table"
    
    partitioner = TablePartitioner(connection_string, num_partitions)
    records = partitioner.read_table(table_name)
    records = partitioner.assign_partitions(records, partition_column="patient_id")
    partitioner.create_partitioned_table("test3", records)
    partitioner.move_data_to_partitioned_table("test3_partitioned",records)


