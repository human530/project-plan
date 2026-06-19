"""遷移學習骨幹 + 任務頭（對應 docs/03：骨幹明確選小以防小樣本過擬合）。

支援 resnet18 / efficientnet_b0（皆為輕量、適合 Colab 與小樣本）。
頭部可選：
- ordinal：輸出 K-1 個 logits 給 CORN（MVP 保底）。
- regression：輸出 1 個連續值（進階；預測標準化後的 SvH 總分）。
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torchvision


def _build_backbone(name: str, pretrained: bool):
    if name == "resnet18":
        weights = torchvision.models.ResNet18_Weights.DEFAULT if pretrained else None
        net = torchvision.models.resnet18(weights=weights)
        feat_dim = net.fc.in_features
        net.fc = nn.Identity()
        feature_layer = "layer4"  # Grad-CAM 目標層
        return net, feat_dim, feature_layer
    if name == "efficientnet_b0":
        weights = torchvision.models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        net = torchvision.models.efficientnet_b0(weights=weights)
        feat_dim = net.classifier[1].in_features
        net.classifier = nn.Identity()
        feature_layer = "features"
        return net, feat_dim, feature_layer
    raise ValueError(f"未知骨幹：{name}")


class RAModel(nn.Module):
    def __init__(self, backbone: str = "resnet18", pretrained: bool = True,
                 head_type: str = "ordinal", num_classes: int = 4):
        super().__init__()
        self.head_type = head_type
        self.num_classes = num_classes
        self.backbone_name = backbone
        self.backbone, feat_dim, self.feature_layer = _build_backbone(backbone, pretrained)

        if head_type == "ordinal":
            out_dim = num_classes - 1          # CORN：K-1 門檻
        elif head_type == "regression":
            out_dim = 1
        else:
            raise ValueError(f"未知 head_type：{head_type}")

        self.head = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(feat_dim, out_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        feats = self.backbone(x)
        return self.head(feats)

    def freeze_backbone(self, freeze: bool = True) -> None:
        """凍結/解凍骨幹（對應 docs/03：先凍結再漸進式微調，避免小樣本過擬合）。"""
        for p in self.backbone.parameters():
            p.requires_grad = not freeze
