# XM API
This is the API XM will provide to the clients. Basically there is the main route that returns all the available functions. To call a function just append the name of the desidered synapse to the main route and pass parameters as query string.

## Install and Run
First of all you have to install [Espeak](#Espeak) and [MJPG-Streamer](#MJPG-Streamer), then just do:

```bash
sudo pip3 install -r requirements.txt
sudo ./runapi.sh
```


## Design
The entire system is designed to be similar to the human body. In fact each module is named as a part of the human body.

XM is composed by 5 parts:
- **Leg** that communicates with the motors using the protocol defined in the arduino folder;
- **Mouth** that makes the rover speak, using *espeak* as backend;
- **Eyes** that allows to stream from a given webcam, uses *mjpg-streamer* as backend;
- **Body** is inside the brain module and it's just a container for all the parts of the body;
- **Brain** is the core part of the API, because it's the glue between input and the body;
- **Hear** is just a tiny wrapper around Brain built to be more similar to the human body.

For more informations about what each module do, read the documentation in the file!

#### <a name="Espeak"></a>Espeak
[Espeak](http://espeak.sourceforge.net/) is an opensource speech synthesizer that is used as the default backend of Mouth module. It's available in most Linux distribution so it's should be as easy as install it with the package manager.

E.g. in Debian(Raspian)
```bash
sudo apt-get install espeak
```

#### <a name="MJPG-Streamer"></a> MJPG-Streamer
[MJPG-Streamer](http://sourceforge.net/projects/mjpg-streamer/) is the default backend for streaming, because it's easy to use and quite efficient. To install it just
```bash
sudo ./install_motion-jpeg.sh
```
and it should be fine.
