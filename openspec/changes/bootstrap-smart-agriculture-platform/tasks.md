# Tasks: Bootstrap Smart Agriculture Platform

> 執行原則：依序完成；每一階段必須通過測試與驗收，才可進入下一階段。不得以刪除測試、略過授權或硬編碼假資料方式宣告完成。

## 0. OpenSpec and Repository Initialization

- [ ] 0.1 在本機安裝最新版 OpenSpec CLI，確認 Node.js 版本符合要求。
- [ ] 0.2 執行 `openspec init`，選擇 Codex／目前使用的 AI 工具整合。
- [ ] 0.3 執行 `openspec update`，保留本專案既有 `AGENTS.md` 治理規範並整合官方管理區塊。
- [ ] 0.4 執行 OpenSpec 驗證，修正所有結構與語法問題。
- [ ] 0.5 建立 `.editorconfig`、`.gitattributes`、`.gitignore` 與 Conventional Commits 規範。

## 1. Development Environment

- [ ] 1.1 建立 `apps/platform` Laravel 12 專案。
- [ ] 1.2 建立 `services/ai` FastAPI 專案。
- [ ] 1.3 建立 Docker Compose：nginx、php-fpm、queue、scheduler、PostgreSQL、Redis、MQTT Broker、FastAPI、Mailpit。
- [ ] 1.4 提供 `.env.example`，不得包含真實憑證。
- [ ] 1.5 建立 `make setup`、`make up`、`make test`、`make lint` 或等效跨平台指令。
- [ ] 1.6 建立 health checks，確認各服務可被 Compose 判定健康。
- [ ] 1.7 在 README 補上本機啟動與除錯方式。

### Acceptance

- [ ] 新環境可依 README 從空白機器完成安裝。
- [ ] 單一指令可啟動完整服務。
- [ ] Laravel、FastAPI、PostgreSQL、Redis 與 MQTT health checks 全部通過。

## 2. Identity and Access

- [ ] 2.1 建立 users、organizations、organization_members、roles/permissions 資料模型。
- [ ] 2.2 建立 Producer、Merchant、Consumer、Administrator 基本角色。
- [ ] 2.3 建立註冊、登入、登出、忘記密碼與電子郵件驗證。
- [ ] 2.4 建立後端 Policies 與 Middleware，不得只依前端選單限制。
- [ ] 2.5 建立角色導向的登入後首頁。
- [ ] 2.6 建立授權測試，涵蓋跨組織存取與角色越權。
- [ ] 2.7 建立管理員帳號與測試種子資料。

### Acceptance

- [ ] 四種角色登入後進入正確入口。
- [ ] Producer 無法讀取其他農場資料。
- [ ] Merchant 無法操作農場設備。
- [ ] Consumer 無法讀取非公開追溯資訊。

## 3. Farm and Crop Management

- [ ] 3.1 建立 farms、fields、crop_types、crop_batches 資料模型。
- [ ] 3.2 建立農場與田區 CRUD。
- [ ] 3.3 建立作物批次、種植日期、生長階段與預計採收日。
- [ ] 3.4 建立 Producer Dashboard 基本摘要。
- [ ] 3.5 建立輸入驗證與組織資料隔離。
- [ ] 3.6 建立 Feature Tests。

### Acceptance

- [ ] Producer 可建立農場、田區與作物批次。
- [ ] 所有資料均關聯正確 organization。
- [ ] 無權限帳號收到 403，而不是空白頁或前端隱藏。

## 4. Device Registry and Security

- [ ] 4.1 建立 devices、sensor_channels、actuator_channels、device_credentials 資料模型。
- [ ] 4.2 建立裝置註冊、啟用、停用與憑證輪替。
- [ ] 4.3 建立裝置最後心跳、韌體版本與在線狀態。
- [ ] 4.4 建立 MQTT Topic 與 ACL 產生規則。
- [ ] 4.5 建立裝置祕密只顯示一次的流程。
- [ ] 4.6 建立憑證雜湊或安全儲存策略。
- [ ] 4.7 建立裝置權限與撤銷測試。

### Acceptance

- [ ] 每台裝置擁有獨立身分。
- [ ] 停用裝置不能再上傳資料。
- [ ] 裝置不能向其他農場 Topic 發布訊息。

## 5. Telemetry Ingestion

- [ ] 5.1 建立共用 JSON Schema 與 MQTT 契約文件。
- [ ] 5.2 建立 telemetry ingestion worker。
- [ ] 5.3 驗證 Topic、裝置身分、payload 與單位。
- [ ] 5.4 依 `device_id + message_id` 去重。
- [ ] 5.5 建立 telemetry_readings 與必要索引。
- [ ] 5.6 建立 latest-value Redis cache。
- [ ] 5.7 建立分鐘與小時聚合作業。
- [ ] 5.8 建立無效訊息紀錄與 dead-letter 處理。
- [ ] 5.9 建立 ESP32 模擬器，可送出四類感測值。
- [ ] 5.10 建立 ingestion 單元、整合與壓力基線測試。

### Acceptance

- [ ] 模擬器可穩定上傳溫度、空氣濕度、土壤濕度與光照。
- [ ] 重複訊息不會重複寫入。
- [ ] 錯誤 payload 不會污染正式 readings。
- [ ] 最新值能在合理延遲內出現在 Dashboard。

## 6. Dashboard and Alerts

- [ ] 6.1 建立最新感測值卡片。
- [ ] 6.2 建立歷史趨勢 API 與圖表。
- [ ] 6.3 建立 alert_rules、alert_events、alert_notifications。
- [ ] 6.4 支援上限、下限、持續時間與裝置離線規則。
- [ ] 6.5 建立告警建立、確認、解除與註記流程。
- [ ] 6.6 建立站內通知，電子郵件列為可選通道。
- [ ] 6.7 建立告警重複抑制與恢復事件。
- [ ] 6.8 建立 Dashboard 與告警測試。

### Acceptance

- [ ] 門檻持續超標後只建立一個活動告警。
- [ ] 數值恢復時更新原告警並記錄恢復時間。
- [ ] 無權限使用者不能確認或解除告警。

## 7. Safe Device Commands

- [ ] 7.1 建立 device_commands 與 command_results。
- [ ] 7.2 建立水泵、風扇、閥門的人工命令 API。
- [ ] 7.3 實作權限、安全限制、有效期限與冪等鍵。
- [ ] 7.4 建立 MQTT command 與 command-result 契約。
- [ ] 7.5 建立裝置端模擬回報。
- [ ] 7.6 建立 pending、success、failed、timeout 狀態機。
- [ ] 7.7 建立完整稽核紀錄。
- [ ] 7.8 明確禁止 AI Service 直接發布命令。

### Acceptance

- [ ] 重送相同冪等鍵不會重複操作設備。
- [ ] 過期命令不得執行。
- [ ] 命令逾時會更新狀態並通知操作者。

## 8. AI Insights Service

- [ ] 8.1 建立 FastAPI health、version 與 inference endpoints。
- [ ] 8.2 建立 OpenAPI／JSON Schema 契約。
- [ ] 8.3 實作規則＋基線模型的異常偵測。
- [ ] 8.4 實作灌溉建議介面。
- [ ] 8.5 建立產量與採收預測的可替換 provider 介面。
- [ ] 8.6 建立 ai_insight_requests、ai_insights、ai_model_versions。
- [ ] 8.7 保存輸入摘要、結果、可信度、解釋與模型版本。
- [ ] 8.8 建立失敗、逾時、重試與 fallback。
- [ ] 8.9 建立 Laravel 與 FastAPI contract tests。
- [ ] 8.10 在 UI 清楚標示 AI 建議，不將其呈現為保證結果。

### Acceptance

- [ ] Laravel 可呼叫 AI Service 並保存完整結果。
- [ ] AI Service 無法取得 MQTT 發布設備命令的憑證。
- [ ] 模型不可用時，平台顯示明確狀態且不影響基本監控。

## 9. Three-Party Portals

- [ ] 9.1 完成 Producer Portal 導覽與主要頁面。
- [ ] 9.2 完成 Merchant Portal 的供應搜尋、批次檢視與採購需求雛形。
- [ ] 9.3 完成 Consumer Portal 的商品、產地與追溯頁。
- [ ] 9.4 建立三種角色專屬 AI 推薦卡片與提示內容。
- [ ] 9.5 建立 Administrator 後台的帳號、設備、告警與 AI 執行紀錄頁。
- [ ] 9.6 建立響應式版面與基本無障礙檢查。
- [ ] 9.7 建立端到端關鍵流程測試。

### Acceptance

- [ ] 三方入口在資訊架構與操作權限上明確分離。
- [ ] 使用者切換組織時資料不會交叉洩漏。
- [ ] 公開頁不要求登入，私有資料必須經授權。

## 10. Marketplace and Traceability MVP

- [ ] 10.1 建立 products、product_lots、supply_offers。
- [ ] 10.2 Producer 可由作物批次建立供應批次。
- [ ] 10.3 Merchant 可搜尋與查看供應批次。
- [ ] 10.4 建立 traceability_events 與公開欄位白名單。
- [ ] 10.5 建立 QR Code 公開追溯 URL。
- [ ] 10.6 Consumer 可查看產地、作物、採收日與經允許的環境摘要。
- [ ] 10.7 建立追溯隱私與越權測試。

### Acceptance

- [ ] 公開追溯頁不洩漏農民聯絡方式、設備 ID 或精確敏感位置。
- [ ] 下架批次依規格顯示不可購買，但歷史追溯仍可依政策查看。

## 11. Quality, Security, and Operations

- [ ] 11.1 建立 PHP、TypeScript、Python lint 與格式化。
- [ ] 11.2 建立單元、Feature、Integration、Contract、E2E 測試分層。
- [ ] 11.3 建立 correlation ID 與結構化日誌。
- [ ] 11.4 建立 Queue、MQTT ingestion、AI latency 與錯誤率監控指標。
- [ ] 11.5 建立備份、還原與資料保存文件。
- [ ] 11.6 建立威脅模型與安全檢查清單。
- [ ] 11.7 建立 CI；Actions 額度不足時提供等效本機驗證命令。
- [ ] 11.8 執行依賴漏洞掃描與祕密掃描。
- [ ] 11.9 更新 README、架構、API、MQTT 與操作文件。

## 12. Final Verification and Archive

- [ ] 12.1 執行全部測試與靜態檢查。
- [ ] 12.2 依 capability specs 逐項完成 Given／When／Then 驗收。
- [ ] 12.3 執行 OpenSpec verify。
- [ ] 12.4 修正規格與實作漂移。
- [ ] 12.5 將已完成 capability 同步到 `openspec/specs/`。
- [ ] 12.6 使用 `/opsx:archive` 歸檔 change。
- [ ] 12.7 產生完成報告、已知限制與下一階段 change 建議。
