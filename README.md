# Video-streamer
------
------

Key | Value
------------ | -------------
Name | Video Streamer
Acronym | VS
Use case | Self-optimization (SO)
Instantiation | Physical Network Function (PNF)
Type | Service
Scope  | Video Flows
Management Protocol | Advanced Message Queuing Protocol (AMQP) messages

------
# Description

The Video Streamer is a component  working as a Physical Network Function (PNF) which is used in the Self-Optimizing use case [3.4](https://github.com/Selfnet-5G/WP3_SO/blob/master/Doku/D3.4/D3.4_master.pdf) . Its main function is to stream scalable H.265 video flows (SHVC) through the network. This component is also in charge to send control messages to the client in order to let it know when start, stop or close the video-player reproduction.

------
# Interfaces
There is a control interface based on Advanced Message Queuing Protocol (AMQP) for sending control/manage messages to the video-player.
There is also an interface in charge to streaming video to the network datapath.

![VS interfaces](https://github.com/Selfnet-5G/video-streamer/blob/master/resources/vs_1.png?raw=true)



# Installation 
Following commands will install all required dependencies by the video-stremaer. This component is able to work just over Linux SO.

### Dependencies

```sh
$sudo apt-get install python2.7 python2.7-dev -y
```

```sh
$pip install kombu
```
```sh
# installing OpenHEVC
if [ ! -d "./openHEVC" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  git clone git://github.com/OpenHEVC/openHEVC.git
  cd openHEVC
  git checkout hevc_rext
  mkdir build
  cd build
  cmake -DCMAKE_BUILD_TYPE=RELEASE ..
  make
  make install
  cd ..
  cd ..
 else
 	echo "openHEVC is already installed"
fi


# installing GPAC
if [ ! -d "./gpac" ]; then
    # Control will enter here if $DIRECTORY doesn't exist.
    git clone https://github.com/gpac/gpac
    cd gpac
    git checkout tags/v0.6.1
    ./configure
    make
    make install
    cd ..
else
	echo "gpac is already installed"
fi

```


### Configuration
The first step to start using the VS is to create a proper configuration file. The following table shows all required parameters .

##### _ config.ini file _
| Parameter | Meaning |
| ------ | ------ |
| Exchange | Exchange used by this video-streamer for publishing control messages to the video-client |
| RoutingKey | Routing key which is used by this video-streamer for publishing control messages to the video-client|
| Rabbit-server-ip | The IP address where the rabbitMQ server is located |
| Vhost | Virtual Host of the rabbitMQ server (If there is not a Virtual Host defined, "/" should be added here) |
| User | User name of the rabbitMQ server |
| MP4File | The video to be streamed. it should be in this same folder |
| Player_ip | The IP address where the video-player is located |

# Usage
```
usage: streamer.py [-h] [-v] [--start] [--startfs] [--stop] [--close] [-m MTU]

video flow streamer

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      show program's version number and exit
  --start            Starts streaming
  --startfs          Starts streaming in full screen mode
  --stop             Stops both video-player and video-streamer
  --close            Stops both video-player and video-streamer and also
                     closes the video-player's daemon
  -m MTU, --mtu MTU  Configures the Maximum Transmision Unit (MTU). Default
                     value is 1200
```

# Usage Example
   Example of starting streaming with a 1500 mtu:
    ```
    $ python2.7 streamer.py --start -mtu 1500
    ```
    Example of starting streaming in full screen with a 1500 mtu:
    ```
     $ python2.7 streamer.py --startfs -mtu 1500
    ```
   Example of starting streaming in full screen with a 1200 default value of mtu:
    ```
    $ python2.7 streamer.py --startfs
    ```
------
# License
### Authors
5G Video-Streamer. Copyright (C) 01/03/17 Pablo Salva Garcia, Qi wang, Jose M. Alcaraz Calero, James Nightingale. University of the West of Scotland
  

### License
Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
  