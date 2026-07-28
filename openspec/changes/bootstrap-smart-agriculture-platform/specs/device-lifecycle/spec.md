# Device Lifecycle Capability

## Purpose

定義 Gateway、Sensor 與 Actuator 從配發、註冊、啟用、心跳、校正、韌體管理到撤銷與退役的完整生命週期。

### Requirement: Device Provisioning

系統 SHALL 為每台裝置產生唯一 device identifier 與獨立憑證。裝置祕密 MUST 只在建立或輪替時顯示一次。

#### Scenario: New ESP32 is provisioned

- GIVEN Producer 具有農場設備管理權限
- WHEN Producer 建立 ESP32 裝置
- THEN 系統 SHALL 建立 pending 裝置
- AND SHALL 產生一次性啟用資料
- AND SHALL 建立僅允許該裝置 Topic 的 MQTT ACL

#### Scenario: Provisioning token is reused

- GIVEN 啟用 Token 已成功使用
- WHEN 任一客戶端再次提交相同 Token
- THEN 系統 SHALL 拒絕啟用
- AND SHALL 記錄安全事件

### Requirement: Device Type and Channel Model

每台裝置 SHALL 宣告類型、型號、硬體版本、韌體版本與能力；Sensor Channel SHALL 定義 measurement type、unit、範圍與校正資料；Actuator Channel SHALL 定義可允許狀態與安全限制。

#### Scenario: Unsupported measurement unit is configured

- GIVEN channel type 為 soil_moisture
- WHEN 使用者設定不受支援的單位
- THEN 系統 SHALL 拒絕設定
- AND SHALL 回傳允許的標準單位

### Requirement: Heartbeat and Connectivity State

裝置 SHALL 定期發布 heartbeat。系統 SHALL 依最後心跳與可配置門檻計算 online、degraded、offline、disabled 狀態。

#### Scenario: Device stops sending heartbeat

- GIVEN 裝置原為 online
- WHEN 最後心跳超過 offline threshold
- THEN 系統 SHALL 標記為 offline
- AND MAY 建立單一活動中的離線告警

### Requirement: Calibration Management

Producer SHALL 能記錄感測通道校正日期、方法、參考值、偏移量、操作者與下次校正日期。

#### Scenario: Expired calibration affects data quality

- GIVEN 感測器已超過下次校正日期
- WHEN 系統接收其 telemetry
- THEN 系統 SHALL 保存資料
- AND SHALL 將 data quality 標記為 calibration_due
- AND Dashboard SHALL 顯示校正提醒

### Requirement: Firmware Inventory

系統 SHALL 保存裝置韌體版本、最後更新時間與相容性狀態。MVP MAY 只提供版本盤點，不要求 OTA 更新。

#### Scenario: Unsupported firmware reports heartbeat

- GIVEN 裝置韌體版本低於最低支援版本
- WHEN 系統收到 heartbeat
- THEN 系統 SHALL 將裝置標記為 degraded
- AND SHALL 建立升級建議
- AND MUST NOT 未經獨立規格自動推送韌體

### Requirement: Credential Rotation and Revocation

授權使用者 SHALL 能輪替或撤銷裝置憑證，舊憑證在生效切換後 MUST 無法連線或發布訊息。

#### Scenario: Compromised device credential is revoked

- GIVEN 管理員判定裝置憑證外洩
- WHEN 管理員撤銷憑證
- THEN Broker ACL SHALL 阻止後續連線或發布
- AND 系統 SHALL 保留裝置歷史資料
- AND SHALL 記錄撤銷原因與操作者

### Requirement: Device Retirement

退役裝置 SHALL 停止接收資料與命令，但歷史 telemetry、告警與稽核紀錄 MUST 保留並可追溯。

#### Scenario: Retired device is deleted from UI

- GIVEN 裝置已產生歷史資料
- WHEN 使用者選擇退役
- THEN 系統 SHALL 執行邏輯退役而非破壞性刪除
- AND SHALL 撤銷其憑證與命令能力
