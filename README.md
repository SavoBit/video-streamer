# Video-streamer

# Configuration (config.ini)

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
