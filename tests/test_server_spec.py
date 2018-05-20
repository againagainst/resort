from resort.server_spec import ServerSpecReader


def test_spec_reader():
    sr = ServerSpecReader('../data/basic-apispec.json')
    assert sr is not None
