# Marketplace and Procurement Capability

## Purpose

定義 Producer 供應批次、Merchant 採購需求、搜尋媒合、詢價與供應狀態。MVP 不包含正式金流與複雜物流。

### Requirement: Product and Supply Lot

Producer SHALL 能由採收紀錄建立供應批次。供應批次 MUST 包含產品、來源批次、數量、單位、等級、可供應日期、價格資訊、公開狀態與追溯政策。

#### Scenario: Producer publishes a supply lot

- GIVEN draft supply lot 具有有效來源、數量與可供應日期
- WHEN Producer 選擇發布
- THEN 系統 SHALL 驗證公開欄位與庫存數量
- AND 將狀態更新為 published
- AND Merchant SHALL 能在授權市場中搜尋該批次

#### Scenario: Producer publishes more than harvested quantity

- GIVEN 可追蹤採收數量低於欲發布數量
- WHEN Producer 提交發布
- THEN 系統 SHALL 拒絕或要求有權限的人工調整理由
- AND SHALL 保留差異稽核紀錄

### Requirement: Procurement Request

Merchant SHALL 能建立採購需求，包含產品、品種、品質、需求量、單位、期望日期、區域與備註。

#### Scenario: Merchant creates a procurement request

- GIVEN Merchant 具有採購權限
- WHEN 提交有效需求
- THEN 系統 SHALL 建立 open request
- AND SHALL 只向符合市場與權限範圍的 Producer 顯示

### Requirement: Supply Search and Filtering

Merchant SHALL 能依產品、品種、區域、可供應日期、數量、價格區間與追溯狀態搜尋供應批次。

#### Scenario: Merchant filters by delivery window

- GIVEN 市場存在多個供應批次
- WHEN Merchant 指定日期範圍
- THEN 系統 SHALL 只回傳可供應日期重疊的 published 批次
- AND SHALL 依權限遮罩非公開欄位

### Requirement: Matching Recommendation

系統 MAY 使用規則或 AI 提供供需媒合排序，但推薦 MUST 顯示主要依據，且不得自動建立契約或訂單。

#### Scenario: AI ranks supply lots

- GIVEN Merchant 具有有效採購需求
- WHEN 系統產生媒合建議
- THEN 結果 SHALL 包含供應符合度、可供應時間、距離層級、數量與風險摘要
- AND Merchant SHALL 自行選擇是否聯繫或詢價

### Requirement: Inquiry Workflow

Merchant SHALL 能針對供應批次建立詢價，Producer SHALL 能接受、拒絕或回覆條件。MVP 詢價不代表正式買賣契約。

#### Scenario: Producer responds to inquiry

- GIVEN Merchant 已建立 open inquiry
- WHEN Producer 回覆價格、數量與有效期限
- THEN 系統 SHALL 保存回覆與狀態
- AND Merchant SHALL 收到通知
- AND UI SHALL 清楚標示非正式訂單

### Requirement: Inventory Reservation Boundary

MVP MAY 提供意向保留，但 MUST 定義有效期限與可釋放狀態，且不得造成負庫存。

#### Scenario: Two merchants request the remaining quantity

- GIVEN 供應批次只剩 100 公斤
- WHEN 兩筆保留同時嘗試各占用 80 公斤
- THEN 系統 MUST 使用交易或鎖定避免總保留超過 100 公斤
- AND 失敗請求 SHALL 收到明確剩餘量

### Requirement: Supply Status Lifecycle

供應批次狀態 SHALL 至少包含 draft、published、partially_reserved、reserved、sold_out、withdrawn、expired。

#### Scenario: Supply lot expires

- GIVEN published 批次超過可供應截止時間
- WHEN 系統執行狀態更新
- THEN 批次 SHALL 標記為 expired
- AND SHALL 不再出現在可採購搜尋
- AND 歷史追溯頁 MAY 依政策保留
