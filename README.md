# Build myPunctuator as a python's cpp extension

## Installation
```shell
# clone this repository
git clone https://github.com/Chaotic-chaos/my_punctuator_cpp.git

# perpare a environment
python -m vnev venv # or whatever ways u'd like

# move into thr right directory
cd punctuator_installer/

# start the building and installation
python setup.py install
```

## Usage

### Initiate the module
```python
import punctuator

model = punctuator()
```

### Setup the model
```python
model = model.setup_model("path/to/model.pth")
```

### Inference && Decode
```python
res = model.decode("<string of the word_ids>")

# maximum snetence length is 512
```

> For more details please refer to [use_sample.py](punctuator_installer/src/use_sample/use_sample.py)

## Reference
- [wenet](https://github.com/wenet-e2e/wenet/tree/main/runtime/binding/python)
- [pybind](https://github.com/pybind/pybind11)
...

## Tech details
- refer to [blog]()