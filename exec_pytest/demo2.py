# test_fixture.py
import pytest

# TODO little test_case, more work with source data.

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

@pytest.fixture(scope='module')
def db3():
    # consume db, query
    data = '3'
    return data

@pytest.fixture(scope='module')
def db4():
    # consume db, query
    data = '4'
    return data

@pytest.fixture(scope='module')
def data_pair(db,db2,db3,db4):
    # for i in range(2):
    yield [db,db2,db3,db4]
    # print('data %s' % request.param)


def test_data(public_topic, data_pair):
    result = True
    for data in data_pair:
        if data not in public_topic:
            result = False
            break
    # compare()
    assert result

def test_2(data_pair):
    # compare()
    assert data_pair[1] in data_pair[0]

# def test_data_2(data):
#     assert data == 1

if __name__=='__main__':
    pytest.main("-v -s demo2.py::test_data")

    # # 运行spec_001_modul_test模块中用例名称包含spec的用例
    # pytest.main("-v -s -k spec spec_001_modul_test.py")
    # # 运行当前文件夹匹配Test_Class的用例，类文件下面的用例
    # pytest.main('-s -v -k Test_Class')