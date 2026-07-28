# Traceability and Consumer Capability

## Purpose

定義農產品批次追溯、QR Code 公開頁、欄位白名單、Consumer 商品資訊、季節內容與 AI 推薦。

### Requirement: Traceability Event Chain

系統 SHALL 以不可任意覆寫的事件鏈保存種植、農務、採收、分級、包裝、供應與下架等追溯事件。修正 SHALL 以新增更正事件完成，不得靜默改寫歷史。

#### Scenario: Harvest event is corrected

- GIVEN 已存在採收事件
- WHEN 授權 Producer 發現數量輸入錯誤
- THEN 系統 SHALL 建立 correction event
- AND SHALL 保留原事件、修正原因、操作者與時間

### Requirement: Public Traceability Profile

Producer SHALL 能為供應批次設定公開追溯資料。公開資料 MUST 採白名單方式，至少可包含產地區域、作物、品種、種植與採收日期、公開農務摘要、品質等級與環境摘要。

#### Scenario: Consumer opens a public lot page

- GIVEN 批次狀態允許公開追溯
- WHEN Consumer 透過公開 URL 查看
- THEN 系統 SHALL 不要求登入
- AND SHALL 顯示白名單欄位與最近更新時間
- AND MUST NOT 顯示私人聯絡資料、裝置憑證、內部成本、完整原始 telemetry 或敏感精確座標

### Requirement: Stable QR Code Identifier

每個公開批次 SHALL 具有不可猜測或具防濫用設計的公開識別。QR Code URL SHOULD 保持穩定，內容狀態變更時由頁面顯示最新有效資訊。

#### Scenario: Product lot is withdrawn

- GIVEN Consumer 掃描已撤回批次的 QR Code
- WHEN 公開頁載入
- THEN 系統 SHALL 顯示已撤回或不可購買狀態
- AND MAY 保留歷史追溯內容
- AND MUST NOT 將使用者導向不存在的商品而無說明

### Requirement: Environmental Summary

公開環境資訊 SHALL 使用經聚合、經品質標記且經 Producer 核准的摘要，不得直接暴露高頻原始資料。

#### Scenario: Sensor data quality is poor

- GIVEN 批次期間主要感測器校正逾期或資料缺漏
- WHEN 系統產生公開環境摘要
- THEN 系統 SHALL 標示資料品質限制
- AND MUST NOT 以虛構或過度精確數值補足缺口

### Requirement: Consumer Product Discovery

Consumer SHALL 能依作物、產季、產地區域、供應狀態與追溯狀態瀏覽公開商品。

#### Scenario: Consumer searches seasonal produce

- GIVEN 系統具有當季且公開的供應批次
- WHEN Consumer 選擇當季篩選
- THEN 系統 SHALL 回傳符合日期與區域規則的商品
- AND SHALL 清楚區分 AI 推薦與實際供應狀態

### Requirement: Consumer AI Recommendation

Consumer AI 建議 SHALL 聚焦選購、保存、料理與替代品，並清楚標示為一般資訊。涉及健康、過敏或食安時 MUST 採保守表述並優先引用平台已驗證資料。

#### Scenario: Consumer requests recipe suggestions

- GIVEN 商品具有可公開的品項與新鮮度資訊
- WHEN Consumer 請求料理建議
- THEN 系統 SHALL 回傳結構化料理方向、保存建議與可替代品
- AND MUST NOT 洩漏 Producer 私有資料

#### Scenario: Product has an active safety notice

- GIVEN 商品批次存在有效食安或召回通知
- WHEN Consumer 查看商品或 AI 推薦
- THEN 系統 SHALL 優先顯示安全通知
- AND MUST NOT 以促銷或料理建議淡化風險

### Requirement: Public Page Privacy and Abuse Protection

公開頁 SHALL 具備速率限制、輸入驗證、機器人濫用防護與隱私最小化。

#### Scenario: Public identifier enumeration is attempted

- GIVEN Client 大量猜測公開識別
- WHEN 請求超過政策門檻
- THEN 系統 SHALL 限流或阻擋
- AND SHALL 記錄可疑活動
