import torch 
########################################################################################
from transformers import BertForSequenceClassification 
from transformers import BertTokenizerFast
    
def load_bert_model():
    num_labels = 2
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-multilingual-cased",
        num_labels=num_labels
    )
    model.load_state_dict(torch.load("inference/models/best_bert.pth"))

    return model

def load_bert_tokenizer():
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-multilingual-cased')

    return tokenizer
########################################################################################
from torchvision.models.vgg import vgg16
import torch.nn as nn
import torchvision.transforms as transforms 

def load_vgg16_model():
    model = vgg16(weights='IMAGENET1K_V1')

    myclassifier = nn.Sequential(
        nn.Linear(in_features=25088, out_features=4096, bias=True),
        nn.ReLU(),
        nn.Dropout(),
        nn.Linear(in_features=4096, out_features=4096, bias=True),
        nn.ReLU(),
        nn.Linear(in_features=4096, out_features=3, bias=True)
    )

    model.classifier = myclassifier

    model.load_state_dict(torch.load("inference/models/celebrity.pth"))

    return model

########################################################################################
# 변수 
bert_model = load_bert_model()
tokenizer = load_bert_tokenizer()

data_transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ]
)
vgg16_model = load_vgg16_model()