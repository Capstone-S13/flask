# def test_landing_page(test_client, init_database):
#     response = test_client.get('/customer/landing',
#                                follow_redirects=True)
#     assert response.status_code == 200
    # assert b'Please login' in response.data
    # assert b'Customer Landing' in response.data
    # assert b'Customer' in response.data
    # assert b'View your orders' in response.data
    # assert b'Shops' in response.data
    # assert b'Delivery' in response.data
    # assert b'Settings' in response.data
    # assert b'Logout' in response.data