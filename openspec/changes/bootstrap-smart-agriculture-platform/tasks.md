# Tasks: Bootstrap Smart Agriculture Platform

> 執行原則：必須依序完成；每一階段需通過測試與驗收才可進入下一階段。不得以刪除測試、略過授權、降低安全限制或硬編碼成功結果宣告完成。

## 0. OpenSpec and Repository Initialization

- [ ] 0.1 確認 Node.js 與 OpenSpec CLI 版本符合目前官方要求。
- [ ] 0.2 執行 `openspec init` 並啟用 Codex／目前 AI 工具整合。
- [ ] 0.3 執行 `openspec update`，保留並整合既有 `AGENTS.md` 治理規範。
- [ ] 0.4 執行 OpenSpec 結構與語法驗證，修正所有錯誤。
- [ ] 0.5 建立 `.editorconfig`、`.gitattributes`、`.gitignore` 與 Conventional Commits 規範。
- [ ] 0.6 閱讀 `SPECIFICATION_INDEX.md`、完整產品規格、資料模型與驗收矩陣。

### Acceptance

- [ ] OpenSpec 可列出 `bootstrap-smart-agriculture-platform` change。
- [ ] 所有 capability spec 可被 OpenSpec 正確解析。
- [ ] `openspec verify` 或目前版本等效驗證命令通過。

## 1. Development Environment

- [ ] 1.1 建立 `apps/platform` Laravel 12 專案。
- [ ] 1.2 建立 `services/ai` FastAPI 專案。
- [ ] 1.3 建立 `firmware/esp32` 模擬器與範例骨架。
- [ ] 1.4 建立 Docker Compose：nginx、php-fpm、queue、scheduler、PostgreSQL、Redis、MQTT Broker、FastAPI、Mailpit。
- [ ] 1.5 提供 `.env.example`，不得包含真實憑證。
- [ ] 1.6 建立 `make setup`、`make up`、`make test`、`make lint` 或等效跨平台命令。
- [ ] 1.7 為 Laravel、FastAPI、PostgreSQL、Redis 與 MQTT 建立 liveness/readiness。
- [ ] 1.8 在 README 補上本機啟動、停止、重置與除錯方式。

### Acceptance

- [ ] 新環境可依 README 從空白機器完成安裝。
- [ ] 單一命令可啟動完整服務。
- [ ] 所有必要服務 health checks 通過。
- [ ] AI Service 故障不會使核心平台 health 直接失敗。

## 2. Identity, Organization and Tenancy

- [ ] 2.1 建立 users、organizations、organization_members、organization_invitations、roles、permissions。
- [ ] 2.2 建立 Producer、Merchant、Consumer、Administrator 基本角色與細分治理角色。
- [ ] 2.3 建立註冊、登入、登出、忘記密碼與 Email 驗證。
- [ ] 2.4 建立組織建立、成員邀請、接受、撤銷與角色調整。
- [ ] 2.5 建立 active organization 切換。
- [ ] 2.6 建立後端 Policies、Middleware、Repository/Query scope。
- [ ] 2.7 防止移除組織最後一位 owner。
- [ ] 2.8 建立帳號與組織 suspended 狀態。
- [ ] 2.9 建立跨組織存取、IDOR、角色越權與邀請 Token 測試。
- [ ] 2.10 建立管理員與角色測試種子資料。

### Acceptance

- [ ] 四類角色登入後進入正確入口。
- [ ] Producer 無法讀寫其他組織農場。
- [ ] Merchant 無法操作農場設備。
- [ ] Consumer 無法讀取非公開追溯資料。
- [ ] 邀請 Token 單次使用且過期失效。
- [ ] 多組織切換不造成資料交叉。

## 3. Farm and Crop Operations

- [ ] 3.1 建立 farms、fields、crop_types、crop_varieties、crop_batches。
- [ ] 3.2 建立農場、田區、溫室 CRUD 與位置隱私欄位。
- [ ] 3.3 建立作物批次狀態機、生長階段與採收預估。
- [ ] 3.4 建立 farm_activities、input_products 與處理紀錄。
- [ ] 3.5 建立 harvest_records 與來源數量驗證。
- [ ] 3.6 建立 append-only crop_batch_events 與 correction event。
- [ ] 3.7 建立 Producer Dashboard 基本摘要。
- [ ] 3.8 建立資料隔離、狀態轉換與歷程測試。

### Acceptance

- [ ] Producer 可建立農場、田區與作物批次。
- [ ] 非法狀態轉換被拒絕。
- [ ] AI 建議不能未確認覆寫人工採收預估。
- [ ] 採收紀錄可建立 draft 供應批次並保留來源關聯。
- [ ] 公開資訊不包含精確敏感位置。

## 4. Device Registry and Lifecycle

- [ ] 4.1 建立 devices、sensor_channels、actuator_channels、device_credentials、device_calibrations。
- [ ] 4.2 建立裝置配發、一次性啟用、啟用、停用、撤銷與退役。
- [ ] 4.3 建立每裝置獨立憑證與祕密只顯示一次流程。
- [ ] 4.4 建立 MQTT Topic 與最小權限 ACL 產生規則。
- [ ] 4.5 建立 heartbeat、online/degraded/offline 狀態與離線門檻。
- [ ] 4.6 建立韌體版本盤點與最低支援版本警示。
- [ ] 4.7 建立校正紀錄、到期提醒與 data quality 標記。
- [ ] 4.8 建立憑證輪替與撤銷流程。
- [ ] 4.9 建立裝置生命週期與安全測試。

### Acceptance

- [ ] 每台裝置擁有獨立身分與 ACL。
- [ ] 啟用 Token 無法重複使用。
- [ ] 停用或撤銷裝置不能上傳資料。
- [ ] 裝置不能向其他農場 Topic 發布。
- [ ] 退役裝置不刪除歷史資料。

## 5. Telemetry Ingestion

- [ ] 5.1 建立共用 JSON Schema、MQTT Envelope 與版本規則。
- [ ] 5.2 建立 telemetry ingestion worker。
- [ ] 5.3 驗證 Topic、裝置身分、schema_version、payload、量測類型與單位。
- [ ] 5.4 依 `device_id + message_id` 去重。
- [ ] 5.5 建立 telemetry_messages、telemetry_readings 與必要索引。
- [ ] 5.6 建立 recorded_at/received_at 與資料時間品質判斷。
- [ ] 5.7 建立 latest-value Redis cache。
- [ ] 5.8 建立分鐘、小時與日聚合作業。
- [ ] 5.9 建立 invalid_messages 與 dead-letter 流程。
- [ ] 5.10 建立 ESP32 模擬器，可送四類感測值、心跳與錯誤案例。
- [ ] 5.11 建立單元、整合、冪等與基準壓力測試。

### Acceptance

- [ ] 模擬器可上傳溫度、空氣濕度、土壤濕度與光照。
- [ ] 重複訊息不重複寫入。
- [ ] 錯誤 Schema 或單位不污染正式 readings。
- [ ] 最新值在正常負載 10 秒內顯示。
- [ ] ingestion 可持續處理至少 100 msg/s 的 MVP 基準。

## 6. Dashboard, Alerts and Notifications

- [ ] 6.1 建立最新值卡片、裝置狀態與資料品質標記。
- [ ] 6.2 建立歷史趨勢 API 與聚合圖表。
- [ ] 6.3 建立 alert_rules、alert_events 與 notes。
- [ ] 6.4 支援上限、下限、持續時間與裝置離線規則。
- [ ] 6.5 建立 active、acknowledged、resolved 生命週期。
- [ ] 6.6 建立重複抑制、恢復事件與升級規則。
- [ ] 6.7 建立 notifications、notification_preferences、notification_deliveries。
- [ ] 6.8 建立站內通知、Email、重試與 provider 狀態。
- [ ] 6.9 建立 Dashboard、告警、通知授權與失敗測試。

### Acceptance

- [ ] 持續超標只建立一個 active alert。
- [ ] 數值恢復時更新原告警為 resolved。
- [ ] 無權限使用者不能確認或解除告警。
- [ ] 已離開組織的使用者不收到新通知。
- [ ] Email 故障不阻塞核心告警建立。

## 7. Safe Device Commands

- [ ] 7.1 建立 device_commands、command_results、emergency_stops。
- [ ] 7.2 建立水泵、風扇、閥門人工命令 API。
- [ ] 7.3 實作權限、安全狀態、最大執行時間、重啟間隔與有效期限。
- [ ] 7.4 實作 idempotency key 與一致性處理。
- [ ] 7.5 建立版本化 MQTT command/command-result 契約。
- [ ] 7.6 建立裝置端 expires_at、本地安全上限與斷線安全停止模擬。
- [ ] 7.7 建立 pending、published、acknowledged、succeeded、failed、expired、timeout、cancelled 狀態機。
- [ ] 7.8 建立 late result 與設備狀態重新同步。
- [ ] 7.9 建立農場與裝置層級 emergency stop。
- [ ] 7.10 建立完整稽核、通知與安全測試。

### Acceptance

- [ ] 重送相同冪等鍵不重複操作。
- [ ] 過期命令在平台與裝置端皆不得執行。
- [ ] 命令逾時更新狀態並通知操作者。
- [ ] emergency stop 阻止所有啟動命令。
- [ ] AI Service 無 MQTT 控制發布憑證。

## 8. AI Insights and Orchestration

- [ ] 8.1 建立 FastAPI health、version 與 inference endpoints。
- [ ] 8.2 建立 OpenAPI、request/response JSON Schema 與 Contract Tests。
- [ ] 8.3 實作規則＋基線模型異常偵測。
- [ ] 8.4 實作灌溉建議、採收日期與產量預測 Provider 介面。
- [ ] 8.5 建立 prompt_templates、ai_model_versions、ai_requests、ai_insights。
- [ ] 8.6 建立 Producer、Merchant、Consumer 三套提示語模板。
- [ ] 8.7 建立 Prompt draft、test、approved、active、retired 與回滾流程。
- [ ] 8.8 建立結構化輸出驗證與 invalid_output 修復/fallback。
- [ ] 8.9 建立 deterministic cache key、JSON cache 與失效規則。
- [ ] 8.10 建立模型路由、timeout、retry、fallback、circuit breaker。
- [ ] 8.11 建立 ai_usage_ledger，保存 Token、延遲、估算成本與 cache 狀態。
- [ ] 8.12 建立輸入最小化、敏感欄位過濾與 Provider 資料邊界。
- [ ] 8.13 建立 useful/not_useful/incorrect/unsafe 回饋與治理事件。
- [ ] 8.14 UI 清楚標示 AI 建議、模型時間與可信度。

### Acceptance

- [ ] 三方角色使用不同 Prompt 與輸出目的。
- [ ] 結果包含模型、版本、可信度與解釋。
- [ ] 不合法 JSON 不寫入正式 insight。
- [ ] 有效快取存在時不呼叫 LLM。
- [ ] 來源資料或 Prompt 版本變更使快取失效。
- [ ] 模型不可用時核心監控仍可用。
- [ ] Secret、完整個資與裝置憑證不傳入外部 Provider。

## 9. Three-Party Portals

- [ ] 9.1 完成 Producer Portal：農場、設備、監控、告警、AI、採收與供應。
- [ ] 9.2 完成 Merchant Portal：供應搜尋、採購需求、詢價、追溯與 AI 採購建議。
- [ ] 9.3 完成 Consumer Portal：公開商品、QR 追溯、季節、保存與料理建議。
- [ ] 9.4 完成 Administrator Portal：帳號、組織、裝置、告警、AI、稽核與設定。
- [ ] 9.5 建立 active organization 切換與角色導覽。
- [ ] 9.6 建立 360 px 以上響應式版面與控制防誤觸。
- [ ] 9.7 執行鍵盤操作、焦點與基本 WCAG 2.1 AA 檢查。
- [ ] 9.8 建立端到端關鍵流程測試。

### Acceptance

- [ ] 三方入口資訊架構與權限明確分離。
- [ ] 組織切換不造成資料洩漏。
- [ ] 公開頁不需登入，私有資料必須授權。
- [ ] 手機版主要流程無水平捲動，高風險控制需明確確認。

## 10. Marketplace and Traceability MVP

- [ ] 10.1 建立 products、product_lots、supply_offers。
- [ ] 10.2 Producer 由採收紀錄建立、驗證與發布供應批次。
- [ ] 10.3 建立 procurement_requests、supply_matches 與搜尋篩選。
- [ ] 10.4 建立 inquiries 與非正式詢價狀態。
- [ ] 10.5 建立 reservations、到期釋放與並行數量保護。
- [ ] 10.6 建立 traceability_events、correction event 與公開欄位白名單。
- [ ] 10.7 建立穩定 QR Code 公開 URL 與防枚舉速率限制。
- [ ] 10.8 建立環境聚合摘要、資料品質與位置模糊化。
- [ ] 10.9 建立 safety_notices，食安通知優先於 AI 推薦。
- [ ] 10.10 建立供應、並行保留、追溯隱私與公開頁 E2E 測試。

### Acceptance

- [ ] 發布量不得無理由超過來源採收量。
- [ ] 並行保留不得造成負庫存。
- [ ] 公開頁不洩漏聯絡資料、裝置 ID、憑證、精確位置或原始 telemetry。
- [ ] 下架或撤回批次顯示明確狀態。
- [ ] 有效食安通知優先顯示。

## 11. Administration, Audit and Data Governance

- [ ] 11.1 建立治理角色最小權限與後台 Policy。
- [ ] 11.2 建立 append-only audit_events 與敏感操作覆蓋。
- [ ] 11.3 建立 organization/account suspension 與恢復。
- [ ] 11.4 建立 configuration_versions、差異、核准與回滾。
- [ ] 11.5 建立 security_incidents 與嚴重度、指派、調查流程。
- [ ] 11.6 建立支援模式、原因、時效、遮罩與操作稽核。
- [ ] 11.7 建立資料分類與敏感欄位遮罩。
- [ ] 11.8 建立 retention jobs、data_holds 與清理報告。
- [ ] 11.9 建立 export_jobs、短效下載與匯出稽核。
- [ ] 11.10 建立備份、還原與隔離環境演練程序。

### Acceptance

- [ ] support_operator 無法修改安全與 AI 治理設定。
- [ ] 稽核事件不可由一般流程修改或刪除。
- [ ] 設定可查看版本、差異與回滾。
- [ ] 日誌與匯出不包含祕密明文。
- [ ] 保存鎖定資料不被 retention job 刪除。

## 12. API and Integration Contracts

- [ ] 12.1 建立 `/api/v1`、OpenAPI 與標準 error envelope。
- [ ] 12.2 建立分頁、篩選、排序白名單與大型查詢限制。
- [ ] 12.3 為高衝突資源建立 optimistic concurrency 或交易鎖定。
- [ ] 12.4 建立 MQTT Topic、Payload、版本與 DLQ 契約。
- [ ] 12.5 建立 Laravel/FastAPI request_id、Schema 與錯誤契約。
- [ ] 12.6 建立版本化 Domain Event envelope 與 Consumer 冪等。
- [ ] 12.7 將 JSON Schema 放入 `packages/contracts` 並建立產生/驗證命令。
- [ ] 12.8 建立 PHP、Python、ESP32 simulator 的 Contract Tests。

### Acceptance

- [ ] 不支援版本回傳明確錯誤與遷移資訊。
- [ ] API 錯誤不洩漏 stack trace 或敏感資料。
- [ ] MQTT 未知 Schema 不寫入正式資料。
- [ ] AI request_id 不一致時拒絕關聯為成功。
- [ ] 契約破壞性變更使測試失敗並阻止合併。

## 13. Quality, Security, Performance and Operations

- [ ] 13.1 建立 PHP、TypeScript、Python lint、formatter 與 static analysis。
- [ ] 13.2 建立 Unit、Feature、Integration、Contract、E2E 測試分層。
- [ ] 13.3 建立 correlation ID 與跨 HTTP/MQTT/Queue/AI/Command 追蹤。
- [ ] 13.4 建立結構化日誌與祕密遮罩測試。
- [ ] 13.5 建立 HTTP、Queue、MQTT、Device、Alert、AI、Command、Database 指標。
- [ ] 13.6 建立依賴漏洞掃描、祕密掃描與安全 Header。
- [ ] 13.7 建立登入限流、公開頁限流與常見 Web 安全測試。
- [ ] 13.8 執行 Dashboard API、聚合 API 與 100 msg/s ingestion 基準測試。
- [ ] 13.9 建立 RPO/RTO、備份、還原與事故文件。
- [ ] 13.10 建立 CI；Actions 額度不足時提供等效本機 Gate 命令。
- [ ] 13.11 更新 README、架構、資料模型、API、MQTT、安全與維運文件。

### Acceptance

- [ ] 最新值 API p95 ≤ 500 ms（基準環境）。
- [ ] 七天小時聚合 API p95 ≤ 1.5 秒。
- [ ] ingestion 持續 100 msg/s、錯誤率低於 1%。
- [ ] AI、Email 故障時核心功能可用或明確降級。
- [ ] lint、static analysis、tests、contracts 全部通過。

## 14. Final Verification and Archive

- [ ] 14.1 依 `docs/spec/ACCEPTANCE_MATRIX.md` 完成所有 P0 驗收。
- [ ] 14.2 未完成 P1 建立 Issue、風險與後續 change。
- [ ] 14.3 執行全部測試、靜態分析、安全與效能基準。
- [ ] 14.4 依 capability specs 逐項完成 Given／When／Then 驗收。
- [ ] 14.5 執行 OpenSpec verify，修正規格與實作漂移。
- [ ] 14.6 將已完成 capability 同步到 `openspec/specs/`。
- [ ] 14.7 產生完成報告、測試證據、已知限制與下一階段建議。
- [ ] 14.8 使用 `/opsx:archive` 歸檔 change。

### Final Definition of Done

- [ ] 所有 P0 驗收案例通過。
- [ ] 不存在被 skip 的安全、權限、Contract 或資料隔離測試。
- [ ] OpenAPI、JSON Schema、MQTT 契約與實作同步。
- [ ] 文件可讓新開發者從空白環境啟動並驗證系統。
- [ ] `openspec verify` 通過，change 可安全歸檔。
