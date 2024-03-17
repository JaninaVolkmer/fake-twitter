import base64
from io import BytesIO

import pytest
from PIL import Image


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def client():
    from rest_framework.test import APIClient

    from users.models import User

    user = User.objects.create(
        username="testuser", first_name="Test", last_name="User", email="user@test.com"
    )

    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def temporary_avatar():

    in_mem_file = BytesIO()
    image = Image.new("RGB", (100, 100), color="blue")
    image.save(in_mem_file, format="jpeg")
    # reset file pointer to start
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()

    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    base64_encoded_result_str = base64_encoded_result_bytes.decode("ascii")
    return base64_encoded_result_str