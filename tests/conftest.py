"""
Pytest configuration and shared fixtures for the Sudoku application tests.

This file defines fixtures used across all test modules, such as the Flask app
test client for testing routes.
"""

import pytest
import sys
import os

# Add the parent directory to sys.path so we can import app and sudoku_logic
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """
    Fixture: Flask test client
    
    Provides a test client for making requests to the Flask application.
    The Flask app is configured with testing enabled to disable error catching
    during request handling.
    
    Returns:
        FlaskClient: Test client for the app
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    """
    Fixture: Flask application context
    
    Provides an application context for tests that need to interact with
    Flask's global state.
    
    Yields:
        Flask app with active context
    """
    with app.app_context():
        yield app
