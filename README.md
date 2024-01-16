### Mirror (Molex AI Model)
```markdown

This project is a Python application that simulates and predicts user interactions with the system. It records and uses mouse and keyboard actions, and also includes screen interactions.

Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites

You need to have Python installed on your machine. The project also uses the following Python libraries:

- numpy
- pandas
- pymongo
- pyautogui
- pynput
- logging
- threading
- string
- uuid
- random
```
```markdown
You can install these using pip:

pip install numpy pandas pymongo pyautogui pynput logging threading string uuid random
```

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/MichaelTheChef/mirror.git
```

Navigate to the project directory:

```bash
cd mirror
```

## Usage

The project consists of several modules:

- `mouse.py`: This module records and uses mouse actions. For example, it can record the time and coordinates of mouse clicks and then use this data to simulate mouse movements and clicks.

```python
from mirror.model.mouse import Mouse

# Start recording mouse actions for 10 seconds
mouse = Mouse(seconds=10)
```

- `record.py`: This module saves and reads the recorded data. It can save the data to a MongoDB database or a CSV file, and it can read the data from a MongoDB database, a CSV file, or a pandas DataFrame.

```python
from mirror.model.record import Record
from mirror.model.mouse import Mouse

# Record mouse data for 10 seconds
mouse = Mouse(seconds=10)

# Save the recorded data to a CSV file
record = Record()
file_id = record.save_data(mouse.read_data(), to_csv=True)
print(f"Data saved to {file_id}.csv")
```

- `train.py`: This module trains the model with random data or sample data and makes predictions. It can train the model to predict keyboard actions, mouse left clicks, mouse right clicks, and screen interactions.

```python
from mirror.training.train import Train

# Train the model with random data
train = Train()
train.train(size=1000, action="mouse-left")
```

- `screen.py`: This module records and uses screen interactions. It can record the time and coordinates of mouse movements and then use this data to simulate mouse movements.

```python
from mirror.model.screen import Screen

# Start recording screen interactions for 10 seconds
screen = Screen(seconds=10)
```

## Built With

* [Python](https://www.python.org/) - The programming language used
* [PyMongo](https://pymongo.readthedocs.io/en/stable/) - Python driver for MongoDB
* [Pandas](https://pandas.pydata.org/) - Data analysis and manipulation tool
* [Numpy](https://numpy.org/) - The fundamental package for scientific computing with Python
* [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) - A Python module for programmatically controlling the mouse and keyboard.
* [Pynput](https://pynput.readthedocs.io/en/latest/) - This library allows you to control and monitor input devices.

## Authors

* **MichaelTheChef** - *Initial work* - [MichaelTheChef](https://github.com/MichaelTheChef)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
