# Database Tool for SQL Server

This Python module, `database_tool.py`, provides a comprehensive solution for managing simple connections to SQL Server databases, executing queries, and handling data within a Python application. It leverages the power of SQLAlchemy and pyODBC for efficient database operations.

## Features

- **Dynamic Driver Selection**: Automatically finds and uses the appropriate ODBC driver for SQL Server available on the system.
- **Connection Management**: Simplifies the process of connecting to a SQL Server database using either Windows Authentication or standard SQL Server authentication.
- **Query Execution**: Facilitates executing SQL queries directly against the connected database and optionally committing transactions.
- **Data Retrieval**: Includes a method for executing a query and directly storing the results in a pandas DataFrame, ideal for data analysis tasks.
- **Logging**: Integrates Python's logging module to log database connection activities, query executions, and potential errors for troubleshooting.

## Pre-requisites

- Python 3.x
- SQLAlchemy
- pyODBC
- pandas (for the `save_query_df` method)
- An ODBC driver for SQL Server installed on the system

## Installation

Ensure you have Python installed on your system and then install the required packages using pip:

```bash
pip install sqlalchemy pyodbc pandas
```

## Usage

1. **Import the Module**: First, import the `MSSQLDatabaseManager` class from the `database_tool.py` file.

    ```python
    from database_tool import MSSQLDatabaseManager
    ```

2. **Create an Instance**: Initialize the database manager with your database connection details. You can use either Windows Authentication or standard SQL Server authentication, plus for SQL Server authentication, you can create environment variables for the database credentials. 
Use the names **SQLUID** and **SQLPWD** for the username and password, respectively.

    ```python
    db_manager = MSSQLDatabaseManager(database='YourDatabaseName', server='YourServerAddress', user='YourUsername', password='YourPassword')
    ```
   or using Windows Authentication:
    ```python
    db_manager = MSSQLDatabaseManager(database='YourDatabaseName', server='YourServerAddress', trusted_connection=True)
    ```
    or using environment variables:
    ```python
    db_manager = MSSQLDatabaseManager(database='YourDatabaseName', server='YourServerAddress')
    ```    

3. **Execute Queries**: Use the `run_query` method to execute SQL queries.
The result is the memory address of the query, to see tables and columns use the save_query_df method bellow.

    ```python
    result = db_manager.run_query("SELECT * FROM YourTable")
    ```

4. **Retrieve Data as DataFrame**: For data analysis, execute a query and retrieve the results as a pandas DataFrame.

    ```python
    df = db_manager.save_query_df("SELECT * FROM YourTable")
    ```
5. **Use to upload a dataframe**: You can use the object to upload a dataframe using the pandas method to_sql.

    ```python
    df.to_sql('YourTable', db_manager.engine, schema='dbo', if_exists='replace', index=False)
    ```

5. **Disconnect**: Properly close the database connection when done.

    ```python
    db_manager.disconnect()
    ```

## Logging

The module is configured to log activities to a file named `database_tool.log` in the same directory as the module. Ensure the application has write permissions to the directory for logging to work correctly.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Contributing

Contributions to enhance `database_tool.py`, such as adding support for more database systems or improving existing functionalities, are welcome. Please fork the repository, make your changes, and submit a pull request.

