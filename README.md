# 🧬 RxTrace | Aetheris Pharma Strategic Intelligence Hub

![Domain](https://img.shields.io/badge/Domain-Pharma%20Sales%20Analytics-0C6B3C?style=flat-square)
![Type](https://img.shields.io/badge/Type-Geospatial%20Intelligence-8A2BE2?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=flat-square&logo=pandas&logoColor=white)
![Aetheris Pharma Enterprise](https://img.shields.io/badge/Aetheris-Enterprise-green)
![Version](https://img.shields.io/badge/Version-3.0-blue)
![AI Powered](https://img.shields.io/badge/AI-Gemini%20Integrated-blueviolet)

**RxTrace** is a next-generation Strategic Intelligence Hub designed for Pharmaceutical Headquarters to dominate territory marketing, synchronize field force actions, and ensure audit-ready clinical fulfillment through a robust 2-way handshake protocol.

---

## Key Modules & Capabilities

### HQ Strategic Command (Admin)
*   **Aetheris AI Playbook**: Real-time market synthesis using **Google Gemini** to transform NewsAPI trends and competitor moves into actionable global level marketing strategies.
*   **Global Directives**: Instant deployment of marketing strategies to every Sales Rep in the network with a single click.
*   **Chemist Audit Intelligence**: 3-way alignment mapping between **Doctor : Molecule : Chemist** to identify competitor leakage and retail substitution risks.
*   **National Map Intelligence**: High-fidelity density analysis across all clinical hubs and specialties.

### Field Force Pulse (Sales Rep)
*   **Strategic Focus Today**: Prioritized doctor visits based on "Risk Scores" and "Strategy Alignment."
*   **Multi-Batch Fulfillment**: Segmented delivery tracking that moves away from 'all-or-nothing' shipments to an audit-ready batch process.
*   **HQ Directive Hub**: Instant access to global strategic commands and transparent plans of action from the enterprise leadership.

### Doctor Partner Portal (HCP)
*   **Sample Handshake Protocol**: Formal digital receipt of specific sample batches, ensuring clinical accountability.
*   **Molecular Target Requirements**: Live tracking of prescription milestones and compliance scores.
*   **Priority Dispatch**: One-click communication with the assigned territory representative for urgent clinical support.

---

## 🛠️ Technology Stack
*   **Framework**: [Streamlit](https://streamlit.io/) for high-performance data interfaces.
*   **Analysis**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) for strategic telemetry.
*   **Visuals**: [Plotly](https://plotly.com/) for enterprise-grade territory intelligence.
*   **AI Engine**: [Google Gemini 1.5 Flash](https://ai.google.dev/) for strategic synthesis.
*   **Market Pulse**: NewsAPI for live competitor tracking.

---

## 📦 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd rxtrace
   ```

2. **Configure Environment**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   NEWS_API_KEY=your_news_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Hub**
   ```bash
   streamlit run app.py
   ```

---

## Credentials Registry
Access the hub using the credentials defined in **`login.txt`**.
*   **Admin**: `admin` / `admin123`
*   **Reps (10)**: `rep01` to `rep10` (Passwords: `user123`)
*   **Doctors (5)**: `doc01` to `doc05` (Passwords: `user123`)

---

## Aetheris Strategic Handshake (Workflow)
RxTrace implements a mandatory 2-way handshake:
1. **Admin** assigns a requisition.
2. **Rep** dispatches a specific batch qty (Status: In Transit).
3. **Doctor** confirms receipt in their portal (Status: Completed).
*This ensures 100% audit-ready data for corporate compliance.*

---
*Developed for Aetheris Pharma Enterprise Strategic Operations.* ⚔️🚀🧬
