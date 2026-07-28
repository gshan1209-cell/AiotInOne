# Three-Party Platform Capability

## Purpose

定義生產端、銷售端、消費端與治理後台的主要使用行為及資訊邊界。

### Requirement: Producer Portal

Producer Portal SHALL 提供農場、田區、作物批次、設備、即時監控、告警、AI 農務建議與供應批次管理。

#### Scenario: Producer opens farm dashboard

- GIVEN Producer 對農場具有檢視權限
- WHEN Producer 開啟農場 Dashboard
- THEN 系統 SHALL 顯示最新感測值、裝置狀態、活動告警與近期 AI 建議
- AND 所有內容 SHALL 限於該 Producer 被授權範圍

### Requirement: Merchant Portal

Merchant Portal SHALL 提供可供應農產品、批次追溯、預估供應量、採購需求與 AI 採購建議。

#### Scenario: Merchant reviews a supply lot

- GIVEN Producer 已發布可供應批次
- WHEN Merchant 查看該批次
- THEN 系統 SHALL 顯示商品、產地、預計或實際採收日、可供應量與經允許的追溯資訊
- AND 系統 SHALL NOT 顯示農場設備憑證、內部告警備註或非公開感測原始資料

### Requirement: Consumer Portal

Consumer Portal SHALL 提供公開商品、產地、批次追溯、季節資訊及 AI 商品與料理推薦。

#### Scenario: Consumer scans traceability QR code

- GIVEN 產品批次已啟用公開追溯頁
- WHEN Consumer 開啟 QR Code 對應 URL
- THEN 系統 SHALL 顯示公開追溯資料
- AND 不要求登入即可查看
- AND 不得揭露農民私人聯絡資料、裝置 ID、憑證或敏感精確位置

### Requirement: Role-Specific AI Presentation

三方入口 SHALL 使用不同的 AI 資訊目的與提示語，不得以同一份通用內容取代角色需求。

#### Scenario: Same crop lot is viewed by three roles

- GIVEN 同一作物批次具有生產、供應與消費資訊
- WHEN Producer 查看 AI 卡片
- THEN 系統 SHALL 優先呈現環境、農務、採收與風險建議

- WHEN Merchant 查看 AI 卡片
- THEN 系統 SHALL 優先呈現採購量、供應穩定性、補貨與短缺風險

- WHEN Consumer 查看 AI 卡片
- THEN 系統 SHALL 優先呈現當季、新鮮度、選購與料理建議

### Requirement: Administrative Governance

Administrator Portal SHALL 提供帳號、組織、裝置、告警規則、AI 模型版本、執行紀錄、安全事件與稽核管理。

#### Scenario: Administrator changes an alert rule

- GIVEN Administrator 具有告警規則管理權限
- WHEN Administrator 修改生產環境告警規則
- THEN 系統 SHALL 保存變更前後內容、操作者、時間與原因
- AND 新規則 SHALL 只影響其明確設定的範圍
