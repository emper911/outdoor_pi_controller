# outdoor_pi_controller
A webapp written using flask to control a raspberry pi outdoors using relays, powered by a solar panel connected to a lithium battery.
The webapp allows shared state across multiple clients and updates to changes through event-stream.

As my summer project I am continuing on with my autogarden project with a fresh perspective from the original project.
This project is to create a isolated system dependent on just a solar panel for energy.

The panel is a 100W 12V panel connected to a lithium polymer ion battery with a capacity of 48000mAh.

The outputs to the system so far consist of a 24W LED outdoor lights, 4W water pump and one miscellaneous output pin.

Future plans are to provide further control over water pump scheduling as well as lights if desirable.

For inputs, sensors such as a distance sensor to measure water levels in the bucket reservoir would a good first step. 
Later ideas include soil moisture sensors to automate water delivery, ph Sensor and ppm sensor to regulate nutrient delivery.

For later stages, once garden is at a point of being able to sucessfully grow and harvest, consider building a solar heater system
controllable by the raspberry pi as well. 

Other things to consider are connecting other micro controllers over bluetooth and add further metrics to monitor in real time.
