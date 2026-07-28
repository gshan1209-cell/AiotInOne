# Identity and Access Capability

## Purpose

定義智慧農業三方平台的帳號、組織、角色與資料隔離行為。

### Requirement: Role-Based Portal Access

系統 SHALL 支援 Producer、Merchant、Consumer 與 Administrator 四類主要權限角色，並依角色提供對應入口與功能。

#### Scenario: Producer signs in

- GIVEN 使用者具有有效的 Producer 角色
- WHEN 使用者完成登入
- THEN 系統 SHALL 導向 Producer Portal
- AND 系統 SHALL 只顯示其被授權農場與生產端功能

#### Scenario: Merchant attempts device control

- GIVEN 使用者具有 Merchant 角色但沒有 Producer 設備操作權限
- WHEN 使用者呼叫設備控制 API
- THEN 系統 SHALL 回傳 403
- AND 系統 SHALL 記錄被拒絕的授權事件

### Requirement: Organization Data Isolation

系統 MUST 以組織與資源關聯執行後端資料隔離，不得只依前端選單或查詢參數限制資料。

#### Scenario: Producer accesses another organization's farm

- GIVEN Producer A 屬於 Organization A
- AND Farm B 屬於 Organization B
- WHEN Producer A 嘗試讀取 Farm B
- THEN 系統 SHALL 拒絕存取
- AND 回應不得洩漏 Farm B 的詳細資料

#### Scenario: Platform administrator audits organizations

- GIVEN 使用者具有 platform_admin 權限
- WHEN 使用者進入治理後台查詢組織
- THEN 系統 SHALL 允許依稽核權限查看必要資料
- AND 系統 SHALL 記錄管理員查詢行為

### Requirement: Secure Device Identity

每台 IoT 裝置 SHALL 具有獨立且可撤銷的身分憑證，不得使用全平台共用永久密碼。

#### Scenario: Disabled device publishes telemetry

- GIVEN 裝置已被停用或憑證已撤銷
- WHEN 裝置嘗試發布 telemetry
- THEN MQTT Broker 或 ingestion layer SHALL 拒絕訊息
- AND 系統 SHALL 記錄安全事件
