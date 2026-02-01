# Smashalytics

This project is intended to provide real-time analysis of your SSBU matches while they are being played. The scope of Smashalytics is to provide support on your competitive playstyle, therefore only those matches are supported.


```mermaid
---
title: Architecture
---
flowchart TD
    A[Switch] --> |HDMI Out| B[HDMI Splitter]
    B --> |HDMI Out 1| TV
    B --> |HDMI Out 2| C[PC]
    C --> |ffmpeg| D@{ shape: procs, label: "Frames"}
    D --> E[YOLO]
    D --> E1[Crop characters]
    E1 --> H[Lost stock CNN]
    H --> I[Save]
    H --> J[Output advice]
    E --> |characters' bounding boxes| F1[Save]
    E --> |characters' bounding boxes| F2[Character action CNN]
    F2 --> G[Save]
```