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
- AI 異常偵測、預測分析與智慧推薦
- 生產端、銷售端、消費端三套入口
- 農產品供應批次與 QR Code 追溯
- 裝置憑證、RBAC、命令稽核與安全控制

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

## 文件入口

- [AI 開發治理規範](AGENTS.md)
- [專案與技術背景](openspec/project.md)
- [系統架構](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [第一階段 OpenSpec Proposal](openspec/changes/bootstrap-smart-agriculture-platform/proposal.md)
- [第一階段技術設計](openspec/changes/bootstrap-smart-agriculture-platform/design.md)
- [第一階段任務清單](openspec/changes/bootstrap-smart-agriculture-platform/tasks.md)

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
├── docs/                   # 架構、API、安全與維運文件
└── openspec/               # 規格與 change 管理
```

## 目前狀態

目前已完成第一階段架構設計與 OpenSpec change 草案，尚未開始大量程式實作。下一步應由 Codex 依 `tasks.md` 從 OpenSpec 初始化、本機開發環境與 Laravel/FastAPI 骨架開始執行。
