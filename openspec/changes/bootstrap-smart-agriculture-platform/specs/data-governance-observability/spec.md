# Data Governance and Observability Capability

## Purpose

定義資料分類、保存、刪除、備份、還原、日誌、指標、追蹤與營運告警。

### Requirement: Data Classification

系統 SHALL 將資料至少分類為 public、internal、confidential、secret。裝置憑證、密碼與 Token MUST 分類為 secret；精確位置、個資與內部農務成本 SHALL 至少為 confidential。

#### Scenario: Secret field is logged

- GIVEN request 或 payload 含有裝置祕密
- WHEN 系統產生日誌
- THEN logger MUST 遮罩或移除祕密
- AND SHOULD 建立自動化測試防止敏感欄位外洩

### Requirement: Configurable Retention

資料保存週期 SHALL 可配置並依資料類型執行。初始政策：原始 payload 30 天、高頻 readings 180 天、分鐘與小時聚合 2 年、日聚合與追溯事件長期保存、稽核紀錄至少 1 年。

#### Scenario: Raw payload reaches retention age

- GIVEN 原始 payload 已超過保存期限
- WHEN retention job 執行
- THEN 系統 SHALL 安全刪除或匿名化該 payload
- AND SHALL 保留必要聚合與處理證據
- AND SHALL 記錄清理數量與結果

### Requirement: Legal and Operational Hold

治理人員 SHALL 能對特定安全事件、稽核範圍或追溯批次設定保留鎖定，避免一般保存工作刪除相關資料。

#### Scenario: Incident data is under hold

- GIVEN 安全事件仍在調查
- WHEN retention job 處理關聯資料
- THEN 系統 SHALL 跳過刪除
- AND SHALL 記錄 hold reference

### Requirement: Backup and Restore

PostgreSQL、關鍵設定與必要 Object Storage SHALL 定期備份。系統 SHALL 定義 RPO、RTO 並定期執行還原演練。

#### Scenario: Restore drill is performed

- GIVEN 有可用備份
- WHEN 維運人員在隔離環境執行還原
- THEN 系統 SHALL 驗證資料完整性、Schema 版本與關鍵流程
- AND SHALL 保存演練時間、耗時、缺失與改善事項

### Requirement: Correlation and Traceability

HTTP request、MQTT message、Queue event、AI request、alert 與 device command SHALL 使用 correlation ID 或可鏈結識別，支援跨服務追蹤。

#### Scenario: AI recommendation creates a user notification

- GIVEN AI request 完成並建立 insight
- WHEN notification worker 發送通知
- THEN 管理員 SHALL 能由 notification 追蹤至 insight、AI request、Prompt 與來源資料摘要

### Requirement: Structured Logging

服務 SHALL 使用結構化日誌，至少包含 timestamp、level、service、environment、correlation_id、event、result。正式環境 MUST NOT 回傳 stack trace 給一般使用者。

#### Scenario: Telemetry validation fails

- GIVEN ingestion 收到不合法 payload
- WHEN 驗證失敗
- THEN 系統 SHALL 記錄 device、message_id、error code 與 schema version
- AND MUST NOT 記錄裝置祕密

### Requirement: Operational Metrics

平台 SHALL 提供 HTTP latency/error rate、Queue backlog、MQTT ingestion lag、invalid payload rate、device offline count、alert backlog、AI latency/error/cost、command timeout rate 與 database health 等指標。

#### Scenario: Ingestion lag exceeds threshold

- GIVEN MQTT 訊息等待處理時間持續超標
- WHEN 監控規則觸發
- THEN 系統 SHALL 通知維運人員
- AND SHALL 提供 queue depth、consumer health 與最近部署版本

### Requirement: Health and Readiness

每個服務 SHALL 提供 liveness 與 readiness。Readiness MUST 驗證必要依賴，但不得因非關鍵外部 AI Provider 故障使核心監控服務完全不可用。

#### Scenario: AI provider is unavailable

- GIVEN Laravel、Database、Redis 與 MQTT 正常
- AND 外部 AI Provider 故障
- WHEN readiness 執行
- THEN 核心平台 SHALL 維持 ready 或 degraded
- AND AI capability SHALL 顯示 unavailable

### Requirement: Data Subject and Account Export

授權使用者 SHALL 能依政策申請其帳號與組織資料匯出。匯出 MUST 經權限檢查、遮罩、短效下載與稽核。

#### Scenario: Producer requests organization export

- GIVEN Producer owner 具有匯出權限
- WHEN 建立匯出工作
- THEN 系統 SHALL 非同步產生允許範圍資料
- AND MUST NOT 包含裝置祕密或其他租戶資料
