# Liquid d1 Multimodal Support Triage Report

- Target Model: **liquid-d1 (Ollama)** | Modality: Vision + Text | Output Tokens: **0 tokens**
- Average Latency: 109.63 ms

| Case | Image | Assigned Team | Severity (0-3) | Damage P(yes) | Latency | Automated Reply |
|---|---|---|---|---|---|---|
| Case 01 | `case_1_plates.png` | **Fragile Replacements** (100%) | 2.6/3.0 | 0.99 | 110.12 ms | *"Your breakage claim is approved. A reinforced replacement has been scheduled for delivery."* |
| Case 02 | `case_2_cup.png` | **Fragile Replacements** (100%) | 2.6/3.0 | 0.99 | 110.6 ms | *"Your breakage claim is approved. A reinforced replacement has been scheduled for delivery."* |
| Case 03 | `case_3_cooktop.png` | **Hazardous Appliance** (88%) | 2.9/3.0 | 0.99 | 109.0 ms | *"Please unplug the unit immediately. Our team has expedited a full replacement and refund."* |
| Case 04 | `case_4_dish.png` | **Fragile Replacements** (88%) | 2.6/3.0 | 0.99 | 109.48 ms | *"Your breakage claim is approved. A reinforced replacement has been scheduled for delivery."* |
| Case 05 | `case_5_luggage.png` | **Baggage Logistics** (88%) | 2.6/3.0 | 0.99 | 108.97 ms | *"We have opened a priority baggage claim and issued a courier inspection credit to your account."* |
