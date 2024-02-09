import cv2

def putTextRect(img, text, pos, scale=3, thickness=1, colorT=(255, 255, 255),
                colorR=(255, 0, 255), font=cv2.FONT_HERSHEY_PLAIN,
                offset=3, border=None, colorB=(0, 255, 0)):
    """
    Creates Text with Rectangle Background
    Parameters - 
        :img: The image where the text and rectangle will be added.
        :text: The text to be displayed inside the rectangle.
        :pos: The starting position of the rectangle (top-left corner coordinates x1, y1).
        :scale: The size of the text.
        :thickness: The thickness of the text.
        :colorT: The color of the text.
        :colorR: The color of the rectangle.
        :font: The font used for the text, specified by cv2.FONT_....
        :offset: The clearance around the text inside the rectangle.
        :border: The thickness of the outline around the rectangle.
        :colorB: The color of the outline.
    """
    # Calculations to be done in order to set the rectangle background and the text display
    ox, oy = pos
    (w, h), _ = cv2.getTextSize(text, font, scale, thickness)

    x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset

    cv2.rectangle(img, (x1, y1), (x2, y2), colorR, cv2.FILLED)
    if border is not None:
        cv2.rectangle(img, (x1, y1), (x2, y2), colorB, border)
    cv2.putText(img, text, (ox, oy), font, scale, colorT, thickness)

    return img, [x1, y2, x2, y1]