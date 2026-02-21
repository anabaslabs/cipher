# Cipher (API)

FastAPI backend for the Cipher project.

## ⚙️ API Endpoints

| METHOD | ENDPOINT            | DESCRIPTION                                       |
| ------ | ------------------- | ------------------------------------------------- |
| `GET`  | `/health`           | Health check                                      |
| `POST` | `/report`           | Compare original vs recovered and download report |
| `GET`  | `/caesar/key`       | Generate a random Caesar cipher key               |
| `POST` | `/caesar/encrypt`   | Encrypt with Caesar cipher                        |
| `POST` | `/caesar/decrypt`   | Decrypt with Caesar cipher                        |
| `POST` | `/caesar/attack`    | Frequency analysis attack on Caesar cipher        |
| `GET`  | `/permute/key`      | Generate a random Permutation cipher key          |
| `POST` | `/permute/encrypt`  | Encrypt with Permutation cipher                   |
| `POST` | `/permute/decrypt`  | Decrypt with Permutation cipher                   |
| `POST` | `/permute/attack`   | Frequency analysis attack on Permutation cipher   |
| `GET`  | `/vigenere/key`     | Generate a random Vigenère cipher key             |
| `POST` | `/vigenere/encrypt` | Encrypt with Vigenère cipher                      |
| `POST` | `/vigenere/decrypt` | Decrypt with Vigenère cipher                      |
| `POST` | `/vigenere/attack`  | Frequency analysis attack on Vigenère cipher      |
| `GET`  | `/playfair/key`     | Generate a random Playfair cipher (8x8) key       |
| `POST` | `/playfair/encrypt` | Encrypt with Playfair cipher (8x8)                |
| `POST` | `/playfair/decrypt` | Decrypt with Playfair cipher (8x8)                |
| `GET`  | `/hill/key`         | Generate a random Hill cipher (2x2) key           |
| `POST` | `/hill/encrypt`     | Encrypt with Hill cipher (2x2)                    |
| `POST` | `/hill/decrypt`     | Decrypt with Hill cipher (2x2)                    |
| `POST` | `/hill/attack`      | Frequency analysis attack on Hill cipher (2x2)    |
| `GET`  | `/des/key`          | Generate a random DES key                         |
| `POST` | `/des/encrypt`      | Encrypt with DES                                  |
| `POST` | `/des/decrypt`      | Decrypt with DES                                  |

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
