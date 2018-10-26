#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys

class Manager:
    
    # Indexes list
    idx_name = ["crypto", "raw_material", "stock_exchange", "forex"]

    def __init__(self): # Constructor

        # Default evaluation environment
        self.nb_index = 360 # Nb indexes before exiting
        self.clock = 0.05 # in seconds

        if (self.CheckArgv() is False):
            return
        self.idx_list = dict() # key: marketplace - values: index list
        self.run = True
        self.fifo = None
        self.Launch()

    def CheckArgv(self):
        if (len(sys.argv) == 3):
            try:
                self.clock = float(sys.argv[1])
                self.nb_index = int(sys.argv[2])
            except ValueError:
                print("usage: ./main.py CLOCK NB_INDEX")
                return False
        elif (len(sys.argv) != 1):
            print("usage: ./main.py CLOCK NB_INDEX")
            return False
        return True

    def GetDatas(self):
        for marketplace in self.idx_name:
            try:
                with open("./indexes/" + marketplace + ".txt", "r") as f:
                    for item in f:
                        self.idx_list[marketplace].append(''.join(item.splitlines()))
            except ValueError:
                pass
            except:
                print("Can't open and read file")
                raise

    def Push(self):
        i = 0
        while self.run:

            # Check the end
            if i >= self.nb_index - 1:
                self.run = False

            # Open DB like file
            self.fifo = open("./.index.db", "w")

            # Foreach marketplace, push current value
            for key, value in self.idx_list.items():
                self.SendIndexToServer(key, self.idx_list[key][i])

            # Close DB like file
            self.fifo.close()

            # Flush stdout
            sys.stdout.flush()

            # Delta time between 2 pushes
            time.sleep(self.clock)
            i += 1

    def SendIndexToServer(self, marketplace ,value):
        sys.stdout.write(marketplace + ":" + str(value) + "\n")
        tmp_str = marketplace + ":" + str(value) + "\n"
        self.fifo.write(tmp_str) # Write into DB like file

    def InitDatas(self):
        for marketplace in self.idx_name:
            self.idx_list[marketplace] = list()        
    
    def Launch(self):
        self.InitDatas()
        self.GetDatas()
        self.Push()
