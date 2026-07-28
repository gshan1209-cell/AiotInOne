# Organization and Tenancy Capability

## Purpose

定義 Producer、Merchant 與治理組織的生命週期、成員邀請、角色指派、組織切換與資料隔離。

### Requirement: Organization Lifecycle

系統 SHALL 支援建立、啟用、停用與封存 Producer、Merchant 及 Platform 類型組織，且每個組織 SHALL 具有唯一識別、名稱、類型、狀態、時區與聯絡資訊。

#### Scenario: Producer creates an organization

- GIVEN 已登入使用者尚未擁有 Producer 組織
- WHEN 使用者提交有效組織資料
- THEN 系統 SHALL 建立 Producer 組織
- AND 建立者 SHALL 成為 `producer_owner`
- AND 系統 SHALL 記錄建立稽核事件

#### Scenario: Suspended organization accesses private resources

- GIVEN 組織狀態為 suspended
- WHEN 該組織成員嘗試存取私有資源
- THEN 系統 SHALL 拒絕寫入操作
- AND 系統 MAY 依治理政策允許唯讀匯出
- AND SHALL 顯示停用原因與支援管道

### Requirement: Membership Invitation

組織擁有者 SHALL 能以 Email 邀請成員，邀請 MUST 具有單次使用 Token、角色、有效期限、狀態與邀請者。

#### Scenario: Valid invitation is accepted

- GIVEN 邀請尚未使用且未過期
- WHEN 收件者完成登入或註冊並接受邀請
- THEN 系統 SHALL 建立 organization membership
- AND 邀請 SHALL 標記為 accepted
- AND Token SHALL 立即失效

#### Scenario: Expired invitation is used

- GIVEN 邀請已超過有效期限
- WHEN 使用者提交該 Token
- THEN 系統 SHALL 拒絕接受
- AND SHALL NOT 建立成員關係

### Requirement: Role Assignment

只有具備成員管理權限的使用者 SHALL 能新增、修改或移除組織角色，且使用者不得移除組織最後一位 owner。

#### Scenario: Removing the last owner

- GIVEN 組織僅有一位 owner
- WHEN 該 owner 或管理員嘗試移除其 owner 角色
- THEN 系統 SHALL 拒絕操作
- AND SHALL 要求先指派另一位 owner

### Requirement: Active Organization Context

同時隸屬多個組織的使用者 SHALL 能切換 active organization，且每次請求的資源授權 MUST 依後端解析的 active organization 執行。

#### Scenario: User switches organization

- GIVEN 使用者同時屬於 Organization A 與 Organization B
- WHEN 使用者切換到 Organization B
- THEN 後續 Dashboard 與 API 查詢 SHALL 使用 Organization B 範圍
- AND 前端保存值不得取代後端授權驗證

### Requirement: Tenant Isolation

所有組織私有資料 MUST 具有 organization ownership 或明確授權關係，Repository、Query、Policy 與測試 SHALL 防止跨租戶讀寫。

#### Scenario: Object identifier from another tenant is submitted

- GIVEN 使用者屬於 Organization A
- AND 請求包含 Organization B 的資源 ID
- WHEN API 執行查詢或更新
- THEN 系統 SHALL 回傳 403 或不洩漏存在性的 404
- AND SHALL NOT 回傳 Organization B 的敏感欄位
- AND SHALL 記錄越權嘗試
