import pytest

from parma_analytics import __version__
from parma_analytics.api import app


@pytest.mark.parametrize("arg", [True, False])
def test_dummy(arg: bool):
    assert arg or not arg
    assert app
    assert len(__version__) > 0
