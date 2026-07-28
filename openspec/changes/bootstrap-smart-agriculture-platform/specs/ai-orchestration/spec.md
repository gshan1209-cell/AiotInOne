# AI Orchestration Capability

## Purpose

定義三方角色 AI 提示語、Prompt Registry、JSON 快取、模型路由、成本紀錄、內容安全、fallback 與人工回饋。

### Requirement: Role-Specific Prompt Registry

系統 SHALL 維護 Producer、Merchant、Consumer 三套獨立提示語模板。每個模板 MUST 保存用途、角色、版本、輸入 Schema、輸出 Schema、狀態、建立者、核准者與生效時間。

#### Scenario: Producer insight is generated

- GIVEN Producer 請求農務建議
- WHEN AI Orchestrator 選擇提示語
- THEN 系統 SHALL 使用 Producer 模板
- AND 輸出 SHALL 優先包含環境風險、農務行動、採收與設備建議
- AND SHALL NOT 使用 Consumer 行銷語氣取代專業資訊

#### Scenario: Merchant insight is generated

- GIVEN Merchant 查看供應批次
- WHEN AI Orchestrator 產生建議
- THEN 系統 SHALL 使用 Merchant 模板
- AND 輸出 SHALL 優先包含供應穩定性、採購量、補貨與短缺風險

#### Scenario: Consumer insight is generated

- GIVEN Consumer 查看公開商品
- WHEN AI Orchestrator 產生推薦
- THEN 系統 SHALL 使用 Consumer 模板
- AND 輸出 SHALL 優先包含當季、新鮮度、選購與料理建議
- AND MUST NOT 洩漏內部成本、私人農務紀錄或精確敏感位置

### Requirement: Structured AI Output

所有主要 AI 功能 MUST 使用版本化 JSON Schema 驗證輸出，不得直接將未驗證自由文字寫入核心資料欄位。

#### Scenario: Model returns invalid JSON

- GIVEN AI Provider 回傳不符合 Schema 的內容
- WHEN Orchestrator 驗證輸出
- THEN 系統 SHALL 將結果標記為 invalid_output
- AND SHALL 執行有限次修復或 fallback
- AND MUST NOT 將不合法內容當作正式建議

### Requirement: Deterministic Cache Key

相同角色、功能、資料版本、提示語版本、模型設定與語系的請求 SHALL 使用可重現 cache key。有效快取存在時 SHALL 優先讀取，不重複呼叫付費模型。

#### Scenario: Equivalent recommendation already exists

- GIVEN 相同商品類型、角色、資料摘要與 Prompt 版本已有未過期 JSON 快取
- WHEN 使用者再次請求推薦
- THEN 系統 SHALL 回傳快取結果
- AND SHALL 記錄 cache hit
- AND MUST NOT 呼叫 LLM

#### Scenario: Source data changes

- GIVEN 作物批次風險或供應資料已更新
- WHEN 新請求計算 cache key
- THEN 系統 SHALL 產生不同 key 或使舊快取失效
- AND SHALL 重新評估是否呼叫模型

### Requirement: Model Routing and Fallback

系統 SHALL 支援依 insight type、風險、成本與可用性選擇 provider/model，並定義 timeout、retry、fallback 與 circuit breaker。

#### Scenario: Primary model is unavailable

- GIVEN 主要模型逾時或服務異常
- WHEN 請求符合 fallback 條件
- THEN 系統 SHALL 改用核准的替代模型或規則引擎
- AND SHALL 清楚記錄實際 provider、model 與 fallback reason

#### Scenario: No safe fallback exists

- GIVEN 高風險建議無核准替代模型
- WHEN 主要模型不可用
- THEN 系統 SHALL 回傳 unavailable 狀態
- AND MUST NOT 產生看似可信的虛構結果

### Requirement: AI Usage Ledger

每次模型呼叫 SHALL 記錄 request_id、角色、功能、Prompt 版本、Provider、Model、輸入與輸出 Token、延遲、估算成本、cache 狀態與結果狀態。

#### Scenario: Administrator reviews AI usage

- GIVEN Administrator 具有 AI 治理權限
- WHEN 查詢指定期間使用量
- THEN 系統 SHALL 提供依角色、功能、模型與狀態彙總
- AND SHALL 能追蹤至個別 request_id
- AND SHALL 遮罩未授權的敏感輸入內容

### Requirement: Prompt Release Governance

正式 Prompt 版本 MUST 經測試、核准與發布流程。草稿版本不得自動成為 production active。

#### Scenario: New prompt version is published

- GIVEN 新版本已通過 Schema、回歸與安全測試
- WHEN 核准者發布版本
- THEN 系統 SHALL 將其標記為 active
- AND SHALL 保留前一版本供回滾
- AND SHALL 記錄發布差異與核准人

### Requirement: Safety and Data Minimization

送往外部 AI Provider 的資料 MUST 依角色、用途與最小必要原則處理；密碼、裝置憑證、完整個資與未核准精確位置 MUST NOT 被傳送。

#### Scenario: Input contains device secret

- GIVEN 組裝 AI features 時發現裝置祕密欄位
- WHEN Orchestrator 執行輸入過濾
- THEN 系統 MUST 移除該欄位
- AND SHALL 記錄安全過濾事件

### Requirement: Human Feedback

授權使用者 SHALL 能對 AI 建議標示 useful、not_useful、incorrect 或 unsafe，並提供可選原因。回饋 SHALL 關聯 request、Prompt 與模型版本。

#### Scenario: Producer reports unsafe advice

- GIVEN Producer 判定建議可能造成農損
- WHEN 提交 unsafe 回饋
- THEN 系統 SHALL 保存回饋
- AND SHALL 通知 AI 治理人員或建立審查事件
- AND MAY 暫停相同 Prompt 版本的高風險自動發布
