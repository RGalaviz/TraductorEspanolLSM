import torch
# import our library
import torchmetrics
preds = ['martes gustar bailar']
target = [['todos martes yo bailar gustar']]
ter = torchmetrics.TranslationEditRate()
print(ter(preds, target))