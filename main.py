# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 18:35:03 2024

@author: Administrator
"""

import Sutrcture

if __name__== "__main__":
    c60_file_path='C60.csv'
    Sutrcture.LinearStructure(c60_file_path)
    Sutrcture.ZigzagStructure(c60_file_path)
    Sutrcture.HelixStructure(c60_file_path)