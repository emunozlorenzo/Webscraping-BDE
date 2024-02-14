def obtener_primer_valor(diccionario):
    if diccionario:
        primer_clave = next(iter(diccionario))
        primer_valor = diccionario[primer_clave]
        return primer_valor
    else:
        return None
    
diccionario = {
    "clave1": ["valor1", "valor2", "valor3"],
    "clave2": ["valor4", "valor5", "valor6"],
    "clave3": ["valor7", "valor8", "valor9"]
}

print(obtener_primer_valor(diccionario)) # ['valor1', 'valor2', 'valor3']