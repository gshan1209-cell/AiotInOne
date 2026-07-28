# Notifications Capability

## Purpose

定義告警、裝置、AI、採購與治理事件的站內通知、Email 通知、偏好、重試、去重與可追蹤性。

### Requirement: Event-Driven Notification

系統 SHALL 由版本化 Domain Event 建立通知，不得由畫面直接拼接不可追蹤的通知內容。

#### Scenario: Critical alert is created

- GIVEN 農場建立 critical active alert
- WHEN notification worker 處理事件
- THEN 系統 SHALL 建立站內通知
- AND SHALL 依使用者偏好發送 Email
- AND 通知 SHALL 關聯 alert event 與 farm

### Requirement: Recipient Authorization

通知收件者 MUST 依事件發生時的組織、資源權限、角色與訂閱設定計算。

#### Scenario: Former member remains in a recipient list

- GIVEN 使用者已離開 Producer 組織
- WHEN 該組織產生新告警
- THEN 系統 MUST NOT 發送通知給該使用者
- AND 快取收件者清單 SHALL 被更新或重新授權

### Requirement: Notification Preferences

使用者 SHALL 能依事件類型與通道設定通知偏好，但平台 MAY 對安全、帳號與法定必要通知設定不可完全停用的最低通道。

#### Scenario: User disables routine AI notifications

- GIVEN 使用者關閉一般 AI 建議 Email
- WHEN 新增非緊急 AI insight
- THEN 系統 SHALL 建立站內通知或依偏好靜默
- AND MUST NOT 發送 Email

#### Scenario: Account security event occurs

- GIVEN 使用者關閉一般通知
- WHEN 帳號密碼或裝置憑證發生高風險變更
- THEN 系統 SHALL 依安全政策發送必要通知
- AND SHALL 說明無法停用的原因

### Requirement: Deduplication and Suppression

相同事件與收件者在可配置時間窗內 MUST 不重複發送；告警通知 SHALL 支援持續事件抑制與升級規則。

#### Scenario: Same alert is evaluated repeatedly

- GIVEN 同一 active alert 已發送初次通知
- WHEN 規則引擎再次評估相同狀態
- THEN 系統 SHALL 不重複發送相同層級通知
- AND MAY 依升級時間表發送提醒

### Requirement: Delivery State and Retry

每筆外部通知 SHALL 保存 queued、sent、delivered、failed、suppressed 狀態與 provider response。暫時錯誤 SHALL 使用有上限的退避重試。

#### Scenario: Email provider is temporarily unavailable

- GIVEN Email 發送回傳可重試錯誤
- WHEN Worker 處理失敗
- THEN 系統 SHALL 安排有限次退避重試
- AND 超過上限後 SHALL 標記 failed 並保留原因
- AND 不得阻塞核心告警建立

### Requirement: Read and Action State

站內通知 SHALL 支援 unread、read、archived，並可提供授權後的事件深層連結。

#### Scenario: User opens a farm alert notification

- GIVEN 使用者仍具有該農場權限
- WHEN 點擊通知
- THEN 系統 SHALL 導向該告警詳情
- AND SHALL 標記為 read

#### Scenario: User no longer has access

- GIVEN 使用者失去該資源權限
- WHEN 點擊舊通知
- THEN 系統 SHALL 拒絕資源存取
- AND MAY 顯示通知摘要而不洩漏目前私有資料

### Requirement: Localization and Time

通知模板 SHALL 支援語系與時區。所有事件時間以 UTC 保存，顯示時依收件者時區轉換。

#### Scenario: Taiwan user receives a scheduled reminder

- GIVEN 使用者時區為 Asia/Taipei
- WHEN 系統顯示或發送排程通知
- THEN 內容 SHALL 使用該時區日期時間
- AND 稽核資料 SHALL 保留原始 UTC 時間
