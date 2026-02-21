import os
import json
import asyncio
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse

from app.routers.report import compare

from app.routers.caesar_key import generate_key as caesar_generate_key
from app.routers.caesar_encrypt import caesar_encrypt
from app.routers.caesar_decrypt import caesar_decrypt
from app.routers.caesar_attack import caesar_attack

from app.routers.permute_key import generate_key as permute_generate_key
from app.routers.permute_encrypt import encrypt as permute_encrypt
from app.routers.permute_decrypt import decrypt as permute_decrypt
from app.routers.permute_attack import frequency_attack

from app.routers.vigenere_key import generate_key as vigenere_generate_key
from app.routers.vigenere_encrypt import encrypt as vigenere_encrypt
from app.routers.vigenere_decrypt import decrypt as vigenere_decrypt
from app.routers.vigenere_attack import vigenere_attack

from app.routers.playfair_key import generate_key as playfair_generate_key
from app.routers.playfair_encrypt import encrypt as playfair_encrypt
from app.routers.playfair_decrypt import decrypt as playfair_decrypt

from app.routers.hill_key import generate_key as hill_generate_key
from app.routers.hill_encrypt import encrypt as hill_encrypt
from app.routers.hill_decrypt import decrypt as hill_decrypt
from app.routers.hill_attack import hill_attack

from app.routers.des_key import generate_key as des_generate_key
from app.routers.des_encrypt import encrypt as des_encrypt
from app.routers.des_decrypt import decrypt as des_decrypt


router = APIRouter()


# Helper
async def read_file(file: UploadFile) -> str:
    raw = await file.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace")


def get_name(file: UploadFile) -> str:
    name = file.filename or "file"
    return name.rsplit(".", 1)[0] if "." in name else name


# Root
@router.get("/")
async def root():
    return {"status": "ok", "message": "Cipher API"}


# Favicon
@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    return FileResponse(path)


# Health
@router.get("/health")
async def health_check():
    return {"status": "ok"}


# Report
@router.post("/report")
async def caesar_report_route(
    original: UploadFile = File(...),
    recovered: UploadFile = File(...),
):
    original_text = await read_file(original)
    recovered_text = await read_file(recovered)
    report = compare(original_text, recovered_text)

    name = get_name(original)
    recovered_name = (recovered.filename or "").upper()
    algo_suffixes = ["_CC_", "_PC_", "_VC_", "_PFC_", "_HC_", "_DC_"]
    suffix = next((s.strip("_") for s in algo_suffixes if s in recovered_name), "")
    report_name = f"{name}_{suffix}_Report.txt" if suffix else f"{name}_Report.txt"
    return PlainTextResponse(
        content=report,
        headers={
            "Content-Disposition": f'attachment; filename="{report_name}"'
        },
    )


# Caesar Key
@router.get("/caesar/key", tags=["caesar"])
async def caesar_key_route():
    return {"key": caesar_generate_key()}


# Caesar Encryption
@router.post("/caesar/encrypt", tags=["caesar"])
async def caesar_encrypt_route(file: UploadFile = File(...), key: int = Form(...)):
    content = await read_file(file)
    encrypted = caesar_encrypt(content, key)
    return JSONResponse(content=encrypted)


# Caesar Decryption
@router.post("/caesar/decrypt", tags=["caesar"])
async def caesar_decrypt_route(file: UploadFile = File(...), key: int = Form(...)):
    content = await read_file(file)
    decrypted = caesar_decrypt(content, key)
    return JSONResponse(content=decrypted)


# Caesar Attack
@router.post("/caesar/attack", tags=["caesar"])
async def caesar_attack_route(file: UploadFile = File(...)):
    content = await read_file(file)
    result = caesar_attack(content)
    return JSONResponse(content=result)


# Permutation Key
@router.get("/permute/key", tags=["permute"])
async def permute_key_route():
    return {"key": permute_generate_key()}


# Permutation Encryption
@router.post("/permute/encrypt", tags=["permute"])
async def permute_encrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    encrypted = permute_encrypt(content, key)
    return JSONResponse(content=encrypted)


# Permutation Decryption
@router.post("/permute/decrypt", tags=["permute"])
async def permute_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    decrypted = permute_decrypt(content, key)
    return JSONResponse(content=decrypted)


# Permutation Attack
@router.post("/permute/attack", tags=["permute"])
async def permute_attack_route(file: UploadFile = File(...)):
    content = await read_file(file)
    result = await asyncio.get_running_loop().run_in_executor(
        None, frequency_attack, content
    )
    return JSONResponse(content=result)


# Vigenere Key
@router.get("/vigenere/key", tags=["vigenere"])
async def vigenere_key_route():
    return {"key": vigenere_generate_key()}


# Vigenere Encryption
@router.post("/vigenere/encrypt", tags=["vigenere"])
async def vigenere_encrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    encrypted = vigenere_encrypt(content, key)
    return JSONResponse(content=encrypted)


# Vigenere Decryption
@router.post("/vigenere/decrypt", tags=["vigenere"])
async def vigenere_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    decrypted = vigenere_decrypt(content, key)
    return JSONResponse(content=decrypted)


# Vigenere Attack
@router.post("/vigenere/attack", tags=["vigenere"])
async def vigenere_attack_route(file: UploadFile = File(...)):
    content = await read_file(file)
    result = await asyncio.get_running_loop().run_in_executor(
        None, vigenere_attack, content
    )
    return JSONResponse(content=result)


# Playfair Key
@router.get("/playfair/key", tags=["playfair"])
async def playfair_key_route():
    return {"key": playfair_generate_key()}


# Playfair Encryption
@router.post("/playfair/encrypt", tags=["playfair"])
async def playfair_encrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    encrypted = playfair_encrypt(content, key)
    return JSONResponse(content=encrypted)


# Playfair Decryption
@router.post("/playfair/decrypt", tags=["playfair"])
async def playfair_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    try:
        data = json.loads(content)
        ciphertext = data.get("ciphertext", "")
        meta = data.get("meta", {})
    except json.JSONDecodeError:
        return JSONResponse(content={"error": "Invalid JSON format in encrypted file"}, status_code=400)
    
    decrypted = playfair_decrypt(ciphertext, key, meta)
    return JSONResponse(content=decrypted)


# Hill Key
@router.get("/hill/key", tags=["hill"])
async def hill_key_route():
    return hill_generate_key()


# Hill Encryption
@router.post("/hill/encrypt", tags=["hill"])
async def hill_encrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    key_data = json.loads(key)
    encrypted = hill_encrypt(content, key_data)
    return JSONResponse(content=encrypted)


# Hill Decryption
@router.post("/hill/decrypt", tags=["hill"])
async def hill_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    key_data = json.loads(key)
    decrypted = hill_decrypt(content, key_data)
    return JSONResponse(content=decrypted)


# Hill Attack
@router.post("/hill/attack", tags=["hill"])
async def hill_attack_route(file: UploadFile = File(...)):
    content = await read_file(file)
    result = await asyncio.get_running_loop().run_in_executor(
        None, hill_attack, content
    )
    return JSONResponse(content=result)


# DES Key
@router.get("/des/key", tags=["des"])
async def des_key_route():
    return {"key": des_generate_key()}


# DES Encryption
@router.post("/des/encrypt", tags=["des"])
async def des_encrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    encrypted = des_encrypt(content, key)
    return JSONResponse(content=encrypted)


# DES Decryption
@router.post("/des/decrypt", tags=["des"])
async def des_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    decrypted = des_decrypt(content, key)
    return JSONResponse(content=decrypted)
