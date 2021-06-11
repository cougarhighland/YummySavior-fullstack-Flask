"""Login test module."""
from flask.globals import request
from website import db
from website.models import User
from flask_login import current_user
from werkzeug.security import generate_password_hash
from tests.base_test import BaseTestCase


class TestLogin(BaseTestCase):
    """User Login tests."""

    def setUp(self):
        """Initialise the test."""
        with self.app.app_context() as context:
            self.context = context
            self.test_user = User(username='username',
                                  password=generate_password_hash('password', 'sha256'),
                                  businessname='business',
                                  location='Sweden',
                                  user_type='restaurant')
            self.context = context
            db.create_all()

            self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after the test."""
        # clear the database at the end of the test
        with self.context:
            db.drop_all()
            db.session.remove()
            self.test_user = None

    def test_login(self):
        """Test GET /login."""
        response = self.client.get('/login')
        res = response.status_code
        exp = 200
        self.assertEqual(res, exp)

    def test_login_success(self):
        """User can log in."""
        # The application context
        with self.context:
            # Add the test user to the database.
            db.session.add(self.test_user)
            db.session.commit()

            # The request context
            with self.client as client:
                # Check current_user has no user object assigned
                self.assertTrue(not current_user)

                # Sign in with test users credentials
                response = client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'))

                # Check current_user has been assigned user object
                self.assertTrue(current_user)
                # Check user is authenticated
                self.assertTrue(current_user.is_authenticated)
                # Check the redirect url matches users dashboard url
                self.assertTrue(request.path == f'/{current_user.username}')
                # Check the status_code of the response.
                self.assertTrue(response.status_code == 200)

    def test_login_redirect(self):
        """Login redirects logged in user when authenticated."""
        with self.context:
            with self.client as client:
                # Add test user to database
                db.session.add(self.test_user)
                db.session.commit()

                # Check current_user has no user object
                self.assertTrue(not current_user)

                # Get login page when not authenticated
                response = client.get('/login', follow_redirects=True)

                # User is not logged in and should load login page CODE: 200
                self.assertTrue(response.status_code == 200)

                # Log the user in
                client.post('/login',
                            follow_redirects=True,
                            data=dict(
                                username=self.test_user.username,
                                password='password')
                            )

                # Check user has been authenticated
                self.assertTrue(current_user.is_authenticated)

                # GET login page when authenticated
                response = client.get('/login', follow_redirects=False)

                # User is now logged in and should be redirected CODE: 302
                self.assertTrue(response.status_code == 302)

    def test_login_wrong_password(self):
        """User cannot log in with wrong password."""
        with self.context:
            with self.client as client:
                # Add test user to database
                db.session.add(self.test_user)
                db.session.commit()

                response = client.post('/login',
                                       follow_redirects=True,
                                       data=dict(
                                           username=self.test_user.username,
                                           password='wrong')
                                       )
                # Check the error message is correct
                msg = b'Incorrect username or password!'
                self.assertTrue(msg in response.data)

    def test_login_wrong_username(self):
        """User cannot log in with incorrect username."""
        with self.context:
            with self.client as client:
                # Add test user to database
                db.session.add(self.test_user)
                db.session.commit()

                response = client.post('/login',
                                       follow_redirects=True,
                                       data=dict(
                                           username='wrong',
                                           password='password')
                                       )

                # Check the error message is correct
                msg = b'Incorrect username or password!'
                self.assertTrue(msg in response.data)

    def test_logout(self):
        """User can log out."""
        with self.context:
            with self.client as client:
                db.session.add(self.test_user)
                db.session.commit()

                client.post('/login',
                            follow_redirects=True,
                            data=dict(
                                username=self.test_user.username,
                                password='password')
                            )

                self.assertTrue(current_user.is_authenticated)

                client.get('/logout', follow_redirects=True)

                self.assertFalse(current_user.is_authenticated)
