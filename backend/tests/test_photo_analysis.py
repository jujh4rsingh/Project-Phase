from io import BytesIO

from PIL import Image
from fastapi.testclient import TestClient

from backend.main import app


def make_image(color: tuple[int, int, int]) -> bytes:
    image = Image.new("RGB", (320, 320), color)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def test_photo_rejects_non_image_bytes() -> None:
    response = TestClient(app).post(
        "/api/users/demo-user-001/skin-photo/analyze",
        files={"photo": ("photo.png", b"not-an-image", "image/png")},
    )

    assert response.status_code == 200
    assert response.json()["analysis_possible"] is False
    assert "readable image" in response.json()["message"]


def test_photo_result_is_pixel_derived() -> None:
    client = TestClient(app)
    bright = client.post("/api/users/demo-user-001/skin-photo/analyze", files={"photo": ("bright.png", make_image((220, 180, 150)), "image/png")}).json()
    dark = client.post("/api/users/demo-user-001/skin-photo/analyze", files={"photo": ("dark.png", make_image((40, 30, 25)), "image/png")}).json()

    assert bright["analysis_possible"] is True
    assert dark["analysis_possible"] is False or bright["dryness_indicator"] != dark["dryness_indicator"]
