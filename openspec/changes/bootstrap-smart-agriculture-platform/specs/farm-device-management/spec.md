# Farm and Device Management Capability

## Purpose

定義農場、田區、作物批次、感測器與控制設備的管理行為。

### Requirement: Farm Structure Management

Producer SHALL 能在其組織範圍內建立與管理農場、田區及作物批次。

#### Scenario: Producer creates a crop batch

- GIVEN Producer 對指定田區具有管理權限
- WHEN Producer 提交有效的作物、種植日期與生長資訊
- THEN 系統 SHALL 建立作物批次
- AND 作物批次 SHALL 關聯正確組織、農場與田區

#### Scenario: Producer uses an unauthorized field

- GIVEN 田區不屬於 Producer 可管理的組織
- WHEN Producer 嘗試在該田區建立作物批次
- THEN 系統 SHALL 拒絕操作並回傳 403

### Requirement: Device Registration

Producer SHALL 能將 Sensor、Gateway 與 Actuator 註冊到其被授權農場，且系統 MUST 保存裝置狀態、韌體版本、最後心跳與憑證狀態。

#### Scenario: Registering a new sensor device

- GIVEN Producer 對農場具有設備管理權限
- WHEN Producer 建立一台新感測裝置
- THEN 系統 SHALL 產生唯一 device identifier
- AND 系統 SHALL 建立獨立裝置憑證
- AND 裝置祕密 SHALL 僅在建立或輪替時顯示一次

#### Scenario: Device heartbeat becomes stale

- GIVEN 裝置最後心跳超過離線門檻
- WHEN 系統執行裝置狀態評估
- THEN 裝置 SHALL 被標記為 offline
- AND 系統 MAY 依規則建立離線告警

### Requirement: Actuator Safety Metadata

每個控制通道 MUST 定義可允許狀態、安全預設、最長執行時間與命令有效期限。

#### Scenario: Command exceeds configured duration

- GIVEN 水泵控制通道的最長執行時間為 15 分鐘
- WHEN 使用者請求執行 30 分鐘
- THEN 系統 SHALL 拒絕命令
- AND 回應 SHALL 說明違反安全限制
