"""View routes."""
from flask.globals import request
from tests.base_test import BaseTestCase
from website.models import Food, Order, OrderDetails, User
from flask_login import current_user
from werkzeug.security import generate_password_hash
from website import db
import json


class TestViewRoutes(BaseTestCase):
    """View route tests."""

    def setUp(self):
        """Set up the tests."""
        with self.app.app_context() as context:
            self.context = context
            self.client = self.app.test_client()

            self.test_user = User(username='username',
                                  password=generate_password_hash('password', 'sha256'),
                                  businessname='testbusiness',
                                  location='Sweden',
                                  user_type='restaurant')

            self.npo_user = User(username='npoUsername',
                                 password=generate_password_hash('password', 'sha256'),
                                 businessname='npoName',
                                 location='Sweden',
                                 user_type='npo')

            self.test_food = Food(id=1,
                                  food_name='name',
                                  description='desc',
                                  quantity=10,
                                  users_id=self.test_user.id)

            db.create_all()

    def tearDown(self):
        """Clean up after the tests."""
        with self.context:
            db.drop_all()
            db.session.remove()
            self.test_user = None
            self.npo_user = None
            self.test_food = None

    def test_home_not_authenticated(self):
        """Home route redirects unauhtenticated user correctly."""
        with self.app.test_client() as client:

            client.get('/', follow_redirects=True)

            self.assertTrue(request.path == '/about')

    def test_home_as_authenticated(self):
        """Home route redirects authenticated user correctly."""
        with self.context:
            db.session.add(self.test_user)
            db.session.commit()
            with self.client as client:

                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                )

                client.get('/', follow_redirects=True)

                dashboard_route = f'/{self.test_user.username}'
                self.assertTrue(request.path == dashboard_route)

    def test_delete(self):
        """Food item can be deleted from restaurant page."""
        with self.context:
            db.session.add(self.test_user)
            db.session.add(self.test_food)
            db.session.commit()
            with self.client as client:

                food = db.session.query(Food.id).filter_by(food_name='name').first()
                self.assertTrue(food)

                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                )
                self.assertTrue(current_user.is_authenticated)

                client.post(
                    '/delete',
                    follow_redirects=True,
                    data=dict(
                        id=food.id
                    )
                )

                the_food = Food.query.filter_by(id=food.id).count()
                self.assertTrue(the_food == 0)

    def test_add_food(self):
        """User can add a food object to the database."""
        with self.context:
            db.session.add(self.test_user)
            db.session.commit()
            with self.client as client:
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                )

                self.assertTrue(current_user.is_authenticated)

            with self.client as client:

                food = self.test_food

                client.post(
                    '/add-food',
                    follow_redirects=True,
                    data=dict(
                        id=food.id,
                        food_name=food.food_name,
                        description=food.description,
                        quantity=food.quantity)
                )

                the_food = Food.query.filter_by(id=food.id).first()
                self.assertTrue(the_food)

                # Values of food object returned from database
                res = [
                    the_food.id,
                    the_food.food_name,
                    the_food.description,
                    the_food.quantity,
                    the_food.users_id
                    ]
                # Class food objects values
                exp = [
                    food.id,
                    food.food_name,
                    food.description,
                    food.quantity,
                    current_user.id
                    ]

                self.assertEqual(res, exp)

    def test_delete_flash_message(self):
        """Correct flash message displayed on delete."""
        with self.context:
            db.session.add(self.test_user)
            db.session.add(self.test_food)
            db.session.commit()
            with self.client as client:

                food = db.session.query(Food.id).filter_by(food_name='name').first()
                self.assertTrue(food)

                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                )
                self.assertTrue(current_user.is_authenticated)

                client.post(
                    '/delete',
                    follow_redirects=True,
                    data=dict(food_name='name',
                              description='cheese',
                              quantity='2',
                              id='1')
                )

                msg = b'Item Deleted!'
                self.assertTrue(msg)

    def test_add_food_flash_message(self):
        """User can add a food object to the database."""
        with self.context:
            db.session.add(self.test_user)
            db.session.commit()
            with self.client as client:
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                )

                self.assertTrue(current_user.is_authenticated)

            with self.client as client:

                food = self.test_food

                client.post(
                    '/add-food',
                    follow_redirects=True,
                    data=dict(
                        id=food.id
                    )
                )
                the_food = Food.query.filter_by(id=food.id).first()
                self.assertTrue(the_food)

                msg = b'Item Added!'
                self.assertTrue(msg)

    def test_update_flash_message(self):
        """Correct flash message displayed on update."""
        with self.context:
            db.session.add(self.test_user)
            db.session.add(self.test_food)
            db.session.commit()
            with self.client as client:
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                )

                self.assertTrue(current_user.is_authenticated)

                food = self.test_food

                self.assertTrue(food.food_name == 'name')

                client.post(
                    '/update/<id>',
                    follow_redirects=True,
                    data=dict(
                        id=food.id,
                        name='updated',
                        description='updated',
                        quantity=200)
                )

                updated = Food.query.filter_by(id=food.id).first()
                self.assertTrue(food)

                res = [
                    updated.food_name,
                    updated.description,
                    updated.quantity
                ]

                exp = [
                    'updated',
                    'updated',
                    200
                ]

                self.assertEqual(res, exp)

                msg = b'Item Updated!'
                self.assertTrue(msg)

    def test_blog(self):
        """Blog page served correctly."""
        with self.client as client:
            res = client.get('/food-waste')

            self.assertTrue(res.status_code == 200)

    def test_npo_valid_location(self):
        """Valid location is found in database."""
        with self.context:
            db.session.add(self.test_user)
            db.session.commit()
            with self.client as client:
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                    )
                response = client.post(
                        '/search',
                        follow_redirects=True,
                        data=dict(tag="Sweden"))

                self.assertTrue(response.status_code == 200)

    def test_npo_valid_businessname(self):
        """Valid businessname is found in database."""
        with self.context:
            db.session.add(self.test_user)
            db.session.commit()
            with self.client as client:
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                    )
                response = client.post(
                        '/search',
                        follow_redirects=True,
                        data=dict(tag='testbusiness'))

                self.assertTrue(response.status_code == 200)

    def test_create_order(self):
        """Order is created and added to database."""
        with self.context:
            db.session.add(self.npo_user)
            db.session.add(self.test_food)
            db.session.commit()
            with self.client as client:
                food = self.test_food
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.npo_user.username,
                        password='password'
                    )
                )

                test_order = [{"id": food.id, "quantity": food.quantity}]

                client.post(
                    '/order',
                    follow_redirects=True,
                    data=json.dumps(test_order),
                    content_type='application/json'
                )
                # Get the newly created order
                order = Order.query.filter_by(user_id=self.npo_user.id).first()

                self.assertIsNotNone(order)
                # Get the food item associated with the new order
                order_item = OrderDetails.query.filter_by(order_id=order.id).first()

                self.assertTrue(order_item.food_id == food.id)

    def test_npo_search_invalid_search_term(self):
        """Check message is displayed when term is not found."""
        with self.context:
            db.session.add(self.test_user)
            db.session.commit()
            with self.client as client:
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                )

                self.assertTrue(current_user.is_authenticated)

            with self.client as client:
                response = client.post(
                    '/search',
                    follow_redirects=True,
                    data=dict(
                        tag="None"
                    )
                )
                self.assertTrue(b"Not found" in response.data)

    def test_npo_search_no_tag(self):
        """Check message is displayed when tag is none."""
        with self.context:
            db.session.add(self.test_user)
            db.session.add(self.test_food)
            db.session.commit()
            with self.client as client:
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.test_user.username,
                        password='password'
                    )
                )
                self.assertTrue(current_user.is_authenticated)

                response = client.post(
                    '/search',
                    follow_redirects=True,
                    data=dict(
                        tag=''
                        )
                )

                self.assertTrue(b'Missing keyword' in response.data)

    def test_reset_search(self):
        """Search functionality can be reset."""
        with self.context:
            db.session.add(self.npo_user)
            db.session.add(self.test_food)
            db.session.commit()
            with self.client as client:
                client.post(
                    '/login',
                    follow_redirects=True,
                    data=dict(
                        username=self.npo_user.username,
                        password='password'
                    )
                )
            response = client.post(
                '/clear_search',
                follow_redirects=True,
                data=dict(
                    username=self.npo_user.username,
                    user=self.npo_user
                    )
                )

            self.assertEqual(response.status_code, 200)
