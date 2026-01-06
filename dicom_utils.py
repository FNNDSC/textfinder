import numpy as np
import pydicom

def dicom_to_uint8(ds):
    img = ds.pixel_array.astype(np.float32)

    # Apply rescale slope/intercept if present
    if hasattr(ds, "RescaleSlope") and hasattr(ds, "RescaleIntercept"):
        img = img * float(ds.RescaleSlope) + float(ds.RescaleIntercept)

    # Windowing (if present)
    if hasattr(ds, "WindowCenter") and hasattr(ds, "WindowWidth"):
        wc = ds.WindowCenter
        ww = ds.WindowWidth

        # Handle multi-value fields
        wc = wc[0] if isinstance(wc, list) else wc
        ww = ww[0] if isinstance(ww, list) else ww

        min_val = wc - ww / 2
        max_val = wc + ww / 2
        img = np.clip(img, min_val, max_val)

    # Normalize to 0–255
    img -= img.min()
    img /= img.max() + 1e-6
    img = (img * 255).astype(np.uint8)

    return img

