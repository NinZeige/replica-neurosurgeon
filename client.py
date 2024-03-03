import torch
from torchvision import models, transforms
from PIL import Image

CATOGARY = './imagenet_classes.json'
INPUT_TENSOR = '/tmp/input.tensor'
INPUT_IMG = '/home/ninzeige/Downloads/slot-machine.jpg'

def client_main():
    with Image.open(INPUT_IMG) as img:
        transform = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        input_tensor: torch.Tensor = transform(img)
        input_tensor = input_tensor.unsqueeze(0)

    # prepare with alex
    alex = models.alexnet(pretrained=True)
    alex.eval()

    with torch.no_grad():
        medium: torch.Tensor = alex.features(input_tensor)
        torch.save(medium, INPUT_TENSOR)


if __name__ == '__main__':
    client_main()