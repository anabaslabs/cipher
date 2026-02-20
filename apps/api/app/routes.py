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
    return PlainTextResponse(
        content=report,
        headers={
            "Content-Disposition": f'attachment; filename="{name}_report.txt"'
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
    return PlainTextResponse(
        content=encrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_encrypted_CC.txt"'
        },
    )


# Caesar Decryption
@router.post("/caesar/decrypt", tags=["caesar"])
async def caesar_decrypt_route(file: UploadFile = File(...), key: int = Form(...)):
    content = await read_file(file)
    decrypted = caesar_decrypt(content, key)
    return PlainTextResponse(
        content=decrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_decrypted.txt"'
        },
    )


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
    return PlainTextResponse(
        content=encrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_encrypted_PC.txt"'
        },
    )


# Permutation Decryption
@router.post("/permute/decrypt", tags=["permute"])
async def permute_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    decrypted = permute_decrypt(content, key)
    return PlainTextResponse(
        content=decrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_decrypted.txt"'
        },
    )


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
    return PlainTextResponse(
        content=encrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_encrypted_VC.txt"'
        },
    )


# Vigenere Decryption
@router.post("/vigenere/decrypt", tags=["vigenere"])
async def vigenere_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    decrypted = vigenere_decrypt(content, key)
    return PlainTextResponse(
        content=decrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_decrypted.txt"'
        },
    )


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
    encrypted_body, meta = playfair_encrypt(content, key)
    payload = json.dumps(meta) + "\n---PLAYFAIR_META---\n" + encrypted_body
    return PlainTextResponse(
        content=payload,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_encrypted_PFC.txt"'
        },
    )


# Playfair Decryption
@router.post("/playfair/decrypt", tags=["playfair"])
async def playfair_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    if "---PLAYFAIR_META---" in content:
        meta_str, ciphertext = content.split("\n---PLAYFAIR_META---\n", 1)
        meta = json.loads(meta_str)
    else:
        return JSONResponse(content={"error": "Missing meta data in encrypted file"}, status_code=400)
    decrypted = playfair_decrypt(ciphertext, key, meta)
    return PlainTextResponse(
        content=decrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_decrypted.txt"'
        },
    )


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
    return PlainTextResponse(
        content=encrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_encrypted_HC.txt"'
        },
    )


# Hill Decryption
@router.post("/hill/decrypt", tags=["hill"])
async def hill_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    key_data = json.loads(key)
    decrypted = hill_decrypt(content, key_data)
    return PlainTextResponse(
        content=decrypted,
        headers={
            "Content-Disposition": f'attachment; filename="{get_name(file)}_decrypted.txt"'
        },
    )


# Hill Attack
@router.post("/hill/attack", tags=["hill"])
async def hill_attack_route(file: UploadFile = File(...)):
    content = await read_file(file)
    result = await asyncio.get_running_loop().run_in_executor(
        None, hill_attack, content
    )
    return JSONResponse(content=result)
