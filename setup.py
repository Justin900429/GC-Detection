from setuptools import setup
import platform

with open("README.md", "r") as f:
    long_description = f.read()

requirements = [
        "PyYAML",
        "opencv-python",
        "pillow",
        "google-cloud-vision",
        "google-cloud-storage",
    ]

if platform.system() == "Darwin":
    requirements.append("tkmacosx")

setup(
    name="GCDetection",
    packages=["gcdetection"],
    install_requires=requirements,
    download_url="https://github.com/Justin900429/GC-Detection/archive/0.9.0.tar.gz",
    license="MIT",
    version="1.0.0",
    keywords=['Google Cloud', 'Vision API', 'Object detection'],
    author="Justin Ruan, Joyce Fang",
    author_email="justin900429@gmail.com, objdoctor891213@gmail.com",
    description="Project for using Cloud Vision API to quickly deployed the object detection application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Justin900429/GC-Detection",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
