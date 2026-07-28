# AiotInOne 完整規格索引

本文件是 `bootstrap-smart-agriculture-platform` 的總入口。此 change 定義智慧農業 AIoT 三方平台 MVP 的完整產品、技術、安全與驗收邊界。

## 1. 系統定位

AiotInOne 以 Laravel 作為商業核心，整合 ESP32、MQTT、PostgreSQL、Redis 與 FastAPI AI Service，服務：

- Producer：農民、農場管理者、合作社。
- Merchant：採購商、通路商、零售商。
- Consumer：一般消費者。
- Administrator：平台治理角色，不列入商業三方。

## 2. Capability Map

| Capability | 規格檔 | MVP 目標 |
|---|---|---|
| Identity & Access | `specs/identity-access/spec.md` | 登入、RBAC、組織隔離、裝置身分 |
| Organization & Tenancy | `specs/organization-tenancy/spec.md` | 組織、成員、邀請、資料範圍 |
| Farm Operations | `specs/farm-operations/spec.md` | 農場、田區、作物批次、農務紀錄 |
| Farm & Device Management | `specs/farm-device-management/spec.md` | 裝置登錄、通道與安全資料 |
| Device Lifecycle | `specs/device-lifecycle/spec.md` | 配發、心跳、校正、韌體與撤銷 |
| Telemetry & Alerts | `specs/telemetry-alerts/spec.md` | MQTT ingestion、去重、趨勢、告警 |
| Device Command Control | `specs/device-command-control/spec.md` | 人工控制、冪等、逾時、安全停止 |
| AI Insights | `specs/ai-insights/spec.md` | 異常、預測、推薦與模型版本 |
| AI Orchestration | `specs/ai-orchestration/spec.md` | 三方提示語、快取、fallback、成本紀錄 |
| Marketplace & Procurement | `specs/marketplace-procurement/spec.md` | 供應批次、採購需求、媒合 |
| Traceability & Consumer | `specs/traceability-consumer/spec.md` | QR 追溯、公開欄位、商品推薦 |
| Three-Party Platform | `specs/three-party-platform/spec.md` | 三方入口與治理後台資訊架構 |
| Notifications | `specs/notifications/spec.md` | 站內、Email、事件偏好與重試 |
| Administration & Audit | `specs/administration-audit/spec.md` | 管理、稽核、安全事件與設定版本 |
| API & Integration Contracts | `specs/api-integration-contracts/spec.md` | REST、MQTT、AI 契約、版本與錯誤格式 |
| Data Governance & Observability | `specs/data-governance-observability/spec.md` | 保存、備份、監控、追蹤與隱私 |
| Nonfunctional Requirements | `specs/nonfunctional-requirements/spec.md` | 效能、可靠性、無障礙、相容性與復原 |

## 3. 核心限制

1. Laravel 是權限、資料一致性與設備控制的唯一商業決策中心。
2. AI Service MUST NOT 持有 MQTT 控制 Topic 的發布憑證。
3. AI 建議預設需人工確認，不得直接操作水泵、風扇或閥門。
4. 每台 IoT 裝置必須有獨立、可撤銷、可輪替的身分。
5. 所有 API、MQTT payload 與 AI request/response 必須版本化。
6. 所有時間以 UTC 儲存，前端預設以 `Asia/Taipei` 顯示。
7. 所有跨組織資料存取必須由後端 Policy 阻擋並留下稽核紀錄。

## 4. MVP 驗收主流程

1. Producer 建立組織、農場、田區與作物批次。
2. Producer 配發 ESP32 裝置並取得一次性裝置憑證。
3. 裝置透過 MQTT 上傳溫度、空氣濕度、土壤濕度與光照。
4. 系統驗證、去重、保存並在 Dashboard 顯示最新值與趨勢。
5. 規則超標建立告警，Producer 可確認與解除。
6. Producer 可送出受安全限制保護的人工設備命令。
7. Laravel 呼叫 FastAPI 產生異常、預測與推薦，保存模型版本與解釋。
8. Producer 建立供應批次，Merchant 查看並建立採購需求。
9. Consumer 掃描 QR Code 查看公開追溯資訊與角色專屬推薦。
10. Administrator 可稽核組織、裝置、AI、告警與控制命令。

## 5. 完成定義

Capability 只有在下列條件全部成立時才可標記完成：

- 對應 Requirement 與 Scenario 已實作。
- 單元、Feature、Integration 或 Contract 測試通過。
- 權限、資料隔離與失敗路徑已驗證。
- API／MQTT／AI 契約文件已同步。
- 日誌、指標與稽核事件可追蹤。
- `openspec verify` 通過且無規格漂移。
