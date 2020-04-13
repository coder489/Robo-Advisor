
import pytest

from app.robo_advisor import get_response

@pytest.fixture(scope="session")
def stock_data():
    return get_response("tsla", API_KEY)

##Code basis written with help form Calvin, but edited to match my code