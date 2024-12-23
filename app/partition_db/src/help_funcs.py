import hashlib
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Float, JSON, MetaData, Table


def assign_segment_md5(patient_id, num_partitions):
    hash_value = hashlib.md5(str(patient_id).encode()).hexdigest()
    return int(hash_value, 16) % num_partitions +1


def map_python_to_sql(data_dict):
    """
    Converts Python types in the dictionary to PostgreSQL types.
    
    Args:
        data_dict (dict): A dictionary where keys are column names and values are Python types.
    
    Returns:
        dict: A dictionary where keys are column names and values are PostgreSQL types.
    """
    type_mapping = {
        str: String,  # For string types, use SQLAlchemy's String
        int: Integer,  # For integers, use SQLAlchemy's Integer
        float: Float,  # Use SQLAlchemy's Float for floating-point numbers
        bool: Boolean,  # Use SQLAlchemy's Boolean for boolean values
        list: Text,  # For lists, consider using Text or JSON
        dict: JSON,  # For dictionaries, use SQLAlchemy's JSON type
        type(None): Text  # Default to Text for None (this can be customized)
    }

    sql_types = {}
    for column, py_type in data_dict.items():
        sql_types[column] = type_mapping.get(py_type, 'TEXT')  # Default to TEXT if type is unknown
    return sql_types