<h1 align="center"><b>Cipher</b></h1>

<p align="center">
  <b>Cipher</b> is your all-in-one toolkit for classic cryptography. Built with a <b>Next.js</b> frontend and a <b>FastAPI</b> backend, it lets you <b>Encrypt</b>, <b>Decrypt</b>, run <b>Frequency Analysis Attacks</b>, and generate detailed <b>Reports</b> — all from a clean & modern interface.
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

| CIPHER                    | KEY TYPE               | ENCRYPTION / DECRYPTION | FREQUENCY ANALYSIS ATTACK |
| ------------------------- | ---------------------- | ----------------------- | ------------------------- |
| **Caesar Cipher**         | Integer Shift          | ✅ Supported            | ✅ Supported              |
| **Permutation Cipher**    | Permutation Alphabetic | ✅ Supported            | ✅ Supported              |
| **Vigenère Cipher**       | Polyalphabetic         | ✅ Supported            | ✅ Supported              |
| **Playfair Cipher (8x8)** | Alphanumeric           | ✅ Supported            | ❌ Unsupported            |
| **Hill Cipher (2x2)**     | Numeric Matrix         | ✅ Supported            | ✅ Supported              |
| **DES**                   | 16-bit Hex             | ✅ Supported            | ❌ Unsupported            |

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
