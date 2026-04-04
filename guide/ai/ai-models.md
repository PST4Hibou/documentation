# AI Models

We experienced a lot of different models during our research and development phase. We have tested and used many of them, but we have selected the ones that we found the most useful for our use case.
We selected only 2 models that we are currently using in production.

| Name          | Description                                                                               |
|---------------|-------------------------------------------------------------------------------------------|
| Custom Resnet | Detect very well the drones, but too many FP                                              |
| ViT           | Transformers architecture, Detect well the drones, but not as good as Resnet, but less FP |

## AI Developpment

To develop train the AI models we used our computer and the jupyter notebooks at https://jupyter.esiea.fr

You should ask the Jupyter administrator to give you access to more GPU, RAM and CPU.

The models weights files are stored in a hugging face repository : https://huggingface.co/Hibou-Foundation/audio-models/tree/main