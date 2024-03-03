import torch
from networks import AlexNet
from torchvision import transforms
from PIL import Image
import json
from utils import nprofile

DOG_PATH = '/home/ninzeige/Downloads/Domestic_Goose.jpg'
SIZE_DUMP = 'size.json'

def main():
    with open('imagenet_classes.json', 'r') as f:
        in_table = json.load(f)
    lookup = lambda x: [in_table[f'{index}'] for index in x]

    # 定义图像预处理
    transform = transforms.Compose(
        [
            transforms.Resize(256),  # 将图像大小调整为256x256
            transforms.CenterCrop(224),  # 从中心裁剪224x224大小的图像
            transforms.ToTensor(),  # 将图像转换为Tensor
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),  # 标准化
        ]
    )

    with Image.open(DOG_PATH) as dog:
        image: torch.Tensor = transform(dog)
        image = image.unsqueeze(0)
        falex = AlexNet.flatten_alex()

        output = nprofile.profile_flatten(falex, image, 'alex')

        _, indices = torch.topk(output, 5)
        print(f"Top 5 predicated classes: {lookup(indices[0])}")


main()