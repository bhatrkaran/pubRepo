from scapy.all import *
import requests
import time
ORDER_PIZZA_EVENT = 'http://maker.ifttt.com/trigger/orderpizza/with/key/<IFTTT KEY>'
WEMO_EVENT = 'http://maker.ifttt.com/trigger/wemo_event/with/key/<IFTTT KEY>'
PLAYSONGS_EVENT = 'http://maker.ifttt.com/trigger/playsongs/with/key/<IFTTT KEY>'

def doParty_press():  # future extension to setup party event
  data = {
    "value1": 'smooth', 
    "value2": time.strftime("%Y-%m-%d %H:%M")
  }
  requests.post(PLAYSONGS_EVENT, data)
  requests.post(WEMO_EVENT, data)
  
def bounty_button_pressed():
  data = {
    "Timestamp": time.strftime("%Y-%m-%d %H:%M"), 
    "Descripton": 'bounty_button_pressed'
  }
  requests.post(WEMO_EVENT, data)
  print time.strftime("%Y-%m-%d %H:%M")
  
def maxwell_button_pressed():
  data = {
    "Timestamp": time.strftime("%Y-%m-%d %H:%M"), 
    "Descripton": 'maxwell_button_pressed'
  }
  requests.post(ORDER_PIZZA_EVENT, data)
  print time.strftime("%Y-%m-%d %H:%M")
  
def arp_display(pkt):
  timestamp = time.strftime("%Y-%m-%d %H:%M")
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc == '10:ae:60:e0:9d:4f': # bounty MAC        
        print "Pushed Bounty"
        bounty_button_pressed()
      elif pkt[ARP].hwsrc == '74:c2:46:1a:03:40': # maxwell MAC
        print "Pushed maxwell"
        maxwell_button_pressed()
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=0)
