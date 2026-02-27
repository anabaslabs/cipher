import os
import json
import asyncio
import threading
import queue
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse, StreamingResponse

from app.routers.report import compare

from app.routers.caesar.key import generate_key as caesar_generate_key
from app.routers.caesar.encrypt import caesar_encrypt
from app.routers.caesar.decrypt import caesar_decrypt
from app.routers.caesar.attack import caesar_attack

from app.routers.permute.key import generate_key as permute_generate_key
from app.routers.permute.encrypt import encrypt as permute_encrypt
from app.routers.permute.decrypt import decrypt as permute_decrypt
from app.routers.permute.attack import frequency_attack

from app.routers.vigenere.key import generate_key as vigenere_generate_key
from app.routers.vigenere.encrypt import encrypt as vigenere_encrypt
from app.routers.vigenere.decrypt import decrypt as vigenere_decrypt
from app.routers.vigenere.attack import vigenere_attack

from app.routers.playfair.key import generate_key as playfair_generate_key
from app.routers.playfair.encrypt import encrypt as playfair_encrypt
from app.routers.playfair.decrypt import decrypt as playfair_decrypt

from app.routers.hill.key import generate_key as hill_generate_key
from app.routers.hill.encrypt import encrypt as hill_encrypt
from app.routers.hill.decrypt import decrypt as hill_decrypt
from app.routers.hill.attack import hill_attack

from app.routers.des.key import generate_key as des_generate_key
from app.routers.des.encrypt import encrypt as des_encrypt
from app.routers.des.decrypt import decrypt as des_decrypt

from app.routers.aes.key import generate_key as aes_generate_key
from app.routers.aes.encrypt import encrypt as aes_encrypt
from app.routers.aes.decrypt import decrypt as aes_decrypt

from app.routers.rc5.key import generate_key as rc5_generate_key
from app.routers.rc5.encrypt import encrypt as rc5_encrypt
from app.routers.rc5.decrypt import decrypt as rc5_decrypt


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
    algo_suffixes = ["_CC_", "_PC_", "_VC_", "_PFC_", "_HC_", "_DC_", "_AES_", "_RC5_"]
    suffix = next((s.strip("_") for s in algo_suffixes if s in recovered_name), "")
    report_name = f"{name}_{suffix}_Report.txt" if suffix else f"{name}_Report.txt"
    return PlainTextResponse(
        content=report,
        headers={
            "Content-Disposition": f'attachment; filename="{report_name}"'
        },
    )


    
# SSE Attack Streaming
def _run_attack_with_progress(attack_fn, content, progress_queue, **kwargs):
    def progress_callback(current, total, status):
        pct = int((current / total) * 100) if total else 0
        progress_queue.put({"progress": pct, "status": status})

    try:
        result = attack_fn(content, progress_callback=progress_callback, **kwargs)
        progress_queue.put({"progress": 100, "status": "Complete", "result": result})
    except Exception as e:
        progress_queue.put({"progress": -1, "status": "Error", "error": str(e)})
    progress_queue.put(None)


async def _sse_generator(progress_queue):
    while True:
        try:
            msg = await asyncio.get_event_loop().run_in_executor(None, progress_queue.get, True, 0.5)
        except Exception:
            await asyncio.sleep(0.1)
            continue
        if msg is None:
            break
        yield f"data: {json.dumps(msg)}\n\n"


@router.post("/caesar/attack/stream", tags=["caesar"])
async def caesar_attack_stream(file: UploadFile = File(...)):
    content = await read_file(file)
    progress_queue = queue.Queue()
    threading.Thread(
        target=_run_attack_with_progress,
        args=(caesar_attack, content, progress_queue),
        daemon=True,
    ).start()
    return StreamingResponse(_sse_generator(progress_queue), media_type="text/event-stream")


@router.post("/permute/attack/stream", tags=["permute"])
async def permute_attack_stream(file: UploadFile = File(...)):
    content = await read_file(file)
    progress_queue = queue.Queue()
    threading.Thread(
        target=_run_attack_with_progress,
        args=(frequency_attack, content, progress_queue),
        daemon=True,
    ).start()
    return StreamingResponse(_sse_generator(progress_queue), media_type="text/event-stream")


@router.post("/vigenere/attack/stream", tags=["vigenere"])
async def vigenere_attack_stream(file: UploadFile = File(...)):
    content = await read_file(file)
    progress_queue = queue.Queue()
    threading.Thread(
        target=_run_attack_with_progress,
        args=(vigenere_attack, content, progress_queue),
        daemon=True,
    ).start()
    return StreamingResponse(_sse_generator(progress_queue), media_type="text/event-stream")


@router.post("/hill/attack/stream", tags=["hill"])
async def hill_attack_stream(file: UploadFile = File(...)):
    content = await read_file(file)
    progress_queue = queue.Queue()
    threading.Thread(
        target=_run_attack_with_progress,
        args=(hill_attack, content, progress_queue),
        daemon=True,
    ).start()
    return StreamingResponse(_sse_generator(progress_queue), media_type="text/event-stream")


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
    ciphertext = await read_file(file)
    decrypted = playfair_decrypt(ciphertext, key)
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


# AES Key
@router.get("/aes/key", tags=["aes"])
async def aes_key_route(bits: int = 128):
    return {"key": aes_generate_key(bits)}


# AES Encryption
@router.post("/aes/encrypt", tags=["aes"])
async def aes_encrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    encrypted = aes_encrypt(content, key)
    return JSONResponse(content=encrypted)


# AES Decryption
@router.post("/aes/decrypt", tags=["aes"])
async def aes_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = await read_file(file)
    decrypted = aes_decrypt(content, key)
    return JSONResponse(content=decrypted)


# RC5 Key
@router.get("/rc5/key", tags=["rc5"])
async def rc5_key_route(b: int = 16):
    return {"key": rc5_generate_key(b)}


# RC5 Encryption
@router.post("/rc5/encrypt", tags=["rc5"])
async def rc5_encrypt_route(
    file: UploadFile = File(...), 
    key: str = Form(...),
    w: int = Form(32),
    r: int = Form(12)
):
    content = await read_file(file)
    encrypted = rc5_encrypt(content, key, w, r)
    return JSONResponse(content=encrypted)


# RC5 Decryption
@router.post("/rc5/decrypt", tags=["rc5"])
async def rc5_decrypt_route(
    file: UploadFile = File(...), 
    key: str = Form(...),
    w: int = Form(32),
    r: int = Form(12)
):
    content = await read_file(file)
    decrypted = rc5_decrypt(content, key, w, r)
    return JSONResponse(content=decrypted)

