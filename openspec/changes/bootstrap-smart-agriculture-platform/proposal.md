# Change Proposal: Bootstrap Smart Agriculture Platform

## Why

AiotInOne 目前是空白 repository，尚無可執行系統、技術骨架與正式規格。第一階段需要先建立可持續演進的 AIoT 共用核心，並以智慧農業三方平台作為首個落地產品。

若直接進入畫面或裝置程式開發，容易產生下列問題：

- 生產端、銷售端與消費端的權限與資料邊界不清。
- PHP、MQTT、ESP32 與 Python AI 服務缺乏穩定契約。
- AI 建議與設備控制混用，造成安全風險。
- 需求只存在聊天紀錄，後續 Codex 實作容易漂移。

因此，本 change 先定義 MVP 的技術骨架、角色模型、IoT 資料流、AI 邊界與驗收任務，再進入程式實作。

## What Changes

本 change 將建立：

1. Laravel 模組化單體專案骨架。
2. PostgreSQL、Redis、MQTT Broker 與 Python FastAPI 的 Docker Compose 開發環境。
3. Producer、Merchant、Consumer、Administrator 四類權限角色。
4. 農場、田區、作物批次、設備與感測通道資料模型。
5. MQTT telemetry ingestion、資料驗證、去重與保存流程。
6. 即時儀表板、歷史趨勢與基本告警中心。
7. AI Insights 服務契約，整合異常偵測、預測分析與智慧推薦。
8. 生產端、銷售端、消費端三套入口與治理後台。
9. 農產品批次與基本追溯頁。
10. 測試、稽核、可觀測性與安全基線。

## Scope

### In Scope

- 單一部署環境的 MVP。
- 基本組織與角色權限。
- ESP32 模擬器與實機皆可使用的 MQTT 契約。
- 溫度、空氣濕度、土壤濕度、光照四類資料。
- 水泵、風扇、閥門的命令資料模型，但預設僅允許人工操作。
- 規則型告警。
- AI Service 的可替換介面與最小可用推論範例。
- 三方角色專屬 Dashboard 與導覽。

### Out of Scope

- 正式金流與複雜物流。
- AI 完全自主控制設備。
- 無人機、衛星與農作物影像辨識。
- 區塊鏈追溯。
- 大規模多區域高可用。
- 完整 SaaS 計費與方案管理。

## Impact

### New Components

- `apps/platform`：Laravel 核心平台。
- `services/ai`：Python FastAPI AI 推論服務。
- `firmware/esp32`：裝置範例與模擬資料格式。
- `infra/docker`：本機開發基礎設施。
- `docs/api`：API 與 MQTT 契約。

### Data

新增使用者、組織、農場、田區、作物批次、設備、感測通道、量測資料、告警、AI 結果、產品批次與追溯事件等資料表。

### Security

新增 RBAC、裝置獨立身分、MQTT ACL、遠端命令稽核與 AI 建議安全邊界。

## Success Criteria

- 新開發者可用單一指令啟動完整本機環境。
- 四類角色登入後只能看到被授權功能與資料。
- 模擬 ESP32 能連續上傳四類感測值。
- 農民能在 Dashboard 查看最新資料與歷史趨勢。
- 門檻超標能建立告警事件並顯示處理狀態。
- Laravel 能呼叫 AI Service 並保存帶有模型版本與可信度的結果。
- 商家能查看可供應批次；消費者能查看公開追溯頁。
- 測試與規格驗證全部通過。
