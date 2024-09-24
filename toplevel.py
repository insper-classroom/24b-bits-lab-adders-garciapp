#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from myhdl import *
from ula_modules import *

from myhdl import block, always_comb, intbv

@block
def bin2hex(hex_display, binary_input):
    @always_comb
    def logic():
        if binary_input == 0:
            hex_display.next = intbv("0111111")  # 0
        elif binary_input == 1:
            hex_display.next = intbv("0000110")  # 1
        elif binary_input == 2:
            hex_display.next = intbv("1011011")  # 2
        elif binary_input == 3:
            hex_display.next = intbv("1001111")  # 3
        elif binary_input == 4:
            hex_display.next = intbv("1100110")  # 4
        elif binary_input == 5:
            hex_display.next = intbv("1101101")  # 5
        elif binary_input == 6:
            hex_display.next = intbv("1111101")  # 6
        elif binary_input == 7:
            hex_display.next = intbv("0000111")  # 7
        elif binary_input == 8:
            hex_display.next = intbv("1111111")  # 8
        elif binary_input == 9:
            hex_display.next = intbv("1101111")  # 9
        elif binary_input == 10:
            hex_display.next = intbv("1110111")  # A
        elif binary_input == 11:
            hex_display.next = intbv("1111100")  # b
        elif binary_input == 12:
            hex_display.next = intbv("0111001")  # C
        elif binary_input == 13:
            hex_display.next = intbv("1011110")  # d
        elif binary_input == 14:
            hex_display.next = intbv("1111001")  # E
        elif binary_input == 15:
            hex_display.next = intbv("1110001")  # F
        else:
            hex_display.next = intbv("0000000")  # Display off for invalid input

    return logic

@block
def toplevel(LEDR, SW, KEY, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, CLOCK_50, RESET_N):
    sw_s = [SW(i) for i in range(10)]
    key_s = [KEY(i) for i in range(4)]
    ledr_s = [Signal(bool(0)) for i in range(10)]
    ledr_bin = Signal(intbv(0)[4:])

    # ---------------------------------------- #
    # ula
    # ---------------------------------------- #
    ic1 = adder(sw_s[0:4], sw_s[6:10], ledr_s[0:4], ledr_s[9])
    ic2 = bin2hex(HEX0, ledr_bin)
    
    @always_comb
    def comb():
        for i in range(len(ledr_s)):
            LEDR[i].next = ledr_s[i]

    return instances()

# Sinais de entrada e saída
LEDR = Signal(intbv(0)[10:])
SW = Signal(intbv(0)[10:])
KEY = Signal(intbv(0)[4:])
HEX0 = Signal(intbv(1)[7:])
HEX1 = Signal(intbv(1)[7:])
HEX2 = Signal(intbv(1)[7:])
HEX3 = Signal(intbv(1)[7:])
HEX4 = Signal(intbv(1)[7:])
HEX5 = Signal(intbv(1)[7:])
CLOCK_50 = Signal(bool())
RESET_N = ResetSignal(0, active=0, isasync=True)

# Instanciando e convertendo para VHDL
top = toplevel(LEDR, SW, KEY, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, CLOCK_50, RESET_N)
top.convert(hdl="VHDL")