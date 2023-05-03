from applications import app
import pytest
def test_default():
    resp = app.test_client().get('/')
    assert resp.status_code == 200
    assert resp.data.decode('utf-8') == 'hello'

def test_increase_level():
    resp = app.