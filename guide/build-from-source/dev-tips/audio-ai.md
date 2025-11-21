# Audio AI

## Adding an AI model

To add an AI model, there's two requirements:
 - Provide a definition of the model
 - Provide the weights of the model

### Defining the model

Add a python file in _assets/models_, with the name corresponding to your model's.
The formatting is as follows: **<model_name>\.py**.
For instance, if your model's name is "CRNN L2", then you'll have the file _CRNN L2.py_.
The file must define a callable named **ModelBuilder**, returning a new instance of the model.
When instantiating the model, this callable will be used.

::: info
As of now, only PyTorch is supported, meaning all inputs to the model will be classes of
PyTorch.
:::

### Providing the weights
Following the same conventions as [previously](#defining-the-model), your file must be placed
in _assets/models_, for the filename, it should be formatted as **<model_name>\.pt**.
