# AiotInOne

**AiotInOne｜智慧農業 AIoT 三方整合平台**

AiotInOne 是一套可擴充的 AIoT 共用平台，第一個落地場景為智慧農業，連結：

- **Producer｜生產端**：農民、農場管理者、合作社
- **Merchant｜銷售端**：採購商、通路商、零售商
- **Consumer｜消費端**：一般消費者
- **Administrator｜治理端**：系統管理員，不列入商業三方角色

本專案採用 **OpenSpec 規格驅動開發**。所有重大功能必須先建立 change proposal、design、tasks 與 capability specs，完成驗證後才進入實作與歸檔。

## 核心能力

- ESP32 與 MQTT 裝置接入
- 溫度、空氣濕度、土壤濕度、光照監控
- 農場、田區、作物批次與設備管理
- 即時 Dashboard、歷史趨勢與告警中心
- 水泵、風扇、閥門安全人工控制
- AI 異常偵測、預測分析與智慧推薦
- Producer、Merchant、Consumer 三套角色提示語與 JSON 快取
- 生產端、銷售端、消費端三套入口
- 農產品供應、採購需求、QR Code 追溯
- 裝置憑證、RBAC、Prompt Registry、稽核與安全治理

## 建議技術架構

| Layer | Technology |
|---|---|
| Core platform | PHP 8.3+ / Laravel 12+ |
| Web UI | Inertia.js / Vue 3 / TypeScript |
| Database | PostgreSQL 16+ |
| Cache and Queue | Redis 7+ |
| IoT transport | MQTT / EMQX or Mosquitto |
| AI service | Python 3.12+ / FastAPI |
| Edge device | ESP32 |
| Local environment | Docker Compose |

Laravel 負責帳號、權限、農場、設備、商業流程與資料一致性；MQTT Broker 負責裝置訊息；FastAPI 負責 AI 推論。AI 建議不得直接操作設備，任何控制命令都必須經過 Laravel 權限、安全限制與稽核流程。

## 完整規格入口

- [完整產品規格](docs/spec/COMPLETE_PRODUCT_SPEC.md)
- [邏輯資料模型](docs/spec/DATA_MODEL.md)
- [MVP 驗收矩陣](docs/spec/ACCEPTANCE_MATRIX.md)
- [完整 Capability 索引](openspec/changes/bootstrap-smart-agriculture-platform/SPECIFICATION_INDEX.md)
- [AI 開發治理規範](AGENTS.md)
- [專案與技術背景](openspec/project.md)
- [系統架構](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [第一階段 OpenSpec Proposal](openspec/changes/bootstrap-smart-agriculture-platform/proposal.md)
- [第一階段技術設計](openspec/changes/bootstrap-smart-agriculture-platform/design.md)
- [第一階段任務清單](openspec/changes/bootstrap-smart-agriculture-platform/tasks.md)

完整 OpenSpec change 現在涵蓋 17 個 capability：身分權限、組織多租戶、農務營運、裝置管理與生命週期、Telemetry、告警、設備命令、AI Insights、AI Orchestration、供應採購、追溯消費者、三方入口、通知、治理稽核、API 契約、資料治理與非功能需求。

## OpenSpec 開發流程

需使用 Node.js 20.19.0 以上。

```bash
npm install -g @fission-ai/openspec@latest
openspec init
openspec update
openspec list
```

AI 開發流程：

```text
/opsx:explore
/opsx:propose <change-name>
/opsx:apply
/opsx:verify
/opsx:archive
```

第一個實作 change：

```text
bootstrap-smart-agriculture-platform
```

## 預定 Repository 結構

```text
AiotInOne/
├── apps/platform/          # Laravel 核心平台
├── services/ai/            # FastAPI AI service
├── firmware/esp32/         # ESP32 範例與模擬器
├── infra/docker/           # Docker Compose 與服務設定
├── packages/contracts/     # API / MQTT JSON schemas
├── docs/                   # 產品、架構、API、安全與維運文件
└── openspec/               # 規格與 change 管理
```

## 目前狀態

完整產品與 Capability 規格已建立，尚未開始大量程式實作。下一步應由 Codex 先執行 OpenSpec CLI 初始化與驗證，再依 `tasks.md` 從開發環境、Identity、Organization、Farm、Device、Telemetry 順序實作。每一階段都必須對照 `ACCEPTANCE_MATRIX.md` 完成測試與驗收。
