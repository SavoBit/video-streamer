#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=======================================================================================================================
#
#          FILE:  streamer.py
#
#         USAGE:  ./streamer  [--start] [--stop] [--close]
#
#   DESCRIPTION: This sowftware should be installed at the streamer (server) side in order to start/stop the video streaming.
#                It needs some dependences described at requeriments.
#
#       OPTIONS:  --start sends the mp4 video to a specific ip address and publishes start_stream in rabbitmq
#                 --stop stops streaming and publish stop_stream message to a rabbitmq
#
#  REQUIREMENTS:  kombu 4.0.1, pika 0.9.4 , gpac branch v0.6.1
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Pablo Salva Garcia
#       COMPANY:  UWS
#       VERSION:  1.0
#       CREATED:  08/08/2017
#      REVISION:  ---
#=======================================================================================================================

import sys, getopt, os
from kombu import BrokerConnection, Exchange, Queue, Producer, Connection
import time
import json
import ConfigParser
from argparse import ArgumentParser
#from Configparser import ConfigParser

def value_from_section(section):
    dict1 = {}
    options = parser.options(section)
    for option in options:
        try:
            dict1[option] = parser.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

# Constants from config.ini file wich has been produced by configure.sh
if not os.path.exists('config.ini'):
    print "Error - Please, run configure.sh script before to start this streamer"
    exit()

# configuration
parser = ConfigParser.ConfigParser()
parser.read('config.ini')

# Paramters of the rabbitMQ server
rabbit_host=value_from_section('Streamer')['rabbit_server_ip']
rabbit_vhost=value_from_section('Streamer')['vhost']
rabbit_user=value_from_section('Streamer')['user']
rabbit_password=value_from_section('Streamer')['password']

# Parameters where the stramer will publish messages
rabbit_exchange= value_from_section('Streamer')['exchange']
rabbit_routingkey=value_from_section('Streamer')['routingkey']

# Local parameters
video_stream=value_from_section('Streamer')['mp4file']
player_ip=value_from_section('Streamer')['player_ip']

# Available commands:
start_json = {"command":"start", "data":"session.sdp"}
startfs_json = {"command":"startfs", "data":"session.sdp"}
stop_json = {"command":"stop", "data":""}
close_json = {"command":"close", "data":""}

def main(argv):
    argp = ArgumentParser(version='1.0', description='video flow streamer', epilog='Pablo Salva Garcia (UWS)')
    argp.add_argument('--start', action="store_true", help='Starts streaming')
    argp.add_argument('--startfs', action="store_true", help='Starts streaming in full screen mode')
    argp.add_argument('--stop', action="store_true", help='Stops both video-player and video-streamer')
    argp.add_argument('--close', action="store_true", help='Stops both video-player and video-streamer and also closes the video-player\'s daemon')
    argp.add_argument('-m', '--mtu', help='Configures the Maximum Transmision Unit (MTU). Default value is 1200')
    argp.add_argument('-l', '--loop', nargs='?', const=True, type=bool, help='The video will be streamed in a loop')
    arguments = argp.parse_args()

	  # (--start) Start streaming
    if arguments.start:
        mtu = arguments.mtu if arguments.mtu else 1200
        loop = True if arguments.loop else False
        start(mtu=mtu, loop=loop)

    # (--startfs) Start streaming in full screen
    if arguments.startfs:
        mtu = arguments.mtu if arguments.mtu else 1200
        loop = True if arguments.loop else False
        startfs(mtu=mtu, loop=loop)

    # (--stop) Stop streaming
    if arguments.stop:
      stop()

    # (--close) Close streaming (Both, streamer and player)
    if arguments.close:
      close()

def publish(start=False, startfs=False, stop=False, close=False):
    body = json.dumps(close_json)
    if start == True:
      body = json.dumps(start_json)
    elif stop == True:
      body = json.dumps(stop_json)
    elif startfs == True:
      body = json.dumps(startfs_json)

    conn = BrokerConnection(hostname=rabbit_host, port=5672, userid=rabbit_user, password=rabbit_password, virtual_host=rabbit_vhost, heartbeat=4)
    channel = conn.channel()

    exchange = Exchange(rabbit_exchange, type='topic', durable=False)
    producer = Producer(exchange=exchange, channel=channel, routing_key=rabbit_routingkey)

    producer.publish(body)

def start(mtu=1200, loop=False):
    print "Starting stream with MTU: {0} >>>".format(mtu)
    publish(start=True)
    time.sleep(2)
    os.system("MP4Box -rtp -dst={0} -port=9099 -mtu={1} {2} {3}".format(player_ip, mtu, video_stream, '-noloop' if loop==False else ''))

def startfs(mtu=1200, loop=False):
    print "Starting stream in full screen with MTU: {0} >>>".format(mtu)
    publish(startfs=True)
    time.sleep(2)
    os.system("MP4Box -rtp -dst={0} -port=9099 -mtu={1} {2} {3}".format(player_ip, mtu, video_stream, '-noloop' if loop==False else ''))

def stop():
    print "Stop stream ....."
    publish(stop=True)
    os.system("sudo pkill MP4Box")

def close():
    print "Clossing streamer and player remotely ....."
    os.system("sudo pkill MP4Box")
    publish(close=True)


if __name__ == "__main__":
    main(sys.argv[1:])
