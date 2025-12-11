#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 13:07:42 2025

@author: adrian
"""
import sympy as sp


def traducir_expresion(expr):
    if not isinstance(expr, str):
        expr = str(expr)

    expr = expr.lower()

    reemplazos = {
        "^": "**",
        "sen": "sin",
        "ln": "log",
        "√": "sqrt",
        
    }

    for a, b in reemplazos.items():
        expr = expr.replace(a, b)

    return sp.sympify(expr, locals={"e": sp.E})
