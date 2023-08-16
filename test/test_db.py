import pytest
from unittest.mock import patch, mock_open
import db.log_db as log_db
 # Adjust the import based on your directory structure.

# Setup and Teardown can be handled using pytest fixtures.
# In this case, I'll skip them since you're not doing anything in them.

@pytest.fixture
def mock_db_connection():
    with patch('db.log_db.sqlite3.connect') as mock_connect:
        yield mock_connect

def test_setup_database(mock_db_connection):
    log_db.setup_database()
    mock_db_connection.assert_called_once_with(log_db.DB_PATH)

def test_log_generation(mock_db_connection):
    session_id = 'test-session'
    level = 'info'
    module = 'test-module'
    query = 'test-query'
    generation = 'test-generation'
    
    log_db.log_generation(session_id, level, module, query, generation)
    mock_db_connection.assert_called_once_with(log_db.DB_PATH)

def test_get_session_logs(mock_db_connection):
    session_id = 'test-session'
    log_db.get_session_logs(session_id)
    mock_db_connection.assert_called_once_with(log_db.DB_PATH)

def test_get_logs(mock_db_connection):
    log_db.get_logs()
    mock_db_connection.assert_called_once_with(log_db.DB_PATH)
