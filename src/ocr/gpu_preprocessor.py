# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false

import cv2
from pathlib import Path
from src.common.config import USE_GPU


def preprocess_image(input_path: Path, output_path: Path) -> Path:
    img = cv2.imread(str(input_path), cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise RuntimeError("Failed to load image")

    if USE_GPU and cv2.cuda.getCudaEnabledDeviceCount() > 0:
        gpu_img = cv2.cuda_GpuMat()
        gpu_img.upload(img)
        gpu_img = cv2.cuda.fastNlMeansDenoising(gpu_img)
        img = gpu_img.download()
    else:
        img = cv2.fastNlMeansDenoising(img)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), img)

    return output_path
