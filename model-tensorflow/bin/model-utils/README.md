# Model-Utils

A utility tool to handle model lifecycle as part of the fruitifyMe project.  
![lifecycle](../../../readme/FruitifyMe-Model%20lifecycle.png)

## Installation:

Change directory to `model-tensorflow/bin/model-utils` then type

```sh
pip install .
```

## Usage:

```sh
mutils <command> [options]
```

## Available operations:

To get a full list of the available operations/commands, type

```sh
mutils --help
```

The following operations are available:

- init
- train
- test
- clear
- promote
- deploy
- exists

for more information about a command, type

```sh
mutils <command> --help
```

for example, the `train` command has the following options

```sh
mutils train --help
```

```
Usage: mutils train [OPTIONS] TRAINING_SCRIPT

  Train a model using a training script.

Options:
  -b, --batch-size INTEGER  Training batch size.  [default: 64]
  -h, --img-height INTEGER  Images resized height.  [default: 100]
  -w, --img-width INTEGER   Images resized width.  [default: 100]
  -e, --epochs INTEGER      Number of training epochs.  [default: 5]
  -t, --tag TEXT            Tag the model that will be shown in its file name.
  --help                    Show this message and exit.
```
