<h1 align="center"><b>Cipher</b></h1>

<p align="center">
  <a href="https://github.com/anabaslabs/cipher"><b>Cipher</b></a> is your all-in-one toolkit for classic cryptography. Built with a <a href="https://nextjs.org"><b>Next.js</b></a> frontend and a <a href="https://fastapi.tiangolo.com"><b>FastAPI</b></a> backend, it lets you <b>Encrypt</b>, <b>Decrypt</b>, run <b>Frequency Analysis Attacks</b>, and generate detailed <b>Reports</b> — all from a clean & modern interface.
</p>

## ✨ Features

| FEATURE                       | DESCRIPTION                                                                        |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| **Encrypt**                   | Secure your text using a custom key. Keeps formatting fully intact.                |
| **Decrypt**                   | Unlock encrypted text with your key. Recover the original message.                 |
| **Frequency Analysis Attack** | Analyze ciphertext patterns automatically. Reveal likely letter substitutions.     |
| **Generate Report**           | Compile comparison insights into a clean summary. Export a ready-to-submit report. |
| **Key Generation**            | Auto-generate secure random keys for any supported cipher.                         |

## 🔑 Supported Ciphers

| CIPHER                    | KEY TYPE                   | ENCRYPTION / DECRYPTION | FREQUENCY ANALYSIS ATTACK |
| ------------------------- | -------------------------- | ----------------------- | ------------------------- |
| **Caesar Cipher**         | Integer Shift Key          | ✅ Supported            | ✅ Supported              |
| **Permutation Cipher**    | Permutation Alphabetic Key | ✅ Supported            | ✅ Supported              |
| **Vigenère Cipher**       | Polyalphabetic Keyword     | ✅ Supported            | ✅ Supported              |
| **Playfair Cipher (6x6)** | Alphanumeric Key Matrix    | ✅ Supported            | ❌ Unsupported            |

## 🛠️ Tech Stack

| LAYER          | TECHNOLOGY                                                   |
| -------------- | ------------------------------------------------------------ |
| **Frontend**   | **TypeScript**, **Next.js**, **Tailwind CSS**, **shadcn/ui** |
| **Shared UI**  | **Radix UI**, **Tabler Icons**, **Motion**                   |
| **Backend**    | **Python**, **FastAPI**, **Uvicorn**                         |
| **Monorepo**   | **Turborepo**, **pnpm Workspaces**                           |
| **Deployment** | **Vercel**                                                   |

## 🏗️ Project Structure

```
cipher/
├── apps/
│   ├── api/               # FastAPI backend
│   │   └── app/
│   │       ├── routers/   # Cipher logic (encrypt, decrypt, attack, key, report)
│   │       ├── routes.py  # API route definitions
│   │       ├── config.py  # App configuration
│   │       └── main.py    # FastAPI app entry point
│   └── web/               # Next.js frontend
│       └── app/
|           ├── /          # Home page
│           ├── encrypt/   # Encryption page
│           ├── decrypt/   # Decryption page
│           ├── attack/    # Frequency analysis attack page
│           └── report/    # Report generation page
└── packages/
    ├── ui/                # Shared UI component library
    ├── eslint-config/     # Shared ESLint configuration
    └── typescript-config/ # Shared TypeScript configuration
```

## ⚙️ API Endpoints

| METHOD | ENDPOINT            | DESCRIPTION                                       |
| ------ | ------------------- | ------------------------------------------------- |
| `GET`  | `/health`           | Health check                                      |
| `POST` | `/report`           | Compare original vs recovered and download report |
| `GET`  | `/caesar/key`       | Generate a random Caesar key                      |
| `POST` | `/caesar/encrypt`   | Encrypt with Caesar cipher                        |
| `POST` | `/caesar/decrypt`   | Decrypt with Caesar cipher                        |
| `POST` | `/caesar/attack`    | Frequency analysis attack on Caesar               |
| `GET`  | `/permute/key`      | Generate a random Permutation key                 |
| `POST` | `/permute/encrypt`  | Encrypt with Permutation cipher                   |
| `POST` | `/permute/decrypt`  | Decrypt with Permutation cipher                   |
| `POST` | `/permute/attack`   | Frequency analysis attack on Permutation          |
| `GET`  | `/vigenere/key`     | Generate a random Vigenère key                    |
| `POST` | `/vigenere/encrypt` | Encrypt with Vigenère cipher                      |
| `POST` | `/vigenere/decrypt` | Decrypt with Vigenère cipher                      |
| `POST` | `/vigenere/attack`  | Frequency analysis attack on Vigenère             |
| `GET`  | `/playfair/key`     | Generate a random Playfair cipher (6x6)           |
| `POST` | `/playfair/encrypt` | Encrypt with Playfair cipher (6x6)                |
| `POST` | `/playfair/decrypt` | Decrypt with Playfair cipher (6x6)                |

## 🚀 Getting Started

### Prerequisites

- **Node.js** >= 20
- **pnpm** >= 10
- **Python** >= 3.12
- **Turbo CLI** (optional)

### Setup

Clone the repository and navigate into it:

```bash
git clone https://github.com/anabaslabs/cipher.git
cd cipher
```

Install frontend dependencies (from monorepo root):

```bash
pnpm install
```

Install backend dependencies (from monorepo root):

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

Configure environment variables (from monorepo root):

```bash
cd apps/api
cp .env.example .env
cd ../../apps/web
cp .env.example .env
```

### Run Locally

Start frontend and backend concurrently (from monorepo root):

```bash
pnpm dev
# OR
turbo dev
```

### In Production

Build frontend and backend (from monorepo root):

```bash
pnpm build
# OR
turbo build
```

Start the production server (from monorepo root):

```bash
pnpm start
# OR
turbo start
```

## 👥 Contributors

<a href="https://github.com/itskdhere"><img src="https://avatars.githubusercontent.com/u/86651039?v=4" width="48" height="48" style="border-radius:50%" alt="itskdhere"></a>&nbsp;
<a href="https://github.com/saptarshiroy39"><img src="https://avatars.githubusercontent.com/u/138118143?v=4" width="48" height="48" style="border-radius:50%" alt="saptarshiroy39"></a>

<p align="center">
  <a href="https://youtu.be/EA4DipdhpV8">🙂</a>
</p>
