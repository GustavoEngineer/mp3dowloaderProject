#!/usr/bin/env python3
"""
Script para generar hash de contraseña de admin
"""

import hashlib
import getpass

def generate_password_hash():
    """Genera un hash SHA-256 de una contraseña"""
    print("=" * 60)
    print("  🔐 GENERADOR DE HASH DE CONTRASEÑA ADMIN")
    print("=" * 60)
    print()
    
    password = getpass.getpass("Ingresa la contraseña de admin: ")
    confirm = getpass.getpass("Confirma la contraseña: ")
    
    if password != confirm:
        print("❌ Las contraseñas no coinciden")
        return
    
    if len(password) < 8:
        print("⚠️  Advertencia: La contraseña es muy corta (mínimo 8 caracteres recomendado)")
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    print()
    print("✅ Hash generado exitosamente:")
    print()
    print(f"ADMIN_PASSWORD_HASH={password_hash}")
    print()
    print("📋 Copia esta línea y agrégala a las variables de entorno en Leapcell:")
    print("   1. Ve al dashboard de Leapcell")
    print("   2. Selecciona tu proyecto")
    print("   3. Ve a 'Settings' → 'Environment Variables'")
    print("   4. Agrega: ADMIN_PASSWORD_HASH = <el hash de arriba>")
    print()
    print("⚠️  IMPORTANTE: No compartas este hash con nadie")
    print()

if __name__ == '__main__':
    generate_password_hash()
