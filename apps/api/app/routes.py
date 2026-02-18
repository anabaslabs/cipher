from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import PlainTextResponse, JSONResponse

from app.routers.caesar_encrypt import caesar_encrypt
from app.routers.caesar_decrypt import caesar_decrypt
from app.routers.caesar_attack import caesar_attack
from app.routers.permute_encrypt import encrypt as permute_encrypt
from app.routers.permute_decrypt import decrypt as permute_decrypt
from app.routers.permute_attack import frequency_attack
from app.routers.caesar_key import generate_key as caesar_generate_key
from app.routers.permute_key import generate_key as permute_generate_key
from app.routers.report import compare

router = APIRouter()

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
    original_text = (await original.read()).decode("utf-8")
    recovered_text = (await recovered.read()).decode("utf-8")
    report = compare(original_text, recovered_text)

    name = original.filename.rsplit(".", 1)[0] if "." in original.filename else original.filename
    return PlainTextResponse(
        content=report,
        headers={"Content-Disposition": f'attachment; filename="{name}_comparison_report.txt"'},
    )


# Caesar Key
@router.get("/caesar/key", tags=["caesar"])
async def caesar_key_route():
    return {"key": caesar_generate_key()}

# Caesar Encryption
@router.post("/caesar/encrypt", tags=["caesar"])
async def caesar_encrypt_route(file: UploadFile = File(...), key: int = Form(...)):
    content = (await file.read()).decode("utf-8")
    encrypted = caesar_encrypt(content, key)
    name = file.filename.rsplit(".", 1)[0] if "." in file.filename else file.filename
    return PlainTextResponse(
        content=encrypted,
        headers={"Content-Disposition": f'attachment; filename="{name}_encrypted.txt"'},
    )


# Caesar Decryption
@router.post("/caesar/decrypt", tags=["caesar"])
async def caesar_decrypt_route(file: UploadFile = File(...), key: int = Form(...)):
    content = (await file.read()).decode("utf-8")
    decrypted = caesar_decrypt(content, key)
    name = file.filename.rsplit(".", 1)[0] if "." in file.filename else file.filename
    return PlainTextResponse(
        content=decrypted,
        headers={"Content-Disposition": f'attachment; filename="{name}_decrypted.txt"'},
    )


# Caesar Attack
@router.post("/caesar/attack", tags=["caesar"])
async def caesar_attack_route(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    result = caesar_attack(content)

    name = file.filename.rsplit(".", 1)[0] if "." in file.filename else file.filename

    return JSONResponse(content={
        "files": [
            {
                "filename": f"{name}_attacked.txt",
                "content": result["plaintext"],
            },
            {
                "filename": f"{name}_key_{result['best_key']}.txt",
                "content": str(result["best_key"]),
            },
        ],
    })


# Permutation Key
@router.get("/permute/key", tags=["permute"])
async def permute_key_route():
    return {"key": permute_generate_key()}


# Permutation Encryption
@router.post("/permute/encrypt", tags=["permute"])
async def permute_encrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = (await file.read()).decode("utf-8")
    encrypted = permute_encrypt(content, key)
    name = file.filename.rsplit(".", 1)[0] if "." in file.filename else file.filename
    return PlainTextResponse(
        content=encrypted,
        headers={"Content-Disposition": f'attachment; filename="{name}_encrypted.txt"'},
    )


# Permutation Decryption
@router.post("/permute/decrypt", tags=["permute"])
async def permute_decrypt_route(file: UploadFile = File(...), key: str = Form(...)):
    content = (await file.read()).decode("utf-8")
    decrypted = permute_decrypt(content, key)
    name = file.filename.rsplit(".", 1)[0] if "." in file.filename else file.filename
    return PlainTextResponse(
        content=decrypted,
        headers={"Content-Disposition": f'attachment; filename="{name}_decrypted.txt"'},
    )


# Permutation Attack
@router.post("/permute/attack", tags=["permute"])
async def permute_attack_route(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    result = frequency_attack(content)
    return JSONResponse(content=result)

