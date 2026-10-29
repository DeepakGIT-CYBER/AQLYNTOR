# AQLYNTOR — Trustworthy AI Execution & Task Safety Observatory

> Enterprise-grade Autonomous AI Agent Governance, Policy Enforcement, and Secure Execution Framework.

---

## 🛡️ Security Architecture & Features

AQLYNTOR is built to bridge the gap between autonomous AI task execution and strict enterprise security. It features a robust defense-in-stack architecture:

1. **Bearer Token Authentication (`HTTPBearer`)**: 
   - Protects all sensitive execution endpoints from unauthorized access.
   - Rejects unauthenticated API calls with a strict `403 Forbidden` security alert response.

2. **Rate Limiting & DDoS Protection (`SlowAPI`)**: 
   - Implements IP-based request throttling to mitigate brute-force and DDoS attacks on critical task execution endpoints.

3. **Autonomous Policy Gate & Verifier**:
   - Intercepts unsafe operations (e.g., unauthorized file deletions or destructive system calls) and triggers bounded recoveries.

4. **Modern High-Tech Dashboard**:
   - Dark-themed glassmorphism UI styled with Tailwind CSS.
   - Real-time telemetry console and live firewall status indicators (`🛡️ Firewall & Auth Active`).

---

## 🚀 Quick Start & Local Setup

### Prerequisites
Make sure you have Python (v3.10+) installed.

### 1. Clone the Repository
```bash
git clone [https://github.com/DeepakGIT-CYBER/AQLYNTOR.git](https://github.com/DeepakGIT-CYBER/AQLYNTOR.git)
cd AQLYNTOR