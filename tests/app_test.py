"""Application testing module."""
import unittest
from website import create_app
from flask import Flask


class TestApp(unittest.TestCase):
    """Application test class."""

    def setUp(self):
        """Initialise the tests."""
        self.app = create_app()

    def tearDown(self):
        """Clean up after the tests."""
        self.app = None

    def test_create_app(self):
        """App instance initialized correctly."""
        self.assertIsInstance(self.app, Flask)

    def test_create_app_config(self):
        """Application configuration is correct."""
        app = self.app
        database = app.config['SQLALCHEMY_DATABASE_URI']
        env = app.config['FLASK_ENV']
        secret = app.config['SECRET_KEY']
        debug = app.config['DEBUG']
        track = app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

        self.assertEqual(database, 'sqlite:///sqlite.db')
        self.assertEqual(env, 'development')
        self.assertEqual(secret, 's3cr3t')
        self.assertTrue(debug)
        self.assertFalse(track)
