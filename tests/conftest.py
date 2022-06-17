import pytest
from application import create_app, db
from application.models import UserDb, OrderDb, IngressDb
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_login import login_user, logout_user, login_manager

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('project.config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        
@pytest.fixture(scope='module')
def new_user():
    user = UserDb(id="customerIdnuMber647",
                  email='jhenderson@gmail.com',
                  name='James Henderson',
                  password=generate_password_hash('vEryS#cur3password'),
                  postalCode='S123456',
                  unitNumber='#12-987',
                  accountType=0)
    return user

@pytest.fixture(scope='module')
def new_order():
    timeNow = datetime.utcnow
    order = OrderDb(orderId="orderIdnumber1346",
                    customerId="customerIdnuMber647",
                    storeId="storeIdnuMBer928",
                    orderDetails='1X Successful test',
                    status="Order Sent",
                    robotID="foodGrabRobot326",
                    dateCreated=timeNow)
    return order

@pytest.fixture(scope='module')
def new_ingress():
    ingress = IngressDb(postalCode=123456,
                        ingressPoint = "Changi City Point")
    return ingress

@pytest.fixture(scope='module')
def test_client():
    app = create_app('flask_test.cfg')
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
            
@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = UserDb(id="customerIdnuMber69123",
                  email='jdoe@gmail.com',
                  name='John Doe',
                  password=generate_password_hash('weakpassword'),
                  postalCode='S917341',
                  unitNumber='#24-324',
                  accountType=0)
    user2 = UserDb(id="storeIdnuMber623",
                  email='bestshop@gmail.com',
                  name='Best Shop',
                  password=generate_password_hash('str0ngp@ssw0rd'),
                  postalCode='S813631',
                  unitNumber='#03-723',
                  accountType=1)
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield
    
    db.drop_all()
    
@pytest.fixture()
def test_with_customer_user(test_client):
    @login_manager.request_loader
    def load_user_from_request():
        return UserDb.query("customerIdnuMber69123").first()
    
@pytest.fixture
def user():
    return UserDb(id="customerIdnuMber69123",
                  email='jdoe@gmail.com',
                  name='John Doe',
                  password=generate_password_hash('weakpassword'),
                  postalCode='S917341',
                  unitNumber='#24-324',
                  accountType=0)