#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from myhdl import block, always_comb, Signal, instances

@block
def halfAdder(a, b, soma, carry):
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a & b

    return comb


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]  # (1)

    haList[0] = halfAdder(a, b, s[0], s[1]) 
    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        carry.next = s[1] | s[2]

    return instances()


@block
def adder2bits(x, y, soma, carry):
    c1 = Signal(bool(0))
    fa0 = fullAdder(x[0], y[0], 0, soma[0], c1)
    fa1 = fullAdder(x[1], y[1], c1, soma[1], carry)
    return instances()


@block
def adder(x, y, soma, carry):
    n = len(x)
    c = [Signal(bool(0)) for _ in range(n+1)]
    full_adders = []
    for i in range(n):
        if i == 0:
            full_adders.append(fullAdder(x[i], y[i], 0, soma[i], c[i+1]))
        else:
            full_adders.append(fullAdder(x[i], y[i], c[i], soma[i], c[i+1]))

    @always_comb
    def carry_out():
        carry.next = c[n]

    return instances()
