import cv2
import numpy as np

from PIL import Image
import requests
from io import BytesIO
from collections import Counter
import colorsys

def getColor(url: str) -> str:
    """
    From an image (at given URL) create the most vibrant color
    """
    response = requests.get(url, timeout=500)
    response.raise_for_status()

    img = Image.open(BytesIO(response.content)).convert("RGBA")
    img.thumbnail((200, 200)) # Resize image

    colors = []

    for r, g, b, a in img.getdata():
        # Ignore transparent pixels
        if a < 128: continue
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

        # Ignore gray colors
        if s < 0.35: continue

        # Ignore very dark/light colors
        if l < 0.2 or l > 0.85: continue

        colors.append((r, g, b))

    if not colors:
        colors = [(r, g, b) for r, g, b, _ in img.getdata()]

    r, g, b = Counter(colors).most_common(1)[0][0]

    return f"#{r:02X}{g:02X}{b:02X}"

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left

    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = int(max(widthA, widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = int(max(heightA, heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)

    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

if __name__ == "__main__":
    print(getColor("https://moly.hu/system/covers/big/covers_936313.jpg?1757316942"))
    exit()
    # Load image
    image = cv2.imread("./Test/A_harmadik_lany.jpg")
    orig = image.copy()

    # Resize for easier processing
    ratio = image.shape[0] / 800.0
    image = cv2.resize(image, (int(image.shape[1] / ratio), 800))

    # Preprocess
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(gray, 75, 200)

    # Find contours
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    book_contour = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            book_contour = approx
            break

    if book_contour is None:
        raise Exception("Could not detect book.")

    # Scale contour back up
    pts = book_contour.reshape(4, 2) * ratio

    # Perspective correction
    scanned = four_point_transform(orig, pts)

    # Save result
    cv2.imwrite("book_scanned.jpg", scanned)

    print("Done.")