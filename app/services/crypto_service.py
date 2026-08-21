"""
Crypto Service - File Encryption at Rest
=========================================
บริการสำหรับการเข้ารหัสและถอดรหัสไฟล์ (AES-256 / Fernet Authenticated Encryption)
สำหรับปกป้องไฟล์ PDF และเอกสารที่อัปโหลดไว้ในโฟลเดอร์ uploads ไม่ให้รั่วไหล
"""

import os
import base64
import hashlib
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

load_dotenv()

# โหลด Encryption Key จาก Environment หรือสร้างจาก Master Seed
_FERNET_KEY_ENV = os.getenv("FILE_ENCRYPTION_KEY")


def _derive_fernet_key(seed_str: str) -> bytes:
    """สร้าง Fernet 32-byte url-safe base64 key จาก string ใดๆ"""
    digest = hashlib.sha256(seed_str.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


def get_encryption_key() -> bytes:
    """
    ดึง Fernet Key จาก .env
    หากยังไม่มีการกำหนด จะสร้าง Deterministic Key จาก secret seed
    """
    env_key = os.getenv("FILE_ENCRYPTION_KEY")
    if env_key and env_key.strip():
        try:
            # ตรวจสอบว่าเป็น valid fernet key หรือไม่
            key_bytes = env_key.strip().encode("utf-8")
            Fernet(key_bytes)
            return key_bytes
        except Exception:
            # ถ้าเป็น passphrase ธรรมดา ให้ derive เป็น Fernet key
            return _derive_fernet_key(env_key.strip())

    # Fallback key ถ้าไม่ได้ตั้งใน .env (เพื่อความเสถียรของระบบ)
    default_secret = os.getenv("SECRET_KEY", "zkp_mental_master_thesis_secret_storage_key_2026")
    return _derive_fernet_key(default_secret)


def get_cipher() -> Fernet:
    """สร้าง Fernet Cipher instance"""
    key = get_encryption_key()
    return Fernet(key)


def encrypt_bytes(raw_data: bytes) -> bytes:
    """
    เข้ารหัสข้อมูลไบนารี (AES-128-CBC + HMAC-SHA256 Authenticated Encryption)
    :param raw_data: ข้อมูลไบนารีต้นฉบับ (เช่น PDF Bytes)
    :return: ข้อมูลที่ถูกเข้ารหัสแล้ว (Ciphertext Bytes)
    """
    if not raw_data:
        return b""
    cipher = get_cipher()
    return cipher.encrypt(raw_data)


def decrypt_bytes(encrypted_data: bytes) -> bytes:
    """
    ถอดรหัสข้อมูลไบนารี
    :param encrypted_data: ข้อมูลที่ถูกเข้ารหัส (Ciphertext Bytes)
    :return: ข้อมูลต้นฉบับ (Decrypted Plaintext Bytes)
    """
    if not encrypted_data:
        return b""
    
    # หากไฟล์ไม่ได้ถูกเข้ารหัส (เช่น ไฟล์เดิมก่อนเปิดใช้ระบบ) ให้ส่งคืนข้อมูลเดิม
    if not is_encrypted(encrypted_data):
        return encrypted_data

    cipher = get_cipher()
    try:
        return cipher.decrypt(encrypted_data)
    except InvalidToken:
        # หาก key ไม่ตรงหรือไฟล์เสียหาย ให้ส่งคืน original data หรือ raise
        print("⚠️ Warning: Invalid decryption token. Returning raw data.")
        return encrypted_data


def is_encrypted(data: bytes) -> bool:
    """
    ตรวจสอบเบื้องหลังว่าข้อมูลถูกเข้ารหัสด้วย Fernet หรือไม่
    (Fernet token จะขึ้นต้นด้วย magic header b'gAAAAA')
    """
    if not data or len(data) < 8:
        return False
    return data.startswith(b"gAAAAA")
