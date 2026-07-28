# API and Integration Contracts Capability

## Purpose

定義 REST API、MQTT Topic、事件、AI Service 與錯誤回應的版本化契約，避免 PHP、ESP32 與 Python 服務各自演進。

### Requirement: Versioned REST API

所有外部與前後端 API SHALL 使用 `/api/v1` 或等效版本標識。破壞性變更 MUST 建立新版本，不得在既有版本靜默改變欄位語意。

#### Scenario: Client calls a supported endpoint

- GIVEN Client 使用支援中的 API 版本
- WHEN 請求有效資源
- THEN 系統 SHALL 回傳版本化 JSON
- AND SHALL 包含 correlation ID

#### Scenario: Client calls an unsupported version

- GIVEN Client 呼叫已停用版本
- WHEN 系統接收請求
- THEN 系統 SHALL 回傳明確版本錯誤
- AND SHOULD 提供支援版本與遷移資訊

### Requirement: Standard Error Envelope

API 錯誤 SHALL 使用一致格式，至少包含 `code`、`message`、`correlation_id`，驗證錯誤 SHALL 包含欄位層級 details。

#### Scenario: Validation fails

- GIVEN Client 提交不合法的 command duration
- WHEN API 驗證失敗
- THEN 回應 SHALL 使用 422
- AND SHALL 提供穩定 error code
- AND SHALL 指出欄位與限制，不回傳敏感堆疊資訊

### Requirement: Pagination, Filtering and Sorting

集合型 API SHALL 支援明確分頁。允許的篩選與排序欄位 MUST 使用白名單，避免任意 SQL 欄位注入。

#### Scenario: Large telemetry query is requested

- GIVEN 使用者查詢超大時間範圍
- WHEN 請求超過同步查詢限制
- THEN 系統 SHALL 要求縮小範圍、使用聚合粒度或建立非同步匯出
- AND MUST NOT 無限制回傳原始資料

### Requirement: Optimistic Concurrency

高衝突資源如設定、供應量與裝置命令 SHOULD 使用版本欄位、ETag 或資料庫鎖定避免遺失更新。

#### Scenario: Two users edit an alert rule

- GIVEN 兩位使用者讀取相同版本
- WHEN 第一位已成功儲存，第二位再提交舊版本
- THEN 系統 SHALL 拒絕第二次覆寫
- AND SHALL 回傳 conflict 與最新版本資訊

### Requirement: MQTT Topic Contract

MQTT Topic SHALL 使用：

`aiotinone/v1/{organization_id}/{farm_id}/{device_id}/{message_type}`

`message_type` 至少包含 telemetry、status、command、command-result。Topic 中的識別 MUST 與憑證 ACL 一致。

#### Scenario: Device publishes to another farm

- GIVEN Device A 綁定 Farm A
- WHEN Device A 發布至 Farm B Topic
- THEN Broker MUST 拒絕發布
- AND 系統 SHALL 記錄安全事件

### Requirement: MQTT Payload Envelope

所有 MQTT payload SHALL 包含 `schema_version`、`message_id`、`device_id`、`recorded_at`。Command 與結果另 SHALL 包含 `command_id` 與 `expires_at` 或 result metadata。

#### Scenario: Unsupported schema version arrives

- GIVEN ingestion 收到未知 schema_version
- WHEN 處理訊息
- THEN 系統 SHALL 拒絕寫入正式資料
- AND SHALL 保存 invalid message metadata
- AND MAY 導向 dead-letter 流程

### Requirement: AI Service Contract

Laravel 與 FastAPI 間 SHALL 使用版本化 OpenAPI 與 JSON Schema。每次請求 MUST 有 request_id、insight_type、subject、features；每次成功回應 MUST 有 model、model_version、result、confidence、explanation 與 generated_at。

#### Scenario: Request and response IDs differ

- GIVEN Laravel 發送 request_id A
- WHEN AI Service 回傳 request_id B
- THEN Laravel SHALL 拒絕將結果關聯為成功
- AND SHALL 記錄 contract violation

### Requirement: Domain Event Contract

跨模組事件 SHALL 具有 event_id、event_type、event_version、occurred_at、organization_id、correlation_id 與 payload。Consumer MUST 對重複 event_id 冪等處理。

#### Scenario: Queue redelivers an event

- GIVEN event_id 已成功處理
- WHEN Queue 再次傳遞相同事件
- THEN Consumer SHALL 不重複建立通知或副作用
- AND SHALL 記錄 duplicate delivery

### Requirement: Contract Testing

PHP、Python、MQTT simulator 與共用 Schema SHALL 具備自動化 Contract Tests。契約變更未通過 Consumer 相容測試時 MUST 不得合併。

#### Scenario: AI response removes a required field

- GIVEN FastAPI 修改回應 Schema 移除 `model_version`
- WHEN Contract Tests 執行
- THEN 測試 MUST 失敗
- AND 變更 SHALL 先建立新版本或遷移計畫
