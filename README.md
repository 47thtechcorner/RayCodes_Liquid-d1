<div align="center">
  <a href="https://youtu.be/dS-Q47dI2_M">
    <img src="https://img.youtube.com/vi/dS-Q47dI2_M/0.jpg" alt="Liquid d1: This 407MB AI Makes 8ms Decisions With ZERO Tokens!">
  </a>
  <h3>📺 <a href="https://youtu.be/dS-Q47dI2_M">Watch the full tutorial on YouTube</a></h3>
</div>

# 🌐 Liquid d1 Multimodal Triage Engine

Liquid d1 Multimodal Support Triage is a zero-token decision engine that analyzes customer complaint text and damage photos simultaneously in a single forward pass without conversational delay.

## ⚡ How It Works

| Step 1: Input | Step 2: AI Action | Step 3: Result |
| :--- | :--- | :--- |
| Customer submits text message and broken item photo | Model evaluates routing, severity, and photo damage simultaneously | Calibrated JSON decision, genuine claim verification, and response |

## 📦 Features

- ⚡ **Zero-Token Latency:** Delivers instantaneous decisions without waiting for autoregressive text stream generation.
- 🖼️ **Multimodal Damage Assessment:** Cross-checks photo visual evidence against customer text claims in one single forward pass.
- 🎯 **Automated Team Routing:** Accurately routes claims to Replacements, Fragile Claims, or Safety Escalations.
- 🛡️ **Genuineness & Fraud Screening:** Validates physical breakage patterns to filter fraudulent or unrelated photo submissions.
- ⏱️ **Sub-20ms Processing:** Records execution latency per request for high-throughput enterprise queues.

## 🛠️ Tech Stack

- **Model:** Liquid AI d1-omni-600M / d1-3B
- **Framework:** Python 3.10+, PIL (Pillow), PyTorch
- **GGUF Runtime:** llama.cpp / Ollama (`llama-server`) with `mmproj-model-f16.gguf`

## 🚀 Setup & Installation

Install dependencies with a single command:

```powershell
pip install "transformers>=5.15" torch torchvision pillow requests
```

### Download Model Checkpoints

Download the official 8-bit quantized weights and vision projector into the `models/` directory:

```powershell
hf download LiquidAI/d1-omni-600M-GGUF d1-omni-600M-Q8_0.gguf --local-dir models
hf download LiquidAI/d1-omni-600M-GGUF mmproj-model-f16.gguf --local-dir models
```

### Register with Ollama

Register the local checkpoint in Ollama using the provided `Modelfile`:

```powershell
ollama create liquid-d1 -f Modelfile
```

Alternatively, serve via `llama-server` with multimodal projector enabled:

```powershell
llama-server -m models/d1-omni-600M-Q8_0.gguf --mmproj models/mmproj-model-f16.gguf -b 4096 -ub 4096 --port 8080
```

## 💻 Running the Application

Run the multimodal triage pipeline across all customer complaints and damage photos:

```powershell
python main.py
```

The script evaluates all 5 customer cases, verifies visual damage, calculates latency in milliseconds, generates customer replies, and exports results to `outputs/outputs.md`.

## 📁 File Structure

```text
Liquid d1/
├── Modelfile                 # Ollama model registration
├── README.md                 # Setup and architecture documentation
├── inputs/                   # Customer complaints & damage photos
│   ├── case_1_plates.png     # Smashed dinner plates
│   ├── case_2_cup.png        # Broken ceramic mug
│   ├── case_3_cooktop.png    # Cracked induction cooktop
│   ├── case_4_dish.png       # Split porcelain platter
│   ├── case_5_luggage.png    # Crushed suitcase
│   └── complaints.json       # Customer complaint texts & order metadata
├── main.py                   # Production multimodal triage engine
└── models/                   # GGUF weights & multimodal projector
    ├── d1-omni-600M-Q8_0.gguf
    └── mmproj-model-f16.gguf
```

## 🎯 5 Use Cases

1. **E-Commerce Damage Claims:** Instant verification of broken merchandise photos for automated zero-touch refunds.
2. **Airline Baggage Damage Triage:** Rapid evaluation of luggage damage photos and compensation routing.
3. **Hazardous Appliance Screening:** Automated escalation of cracked electrical cooktops and shattered glass items.
4. **Logistics Courier Dispute Resolution:** Cross-verifying crushed packaging vs intact items for shipping insurance.
5. **Restaurant & Catering Supply:** High-throughput batch processing of transit-damaged tableware.

## 🔮 5 Future Features

1. **Web Dashboard:** Interactive single-page UI for live drag-and-drop customer ticket submissions.
2. **Optical Character Recognition:** Automatic invoice and serial number reading from parcel labels.
3. **Automated Warehouse Restock:** Direct integration with ERP inventory for immediate replacement dispatch.
4. **Fraud Ring Correlation:** Image hash comparison across multiple accounts to detect recycled damage photos.
5. **Customer SMS Automation:** Instant dispatch of claim resolution updates to customer mobile devices.

---

## 🏷️ Keywords & Tags

`Liquid AI` `Liquid d1` `d1-omni` `Multimodal AI` `Zero-Token Architecture` `Edge AI` `Ollama` `GGUF` `llama.cpp` `Customer Support AI` `Damage Detection` `Vision AI` `Real-Time Inference`
