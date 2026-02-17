from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import PlainTextResponse, JSONResponse

from app.routers.ceaser_encrypt import caesar_encrypt
from app.routers.ceaser_decrypt import caesar_decrypt
from app.routers.ceaser_attack import caesar_attack
from app.routers.report import compare
from app.routers.health import router as health_router

router = APIRouter()

# Health
router.include_router(health_router)

# Report
@router.post("/report")
async def ceaser_report_route(
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


# Caesar Encryption
@router.post("/ceaser/encrypt", tags=["ceaser"])
async def ceaser_encrypt_route(file: UploadFile = File(...), key: int = Form(...)):
    content = (await file.read()).decode("utf-8")
    encrypted = caesar_encrypt(content, key)
    name = file.filename.rsplit(".", 1)[0] if "." in file.filename else file.filename
    return PlainTextResponse(
        content=encrypted,
        headers={"Content-Disposition": f'attachment; filename="{name}_encrypted.txt"'},
    )


# Caesar Decryption
@router.post("/ceaser/decrypt", tags=["ceaser"])
async def ceaser_decrypt_route(file: UploadFile = File(...), key: int = Form(...)):
    content = (await file.read()).decode("utf-8")
    decrypted = caesar_decrypt(content, key)
    name = file.filename.rsplit(".", 1)[0] if "." in file.filename else file.filename
    return PlainTextResponse(
        content=decrypted,
        headers={"Content-Disposition": f'attachment; filename="{name}_decrypted.txt"'},
    )


# Caesar Attack
@router.post("/ceaser/attack", tags=["ceaser"])
async def ceaser_attack_route(file: UploadFile = File(...)):
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
