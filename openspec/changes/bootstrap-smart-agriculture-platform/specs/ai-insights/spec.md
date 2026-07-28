# AI Insights Capability

## Purpose

定義異常偵測、預測分析與智慧推薦的服務契約、可解釋性與安全邊界。

### Requirement: Versioned AI Insight Results

系統 SHALL 對每次 AI 推論保存請求識別、insight 類型、輸入摘要、結果、模型名稱、模型版本、可信度、解釋、狀態與產生時間。

#### Scenario: Irrigation recommendation succeeds

- GIVEN 作物批次具有足夠的近期環境資料
- WHEN Laravel 呼叫 AI Service 產生灌溉建議
- THEN 系統 SHALL 保存建議結果
- AND 結果 SHALL 包含模型版本、可信度與至少一項解釋
- AND Producer Portal SHALL 將其標示為 AI 建議而非保證結果

#### Scenario: AI service times out

- GIVEN AI Service 在設定時間內沒有回應
- WHEN 推論請求逾時
- THEN 系統 SHALL 將請求標記為 failed 或 timeout
- AND 基本監控與告警功能 SHALL 繼續可用
- AND UI SHALL 顯示可理解的暫時不可用狀態

### Requirement: Three AI Function Families

系統 SHALL 提供三類可擴充 AI insight：異常偵測、預測分析與智慧推薦。

#### Scenario: Environmental anomaly detection

- GIVEN 系統具有近期感測資料與基準範圍
- WHEN 執行異常偵測
- THEN 系統 SHALL 回傳異常類型、嚴重度、可信度與判斷依據

#### Scenario: Production prediction

- GIVEN 作物批次具有生長階段、種植日期與有效資料
- WHEN 執行產量或採收日期預測
- THEN 系統 SHALL 回傳預測值、合理區間與模型版本

#### Scenario: Role-specific recommendation

- GIVEN 相同農產品批次可被不同角色查看
- WHEN Producer、Merchant 與 Consumer 分別請求推薦
- THEN 系統 SHALL 依角色目的產生不同內容
- AND 不得在推薦中洩漏該角色無權取得的資料

### Requirement: AI and Actuator Separation

AI Service MUST NOT 直接持有可向 MQTT Broker 發布設備控制命令的憑證。

#### Scenario: AI recommends irrigation

- GIVEN AI 結果建議啟動灌溉
- WHEN 推論完成
- THEN 系統 SHALL 僅建立 recommendation 或待確認事項
- AND SHALL NOT 直接發布水泵控制命令

#### Scenario: Future automation is enabled

- GIVEN 未來經獨立 OpenSpec change 核准自動化功能
- WHEN 系統依 AI 建議評估控制行為
- THEN 控制命令仍 SHALL 通過規則引擎、權限、安全上限與稽核流程
