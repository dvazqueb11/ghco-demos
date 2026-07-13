#!/usr/bin/env python3
"""
Demo 1 Companion - Product Service (codigo sin optimizar)
Usage: Copiar este archivo al proyecto de demo antes de la sesion.
Prerequisites: Python 3.11+
"""

# Este es el archivo que se usa en Demo 1 para mostrar
# como Copilot Chat e Inline Chat mejoran codigo existente.
# Intencionalmente tiene problemas de calidad para que
# Copilot los identifique y corrija.

import json

products_db = {}
order_counter = 0

def process_order(product_id, quantity, customer_name, discount_code):
    global order_counter
    # validar producto
    if product_id not in products_db:
        return {"error": "producto no encontrado"}
    p = products_db[product_id]
    if p["stock"] < quantity:
        return {"error": "stock insuficiente"}
    if quantity <= 0:
        return {"error": "cantidad invalida"}
    # calcular precio
    price = p["price"] * quantity
    if discount_code == "VIP10":
        price = price * 0.9
    elif discount_code == "VIP20":
        price = price * 0.8
    elif discount_code == "EMPLOYEE":
        price = price * 0.7
    # actualizar stock
    p["stock"] = p["stock"] - quantity
    order_counter = order_counter + 1
    order = {
        "id": order_counter,
        "product": product_id,
        "quantity": quantity,
        "customer": customer_name,
        "total": price,
        "status": "completed"
    }
    return order


def add_product(name, price, stock, category):
    id = len(products_db) + 1
    products_db[id] = {
        "name": name,
        "price": price,
        "stock": stock,
        "category": category
    }
    return id


def get_products(category=None):
    result = []
    for id in products_db:
        p = products_db[id]
        if category is None or p["category"] == category:
            result.append({"id": id, **p})
    return result


def calculate_stats():
    total_products = len(products_db)
    total_stock = 0
    total_value = 0
    categories = {}
    for id in products_db:
        p = products_db[id]
        total_stock = total_stock + p["stock"]
        total_value = total_value + (p["price"] * p["stock"])
        if p["category"] not in categories:
            categories[p["category"]] = 0
        categories[p["category"]] = categories[p["category"]] + 1
    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "total_value": total_value,
        "categories": categories
    }
