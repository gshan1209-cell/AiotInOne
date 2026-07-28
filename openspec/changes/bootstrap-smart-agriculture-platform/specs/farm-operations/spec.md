# Farm Operations Capability

## Purpose

定義農場、田區、溫室、作物品種、種植批次、農務活動、投入品與採收紀錄。

### Requirement: Farm and Field Structure

Producer SHALL 能在授權組織內管理農場、田區與溫室。每個資源 MUST 包含 organization、狀態、名稱、時區及可選位置資訊。

#### Scenario: Producer creates a field

- GIVEN Producer 對農場具有管理權限
- WHEN Producer 提交有效田區名稱、面積與用途
- THEN 系統 SHALL 建立田區並關聯該農場與組織
- AND 面積 SHALL 使用明確單位保存

#### Scenario: Precise location is exposed publicly

- GIVEN 農場具有精確座標
- WHEN 系統產生 Consumer 公開追溯頁
- THEN 系統 MUST NOT 預設公開精確座標
- AND SHALL 僅顯示經 Producer 核准的區域級位置

### Requirement: Crop Catalog and Batch Lifecycle

系統 SHALL 管理作物種類、品種與種植批次。批次狀態至少包含 planned、growing、harvest_ready、harvested、cancelled。

#### Scenario: Crop batch starts growing

- GIVEN planned 批次具有作物、田區與種植日期
- WHEN Producer 將批次更新為 growing
- THEN 系統 SHALL 保存狀態變更時間
- AND SHALL 建立批次生命週期事件

#### Scenario: Invalid state transition

- GIVEN 作物批次狀態為 cancelled
- WHEN 使用者嘗試直接改為 harvested
- THEN 系統 SHALL 拒絕狀態轉換
- AND SHALL 回傳允許的下一步狀態

### Requirement: Growth Stage Tracking

Producer SHALL 能更新作物批次的生長階段、預計採收日與健康狀態，且所有重要變更 SHALL 保留歷程。

#### Scenario: Estimated harvest date changes

- GIVEN 批次已有預計採收日
- WHEN Producer 或 AI 建議調整日期
- THEN 系統 SHALL 保存原值、新值、來源、原因與時間
- AND AI 建議 SHALL NOT 未經確認直接覆寫人工核准值

### Requirement: Farm Activity Records

系統 SHALL 支援灌溉、施肥、病蟲害處理、修剪、巡田、採樣與其他自訂農務紀錄。

#### Scenario: Irrigation activity is recorded

- GIVEN Producer 對批次具有操作權限
- WHEN Producer 新增灌溉紀錄
- THEN 系統 SHALL 保存時間、方式、用量、單位、操作者與備註
- AND MAY 關聯設備命令或 AI 建議

### Requirement: Input and Treatment Traceability

涉及肥料、農藥或資材的紀錄 MUST 保存品項、批號、用量、單位、使用時間與操作者，並支援依政策設定公開程度。

#### Scenario: Treatment record is shown to consumer

- GIVEN Producer 建立處理紀錄
- WHEN Consumer 查看公開追溯頁
- THEN 系統 SHALL 只顯示公開白名單欄位
- AND MUST NOT 顯示內部成本、供應商機密或私人備註

### Requirement: Harvest Recording

Producer SHALL 能記錄採收日期、數量、單位、等級、損耗與批次來源，採收紀錄 SHALL 能轉換為供應批次但不得自動等同可販售商品。

#### Scenario: Harvest creates a supply draft

- GIVEN 作物批次具有有效採收紀錄
- WHEN Producer 選擇建立供應批次
- THEN 系統 SHALL 建立 draft supply lot
- AND SHALL 保留來源作物批次與採收紀錄關聯
- AND Producer SHALL 在發布前確認公開資訊、數量與價格
