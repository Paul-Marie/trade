#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Extern
import sys
import string
import signal

# Intern
from GroupData import GroupData
from StatusCode import StatusCode

class Server:

    # Commands
    cmd_definition =  {
        "HELP": "display available commands",
        "BUY:X:Y": "buy X shares in Y marketplace",
        "SELL:X:Y": "sell X shares in Y marketplace",
        "STATS": "display group statistics",
        "EXIT": "leave program"
    }

    marketplace_list = ["crypto", "raw_material", "stock_exchange", "forex"]
    
    def __init__(self): # Constructor
        # signal.signal(signal.SIGINT, self.SignalHandler)
        self.arg_x = 0
        self.arg_y = None
        self.data = GroupData()
        self.run = True
        self.Command()
        
    # Shell function : exit
    def exit_func(this, user_input):
        this.data.FullDump()
        this.run = False

    # Shell function : help
    def help_func(this, user_input):
        for key, value in this.cmd_definition.items():
            print(key + " -> " + value)
            
    # Shell function : buy
    def buy_func(this, user_input):
        if (this.error_management(user_input) == False):
            return
        this.data.Buy(this.arg_x, this.arg_y)

    # Shell function : sell
    def sell_func(this, user_input):
        if (this.error_management(user_input) == False):
            return
        this.data.Sell(this.arg_x, this.arg_y)
        
    # Shell function : stats
    def stats_func(this, user_input):
        this.data.Dump()

    # Buy / sell error management
    def error_management(self, user_input):
        input_list = user_input.split(':')

        # Check nb_args
        if (len(input_list) != 3):
            print(StatusCode.failure.get(403))
            return False

        # First argument is an int ?
        try :
            self.arg_x = int(input_list[1])
            self.arg_y = input_list[2]
        except (TypeError, ValueError) as e:
            print(StatusCode.failure.get(401))
            return False

        # Marketplace exists ?
        if any(self.arg_y in s for s in self.marketplace_list) is False:
            print(StatusCode.failure.get(404))
            return False

    # After each command dump user data in an external file
    def WriteLog(self):
        self.fifo = open("../server/.server.log", "w")
        self.data.WriteLogStats(self.fifo)
        self.fifo.close()
    
    cmd_list = {
        'EXIT': exit_func,
        'HELP': help_func,
        'BUY': buy_func,
        'SELL': sell_func,
        'STATS': stats_func
    }

    # Shell like to administrate
    def Command(self):
        while self.run:
            user_input = sys.stdin.readline()
            user_input = ' '.join(user_input.split())            
            for key, value in self.cmd_list.items():
                if (user_input.split(':')[0] == key):
                    value(self, user_input)
                    self.WriteLog()

    # Disable CTRL+C
    def SignalHandler(self, signal, frame):
        print("type \"EXIT\" to leave")
