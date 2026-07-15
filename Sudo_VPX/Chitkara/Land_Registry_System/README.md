# 🏛️ Blockchain Land Registry System

> **Immutable · Transparent · Tamper-Proof** — A Terminal-Based Blockchain In Pure C

---

## 📋 Overview

A Cross-Platform, Terminal-Based **Blockchain Land Registry** Written Entirely In C With No External Dependencies.
Every Land Record Is Sealed Inside A Cryptographic Block — Once Added, It Cannot Be Modified Or Deleted.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗂️ **Folder Block View** | Each Blockchain Block Renders As A Styled Folder Card In The Terminal |
| 💾 **JSON Persistence** | All Records Are Loaded From And Saved To `Data/Users.json` Automatically |
| ➕ **Add-Only Design** | Users Can Only Register Or Transfer Land — Past Records Can Never Be Deleted |
| 🔗 **Hash Chain** | Every Block Stores The Previous Block's Hash, Creating An Unbreakable Chain |
| 🔍 **Search & Browse** | Search By Land ID Or Browse All Folder Blocks With A Single Key |
| ✅ **Integrity Check** | One-Click Full-Chain Verification Detects Any Tampering |
| 🎨 **ANSI Color UI** | Vibrant Terminal UI With Spinners, Colors, And Box-Drawing Characters |

---

## 📁 File Structure

```
Land_Registry_System/
├── main.c               ← Full Source Code
├── Land_Registry.exe    ← Compiled Binary (Windows)
├── Data/
│   └── Users.json       ← Persistent Record Store (Add-Only)
└── README.md            ← This File
```

---

## 🗂️ Data/Users.json

All Land Records Are Stored Here In Human-Readable JSON Format.
The Program **Loads** This File On Startup And **Appends** New Records After Every Registration Or Transfer.

```json
{
  "Records": [
    {
      "Land_Id":  "LND-001",
      "Owner":    "Rajesh Kumar",
      "Location": "Chandigarh, Punjab",
      "Area":     1500,
      "Price":    8500000,
      "Type":     "REGISTER",
      "Status":   "ACTIVE"
    }
  ]
}
```

> ⚠️ **Never Manually Edit This File** — The Blockchain Hash Chain Will Break.

---

## 🔢 Menu Options

```
[ 1 ]  View All Records        → Table View Of All Land Entries
[ 2 ]  Register New Land       → Add A New Land Block (Saved To JSON)
[ 3 ]  Transfer Ownership      → Transfer Land To A New Owner (Saved To JSON)
[ 4 ]  Search By Land ID       → Folder-Style Block View Of Matching Records
[ 5 ]  View Block Folders      → Browse Any Block As A Styled Folder Card
[ 6 ]  Verify Chain Integrity  → Validate Every Hash In The Chain
[ 0 ]  Exit
```

---

## 🏗️ Build Instructions

### Windows (GCC / MinGW)
```bash
gcc main.c -o Land_Registry.exe -Wall -O2
.\Land_Registry.exe
```

### Linux / macOS
```bash
gcc main.c -o Land_Registry -Wall -O2
./Land_Registry
```

---

## 🔐 How The Blockchain Works

```
Block #0  [GENESIS]
    Hash: a1b2c3d4
        ↓
Block #1  [LND-001 · REGISTER]
    Prev: a1b2c3d4   Hash: e5f6g7h8
        ↓
Block #2  [LND-002 · REGISTER]
    Prev: e5f6g7h8   Hash: i9j0k1l2
```

Every Block's `Prev_Hash` Must Equal The Previous Block's `Hash`.
Any Modification Breaks The Chain — Detected Instantly By Option `[6]`.

---

## 🌍 Tech Stack

- **Language** : C (C99 Standard)
- **Storage**  : Custom JSON Parser + Writer (No External Libs)
- **Hashing**  : DJB2 Variant Hash Function
- **UI**       : ANSI Escape Codes + Unicode Box Drawing
- **Platform** : Windows & Linux/macOS (Cross-Platform)

---

*Built With ❤️ As Part Of The Chitkara University Project Series*
