import feedparser
import sys
import serial
import time
from datetime import date, datetime

# Variables to hold rss uri and latest story
newsfeed = ''
latest = ''

# Configure Pi serial port
s = serial.Serial()
s.baudrate = 9600
s.timeout = 10
s.port = "/dev/serial0"

try:
    # Open serial port
    s.open()
except serial.SerialException, e:
    # There was an error
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)

# Clear display
s.write("$$$ALL,OFF\r")  



while True:    
    
  # Send date message to the Pi-Lite
  today = date.today()
  datemessage = today.strftime("%d-%m-%Y")
  s.write(datemessage + '\r')

  # Short delay to allow the message to finish
  time.sleep(8)

  # Send time message to the Pi-Lite
  now = datetime.now()
  timemessage = now.strftime("%H:%M")
  s.write(timemessage + '\r')

  # Short delay
  time.sleep(8)

  # Get the latest posts from BBC UK News
  newsfeed = feedparser.parse("http://feeds.bbci.co.uk/news/uk/rss.xml#")
  # Retrieve just the latest post
  entry = newsfeed.entries[0]
  # Get the title and convert to non-unicode
  title = (entry.title)
  title = title.encode('latin-1')

  # If the title of the latest post has changed, scroll it twice and then update the latest variable
  while title != latest:
      i = 0
      while i < 2:
          s.write (title + '\r')
          time.sleep (30)
          i += 1
      latest = title
