# Cipher (API)

FastAPI backend for the Cipher project.

## ⚙️ API Endpoints

| METHOD                                           | ENDPOINT                  | DESCRIPTION                                       |
| ------------------------------------------------ | ------------------------- | ------------------------------------------------- |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/`                       | Root endpoint                                     |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/health`                 | Health check                                      |
| ![POST](https://img.shields.io/badge/POST-green) | `/report`                 | Compare original vs recovered and download report |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/caesar/key`             | Generate a random Caesar cipher key               |
| ![POST](https://img.shields.io/badge/POST-green) | `/caesar/encrypt`         | Encrypt with Caesar cipher                        |
| ![POST](https://img.shields.io/badge/POST-green) | `/caesar/decrypt`         | Decrypt with Caesar cipher                        |
| ![POST](https://img.shields.io/badge/POST-green) | `/caesar/attack`          | Frequency analysis attack on Caesar cipher        |
| ![POST](https://img.shields.io/badge/POST-green) | `/caesar/attack/stream`   | SSE feed for Caesar attack progress               |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/permute/key`            | Generate a random Permutation cipher key          |
| ![POST](https://img.shields.io/badge/POST-green) | `/permute/encrypt`        | Encrypt with Permutation cipher                   |
| ![POST](https://img.shields.io/badge/POST-green) | `/permute/decrypt`        | Decrypt with Permutation cipher                   |
| ![POST](https://img.shields.io/badge/POST-green) | `/permute/attack`         | Frequency analysis attack on Permutation cipher   |
| ![POST](https://img.shields.io/badge/POST-green) | `/permute/attack/stream`  | SSE feed for Permutation attack progress          |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/vigenere/key`           | Generate a random Vigenère cipher key             |
| ![POST](https://img.shields.io/badge/POST-green) | `/vigenere/encrypt`       | Encrypt with Vigenère cipher                      |
| ![POST](https://img.shields.io/badge/POST-green) | `/vigenere/decrypt`       | Decrypt with Vigenère cipher                      |
| ![POST](https://img.shields.io/badge/POST-green) | `/vigenere/attack`        | Frequency analysis attack on Vigenère cipher      |
| ![POST](https://img.shields.io/badge/POST-green) | `/vigenere/attack/stream` | SSE feed for Vigenère attack progress             |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/playfair/key`           | Generate a random Playfair cipher (8x8) key       |
| ![POST](https://img.shields.io/badge/POST-green) | `/playfair/encrypt`       | Encrypt with Playfair cipher (8x8)                |
| ![POST](https://img.shields.io/badge/POST-green) | `/playfair/decrypt`       | Decrypt with Playfair cipher (8x8)                |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/hill/key`               | Generate a random Hill cipher (2x2) key           |
| ![POST](https://img.shields.io/badge/POST-green) | `/hill/encrypt`           | Encrypt with Hill cipher (2x2)                    |
| ![POST](https://img.shields.io/badge/POST-green) | `/hill/decrypt`           | Decrypt with Hill cipher (2x2)                    |
| ![POST](https://img.shields.io/badge/POST-green) | `/hill/attack`            | Frequency analysis attack on Hill cipher (2x2)    |
| ![POST](https://img.shields.io/badge/POST-green) | `/hill/attack/stream`     | SSE feed for Hill attack progress                 |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/des/key`                | Generate a random DES key                         |
| ![POST](https://img.shields.io/badge/POST-green) | `/des/encrypt`            | Encrypt with DES                                  |
| ![POST](https://img.shields.io/badge/POST-green) | `/des/decrypt`            | Decrypt with DES                                  |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/aes/key`                | Generate a random AES key (default: 128 bits)     |
| ![POST](https://img.shields.io/badge/POST-green) | `/aes/encrypt`            | Encrypt with AES                                  |
| ![POST](https://img.shields.io/badge/POST-green) | `/aes/decrypt`            | Decrypt with AES                                  |
| ![GET](https://img.shields.io/badge/GET-blue)    | `/rc5/key`                | Generate a random RC5 key (default: 16 bytes)     |
| ![POST](https://img.shields.io/badge/POST-green) | `/rc5/encrypt`            | Encrypt with RC5                                  |
| ![POST](https://img.shields.io/badge/POST-green) | `/rc5/decrypt`            | Decrypt with RC5                                  |

## 🚀 Getting Started

### Setup

```bash
cd apps/api
py -m venv venv
```

```bash
venv\Scripts\activate # Windows
# OR
source venv/bin/activate # Linux / macOS
```

```bash
pip install -r requirements.txt
```

### Development

```bash
pnpm dev
# OR
turbo dev
```

### Production

```bash
pnpm start
# OR
turbo start
```

## 🔮 Usage

The API runs at [http://localhost:8000](http://localhost:8000).  
Interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).
