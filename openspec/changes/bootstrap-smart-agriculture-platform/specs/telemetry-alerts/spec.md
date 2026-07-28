# Telemetry and Alerts Capability

## Purpose

定義 MQTT 感測資料接收、驗證、保存、查詢與告警生命週期。

### Requirement: Validated Telemetry Ingestion

系統 SHALL 接收經授權裝置發布的 telemetry，並在寫入正式量測資料前驗證 Topic、裝置身分、payload schema、量測類型與單位。

#### Scenario: Valid telemetry is received

- GIVEN 裝置憑證有效且 Topic 與裝置授權範圍一致
- AND payload 包含有效 message_id、recorded_at 與 readings
- WHEN ingestion worker 接收訊息
- THEN 系統 SHALL 保存正規化量測資料
- AND 更新該裝置的最新值快取與最後心跳

#### Scenario: Payload schema is invalid

- GIVEN 裝置已通過連線驗證
- BUT payload 缺少必要欄位或包含不支援單位
- WHEN ingestion worker 處理訊息
- THEN 系統 SHALL 拒絕寫入正式 readings
- AND 保存可追蹤的無效訊息紀錄

### Requirement: Idempotent Message Processing

系統 MUST 以裝置識別與 message_id 保證 telemetry 處理冪等性。

#### Scenario: Device retries the same message

- GIVEN 某裝置的 message_id 已成功處理
- WHEN Broker 再次送達相同裝置與 message_id 的訊息
- THEN 系統 SHALL 不建立重複量測資料
- AND 系統 SHALL 將此次處理標記為 duplicate

### Requirement: Time-Series Query

授權使用者 SHALL 能查詢最新值與指定期間的歷史趨勢，且查詢應優先使用適合的聚合資料。

#### Scenario: Producer views hourly trend

- GIVEN Producer 對指定農場具有檢視權限
- WHEN Producer 查詢最近七天的每小時土壤濕度
- THEN 系統 SHALL 回傳時間排序的聚合資料
- AND 回應 SHALL 包含量測單位與資料品質狀態

### Requirement: Alert Lifecycle

系統 SHALL 支援門檻、持續時間與裝置離線告警，並追蹤 active、acknowledged、resolved 狀態。

#### Scenario: Threshold remains exceeded

- GIVEN 土壤濕度下限規則設為 30% 且持續時間為 10 分鐘
- WHEN 有效量測連續 10 分鐘低於 30%
- THEN 系統 SHALL 建立一個 active 告警
- AND 相同規則與資源不得重複建立多個活動告警

#### Scenario: Reading returns to normal

- GIVEN 存在一個活動中的低土壤濕度告警
- WHEN 有效量測恢復到規則安全範圍
- THEN 系統 SHALL 將原告警更新為 resolved
- AND 記錄恢復時間與觸發恢復的量測
