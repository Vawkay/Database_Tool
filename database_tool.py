import logging
import sqlalchemy
import pyodbc
import os
from sqlalchemy.orm import sessionmaker
import urllib
from sqlalchemy import text

# Configuring the logger
logging.basicConfig(filename='database_tool.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DBLogger')


def find_driver(db_system):
    """
    Finds ODBC drivers available on the system.
    Returns the name of the driver found or None if none is found.
    Examples: 'ODBC Driver 17 for SQL Server', 'ODBC Driver 13 for SQL Server'
    """
    # TODO: Implement new system drivers for new classes in future versions
    if db_system not in ['SQL Server']:
        logger.error("Invalid database system. Please provide a valid database system name.")
        return None
    drivers = [driver for driver in pyodbc.drivers() if db_system in driver]
    if drivers:
        # Returns the last known compatible driver found, usually the most updated one
        return drivers[-1]
    else:
        return None


class MSSQLDatabaseManager:
    """
    DatabaseManager Class
    This class provides methods for connecting to a SQL Server database,
    running queries and procedures, and disconnecting from the database,
    along with additional data manipulation and management functionalities.
    """

    def __init__(self, database, server='db.perseus.com.br',
                 port=44324, user=None, password=None, use_trusted_connection=False) -> None:
        """
        Initializes the DatabaseManager instance with connection parameters for a SQL Server database.
        Args:
            database (str): The name of the database to connect to.
            server (str, optional): The address of the database server. Defaults to 'db.perseus.com.br'.
            port (int, optional): The port number on which the database server is listening. Defaults to 44324.
            user (str, optional): The username for database authentication. If not provided, it attempts to use the SQLUID environment variable.
            password (str, optional): The password for database authentication. If not provided, it attempts to use the SQLPWD environment variable.
            use_trusted_connection (bool, optional): Whether to use Windows Authentication for connecting to the database. Defaults to False.
        Raises:
            Exception: If an ODBC driver for SQL Server is not found or if there is an error in establishing a connection to the database.
        """
        self.driver = find_driver('SQL Server')
        if not self.driver:
            logger.error("ODBC Driver for SQL Server not found. Please install the driver and try again.")
            raise Exception("ODBC Driver for SQL Server not found. Please install the driver and try again.")
        self.server = server
        self.port = port
        self.database = database
        self.user = user or os.environ.get('SQLUID')
        self.password = password or os.environ.get('SQLPWD')
        self.use_trusted_connection = use_trusted_connection

        if self.use_trusted_connection:
            self.params = urllib.parse.quote_plus(f"DRIVER={self.driver};"
                                                  f"SERVER={self.server},{self.port};"
                                                  f"DATABASE={self.database};"
                                                  f"Trusted_Connection=yes;")
        else:
            self.params = urllib.parse.quote_plus(f"DRIVER={self.driver};"
                                                  f"SERVER={self.server},{self.port};"
                                                  f"DATABASE={self.database};"
                                                  f"UID={self.user};"
                                                  f"PWD={self.password};"
                                                  f"Trusted_Connection=no;")

        try:
            self.engine = sqlalchemy.create_engine(f"mssql+pyodbc:///?odbc_connect={self.params}",
                                                   fast_executemany=True, echo=True)
            session = sessionmaker(bind=self.engine)
            self.session = session()
            self.conn = self.engine.connect()
            logger.info("DB Connected!")
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise

    def run_query(self, query, commit=False):
        """
        Executes a SQL query against the connected database.
        Args:
            query (str): The SQL query to execute.
            commit (bool, optional): Whether to commit the transaction. Defaults to False.
        Returns:
            The result of the executed query.
        This method executes a given SQL query using the current database connection.
        If `commit` is True, the transaction is committed.
        """
        logger.info(f"Executing query: {query}")
        try:
            with self.engine.begin() as conn:
                query = text(str(query))  # Convert the query into a textual SQL expression
                result = conn.execute(query)
                if commit:
                    self.session.commit()
                logger.info("Query executed successfully!")
            return result
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise

    def save_query_df(self, query):
        """
        Executes a SQL query and stores the results in a pandas DataFrame.
        Args:
            query (str): The SQL query to execute.
        Returns:
            pandas.DataFrame: A DataFrame containing the results of the executed query.
        This method directly executes a given SQL query and stores the results in a pandas DataFrame,
        leveraging the pandas `read_sql_query` function for convenience and efficiency.
        """
        import pandas as pd
        # Execute the query and store the results in a DataFrame directly
        df = pd.read_sql_query(query, self.engine)
        return df

    def disconnect(self):
        try:
            self.conn.close()
            self.engine.dispose()
            logger.info("DB Disconnected!")
        except Exception as e:
            logger.error(f"Disconnection error: {e}")
            raise
