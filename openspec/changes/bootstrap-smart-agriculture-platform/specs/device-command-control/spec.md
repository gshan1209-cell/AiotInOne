# Device Command Control Capability

## Purpose

定義水泵、風扇、閥門等控制設備的人工命令、安全限制、MQTT 契約、狀態機、稽核與緊急停止。

### Requirement: Authorized Manual Command

MVP SHALL 僅允許具備指定農場設備控制權限的使用者建立命令。每次命令 MUST 保存操作者、組織、農場、裝置、通道、目標狀態、原因、建立時間、有效期限與 idempotency key。

#### Scenario: Producer turns on a pump

- GIVEN Producer 對水泵具有控制權限
- AND 水泵狀態允許操作
- WHEN Producer 提交有效啟動命令
- THEN Laravel SHALL 建立 pending command
- AND SHALL 通過安全檢查後發布至該裝置 command Topic
- AND UI SHALL 顯示等待設備回報狀態

#### Scenario: Merchant attempts actuator control

- GIVEN 使用者只有 Merchant 角色
- WHEN 使用者呼叫控制 API
- THEN 系統 SHALL 回傳 403
- AND SHALL 記錄被拒絕的操作事件

### Requirement: Safety Limits

每個 Actuator Channel MUST 定義允許狀態、安全預設、最長連續執行時間、最短重啟間隔與命令有效期限。

#### Scenario: Pump duration exceeds limit

- GIVEN 水泵最長連續執行時間為 15 分鐘
- WHEN 使用者要求啟動 30 分鐘
- THEN 系統 SHALL 拒絕命令
- AND SHALL 說明違反的安全限制

#### Scenario: Rapid restart is requested

- GIVEN 水泵剛停止且最短重啟間隔尚未結束
- WHEN 使用者再次啟動
- THEN 系統 SHALL 拒絕或延後命令
- AND SHALL 顯示可再次操作時間

### Requirement: Idempotent Command Processing

系統 MUST 以 organization、device、channel 與 idempotency key 保證命令建立與執行冪等。

#### Scenario: Client retries the same request

- GIVEN 相同 idempotency key 已建立命令
- WHEN Client 因網路錯誤重送請求
- THEN 系統 SHALL 回傳原命令
- AND MUST NOT 再次發布控制訊息

### Requirement: Command State Machine

命令狀態 SHALL 至少包含 pending、published、acknowledged、succeeded、failed、expired、timeout、cancelled，且狀態轉換 MUST 可追蹤。

#### Scenario: Device does not acknowledge

- GIVEN 命令已發布
- WHEN acknowledgment timeout 到期
- THEN 系統 SHALL 將命令標記為 timeout
- AND SHALL 通知操作者
- AND SHALL NOT 假設設備已成功執行

#### Scenario: Late success arrives after timeout

- GIVEN 命令已標記 timeout
- WHEN 裝置稍後回報實際成功
- THEN 系統 SHALL 保存 late result
- AND SHALL 顯示狀態不一致警示
- AND SHALL 觸發設備狀態重新同步

### Requirement: Signed and Scoped MQTT Command

命令 payload SHALL 包含 schema version、command_id、channel、action、parameters、issued_at、expires_at 與完整性驗證資料。Broker ACL MUST 僅允許授權服務發布與指定裝置訂閱。

#### Scenario: Expired command reaches device

- GIVEN 裝置收到 expires_at 已過期的命令
- WHEN 裝置驗證 payload
- THEN 裝置 MUST 拒絕執行
- AND SHALL 發布 expired command result

### Requirement: Local Safety and Fail-Safe

裝置端 MUST 具有本地安全上限與斷線安全預設；雲端命令不得繞過硬體保護。

#### Scenario: Broker connection is lost while pump is running

- GIVEN 水泵因有效命令啟動
- WHEN 裝置與 Broker 斷線且達本地安全上限
- THEN 裝置 MUST 自動切換到安全停止狀態
- AND SHALL 在恢復連線後回報事件

### Requirement: Emergency Stop

授權 Producer 與 Administrator SHALL 能啟動農場或裝置層級緊急停止。緊急停止 MUST 優先於一般命令並阻止新啟動命令，直到明確解除。

#### Scenario: Emergency stop is active

- GIVEN 農場 emergency stop 已啟用
- WHEN 任一使用者或服務提出啟動 Actuator 的命令
- THEN 系統 SHALL 拒絕命令
- AND SHALL 回傳 emergency stop 狀態

### Requirement: AI Separation

AI Service MUST NOT 發布、建立或批准設備命令。AI 輸出只能建立 recommendation，由 Laravel 及授權使用者決定是否轉換為命令。

#### Scenario: AI recommends irrigation

- GIVEN AI 建議灌溉 10 分鐘
- WHEN 建議寫入平台
- THEN 系統 SHALL 顯示建議、依據與可信度
- AND SHALL 要求授權使用者確認
- AND MUST NOT 自動啟動水泵
