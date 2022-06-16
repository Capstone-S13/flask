def test_signup_page(test_client):
    response = test_client.get('/signup')
    assert response.status_code == 200
    assert b'Sign Up' in response.data
    assert b'Name' in response.data
    assert b'Account Type' in response.data
    assert b'Customer' in response.data
    assert b'Vendor' in response.data
    assert b'Postal Code' in response.data
    assert b'Unit Number' in response.data
    assert b'Email address' in response.data
    assert b'Password' in response.data
    assert b'Have an Account? Login here' in response.data    
    
def test_valid_signup(test_client, init_database):
    response = test_client.post('/signup',
                                data=dict(name='Jane Doe',
                                          email='janeDoe@gmail.com',
                                          password='password',
                                          postalCode='S172632',
                                          unit='#06-151',
                                          accType='0'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Please login' in response.data
    assert b'Email address' in response.data
    assert b'Password' in response.data
    assert b'No Account? Sign Up here' in response.data
    
def test_invalid_signup_user_already_exist(test_client, init_database):
    response = test_client.post('/signup',
                                data=dict(name='Jane Doe',
                                          email='jdoe@gmail.com',
                                          password='password',
                                          postalCode='S172632',
                                          unit='#06-151',
                                          accType='0'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign Up' in response.data
    assert b'Name' in response.data
    assert b'Account Type' in response.data
    assert b'Customer' in response.data
    assert b'Vendor' in response.data
    assert b'Postal Code' in response.data
    assert b'Unit Number' in response.data
    assert b'Email address' in response.data
    assert b'Password' in response.data
    assert b'Have an Account? Login here' in response.data 



def test_login_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Please login' in response.data
    assert b'Email address' in response.data
    assert b'Password' in response.data
    assert b'No Account? Sign Up here' in response.data
    
    
def test_valid_login_customer(test_client, init_database):
    response = test_client.post('/',
                                data=dict(email='jdoe@gmail.com',
                                          password='weakpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Customer Landing' in response.data
    assert b'Customer' in response.data
    assert b'View your orders' in response.data
    assert b'Shops' in response.data
    assert b'Delivery' in response.data
    assert b'Settings' in response.data
    assert b'Logout' in response.data

def test_valid_login_logout_customer(test_client, init_database):
    response = test_client.post('/',
                                data=dict(email='jdoe@gmail.com',
                                          password='weakpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Customer Landing' in response.data
    assert b'Customer' in response.data
    assert b'View your orders' in response.data
    assert b'Shops' in response.data
    assert b'Delivery' in response.data
    assert b'Settings' in response.data
    assert b'Logout' in response.data

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please login' in response.data
    assert b'Email address' in response.data
    assert b'Password' in response.data
    assert b'No Account? Sign Up here' in response.data
    
    
    
def test_valid_login_store(test_client, init_database):
    response = test_client.post('/',
                                data=dict(email='bestshop@gmail.com',
                                          password='str0ngp@ssw0rd'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Store Landing' in response.data
    assert b'Shop Owner' in response.data
    assert b'View all orders and their status' in response.data
    assert b'Incoming' in response.data
    assert b'Preparing' in response.data
    assert b'Delivery' in response.data
    assert b'Settings' in response.data
    assert b'Logout' in response.data

def test_valid_login_logout_store(test_client, init_database):
    response = test_client.post('/',
                                data=dict(email='bestshop@gmail.com',
                                          password='str0ngp@ssw0rd'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Store Landing' in response.data
    assert b'Shop Owner' in response.data
    assert b'View all orders and their status' in response.data
    assert b'Incoming' in response.data
    assert b'Preparing' in response.data
    assert b'Delivery' in response.data
    assert b'Settings' in response.data
    assert b'Logout' in response.data

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please login' in response.data
    assert b'Email address' in response.data
    assert b'Password' in response.data
    assert b'No Account? Sign Up here' in response.data
    
    
    
def test_invalid_login_wrong_password(test_client, init_database):
    response = test_client.post('/',
                                data=dict(email='jdoe@gmail.com',
                                          password='strongpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Please login' in response.data
    assert b'Email address' in response.data
    assert b'Password' in response.data
    assert b'No Account? Sign Up here' in response.data
    
def test_invalid_login_user_not_found(test_client, init_database):
    response = test_client.post('/',
                                data=dict(email='james@gmail.com',
                                          password='strongpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Please login' in response.data
    assert b'Email address' in response.data
    assert b'Password' in response.data
    assert b'No Account? Sign Up here' in response.data
