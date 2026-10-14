from io import BytesIO

from PIL import Image, UnidentifiedImageError

from backend.schemas.photo import PhotoAnalysisResult


def analyze_image(content: bytes) -> PhotoAnalysisResult:
    try:
        with Image.open(BytesIO(content)) as image:
            image.verify()
        with Image.open(BytesIO(content)) as image:
            rgb = image.convert("RGB")
            width, height = rgb.size
            pixels = list(rgb.resize((32, 32)).getdata())
    except (UnidentifiedImageError, OSError, ValueError):
        return PhotoAnalysisResult(image_quality=0, lighting_quality=0, face_visibility=0, analysis_possible=False, message="This file is not a readable image. Choose a JPEG, PNG, or WebP photo.")

    if width < 160 or height < 160:
        return PhotoAnalysisResult(image_quality=25, lighting_quality=25, face_visibility=15, analysis_possible=False, message="The image is too small for a useful comparison. Choose a photo at least 160 by 160 pixels.")

    brightness = sum((red + green + blue) / 3 for red, green, blue in pixels) / len(pixels)
    spread = sum(abs(((red + green + blue) / 3) - brightness) for red, green, blue in pixels) / len(pixels)
    skin_like = [pixel for pixel in pixels if pixel[0] > pixel[1] * 0.92 and pixel[1] > pixel[2] * 0.9 and pixel[0] - pixel[2] > 12]
    skin_fraction = len(skin_like) / len(pixels)
    red_bias = sum(max(0, red - ((green + blue) / 2)) for red, green, blue in skin_like) / max(1, len(skin_like))
    lighting_quality = max(0, min(100, round(100 - abs(brightness - 128) * 0.75)))
    contrast_quality = max(0, min(100, round(spread * 2.2)))
    quality = round((lighting_quality * 0.55) + (contrast_quality * 0.25) + 20)
    if quality < 45:
        return PhotoAnalysisResult(image_quality=quality, lighting_quality=lighting_quality, face_visibility=35, analysis_possible=False, message="Lighting is too inconsistent to make a useful comparison. Try brighter, indirect light with less shadow.")

    dryness = max(0, min(100, round(70 - (brightness * 0.18) + (spread * 0.2))))
    redness = max(0, min(100, round(red_bias * 2.4)))
    blemish = max(0, min(100, round((1 - min(1, skin_fraction * 2)) * 35)))
    subject_visibility = max(20, min(85, round(skin_fraction * 180)))
    return PhotoAnalysisResult(image_quality=quality, lighting_quality=lighting_quality, face_visibility=subject_visibility, analysis_possible=True, message="Pixel-derived visual indicators are available for comparison only, not medical diagnosis.", dryness_indicator=dryness, redness_indicator=redness, visible_blemish_indicator=blemish, confidence=max(35, quality - 15))