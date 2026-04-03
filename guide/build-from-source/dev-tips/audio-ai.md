# Audio AI

## Adding an AI model

To add an AI model, there's two requirements:
 - Provide a definition of the model
 - Provide the weights of the model

### Defining the model

Create a directory in _assets/audio_models_ with the name of your model. Inside this directory, you must have 2 files :
- model.py : This file contains the definition of your model and the processing of the data
- model.pt : This file contains the weights of your model, in the format of a PyTorch state dict.

::: warning
As of now, only PyTorch is supported, meaning all inputs to the model will be classes of
PyTorch.
:::