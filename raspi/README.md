### Processing data

- Create virtual env on Raspberry pi
- Install requirements
- Connect the two Arduinos to the pi (The arduinos should be reading data from the sensors)
- Identify the serial ports on the pi that have been connected to the Arduinos
- Configure the serial ports in `read.py` and `read2.py` accordingly
- Start two separate python process:

  `python read.py`
  
  `python read2.py`
