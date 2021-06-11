"""Init."""
import unittest
from website import create_test_app


class BaseTestCase(unittest.TestCase):
    """Base Test class."""

    app = create_test_app()
