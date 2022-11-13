# test_fixture.py
import pytest

@pytest.fixture(scope='module')
def public_topic():
    # consume kafka
    msg = '1,2,3'
    # transform
    return msg

@pytest.fixture(scope='module')
def db():
    # consume db, query
    data = '1'
    return data

@pytest.fixture(scope='module')
def db2():
    # consume db, query
    data = '2'
    return data

@pytest.fixture(scope='function')
def data_pair(public_topic, db):
    # for i in range(2):
    yield (public_topic, db)
    # print('data %s' % request.param)

@pytest.fixture(scope='function')
def data_pair2(public_topic, db2):
    # for i in range(2):
    yield (public_topic, db2)
    # print('data %s' % request.param)

def test_data(data_pair):
    # compare()
    assert data_pair[1] in data_pair[0]

def test_data2(data_pair2):
    # compare()
    assert data_pair2[1] in data_pair2[0]
#
# def test_data_2(data):
#     assert data == 1

if __name__=='__main__':
    pytest.main()