---
tags: [concept]
---
# Transfer learning

遷移學習：用 ImageNet 預訓練骨幹（ResNet/EfficientNet/MobileNet）微調，於小樣本醫療影像收斂更快、更不易過擬合。策略：先凍結暖身再漸進式解凍微調。本專題 MVP 即採此法（見 src/raxray）。
