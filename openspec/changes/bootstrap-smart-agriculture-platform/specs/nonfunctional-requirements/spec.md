# Nonfunctional Requirements Capability

## Purpose

定義 MVP 的效能、可靠性、可用性、安全、相容性、無障礙、維護性與災難復原驗收標準。

### Requirement: Dashboard Performance

在開發基準資料量下，Producer Dashboard 最新值 API 的 p95 回應時間 SHOULD 不超過 500 ms，七天小時聚合趨勢 API 的 p95 SHOULD 不超過 1.5 秒，不含使用者網路延遲。

#### Scenario: Baseline load test runs

- GIVEN 具有 100 個農場、1,000 台裝置與代表性 telemetry 資料
- WHEN 執行基準負載測試
- THEN p95 SHALL 符合定義門檻或產生核准的改善計畫
- AND 測試報告 SHALL 保存資料量、環境與版本

### Requirement: Telemetry Throughput

MVP ingestion SHALL 在單一部署環境持續處理至少每秒 100 筆 telemetry message，錯誤率低於 1%，且不得產生重複正式 readings。

#### Scenario: Burst telemetry arrives

- GIVEN 1,000 台模擬裝置同時回補短期資料
- WHEN 流量短暫超過持續基準
- THEN Queue SHALL 吸收尖峰
- AND 系統 SHALL 不丟失已被 Broker 接受的訊息
- AND ingestion lag SHALL 可監控

### Requirement: Availability Degradation

AI、Email 或非關鍵外部服務故障時，登入、農場監控、歷史資料、告警與人工控制核心功能 SHALL 維持可用或明確降級。

#### Scenario: AI service is down

- GIVEN FastAPI 或外部模型不可用
- WHEN Producer 開啟 Dashboard
- THEN 感測資料與告警 SHALL 正常顯示
- AND AI 區塊 SHALL 顯示暫時不可用
- AND MUST NOT 阻塞核心頁面

### Requirement: Data Consistency

帳號、權限、供應數量、命令狀態與追溯事件等交易資料 SHALL 使用資料庫交易或等效機制保持一致；跨服務流程 SHALL 使用可重試、冪等事件。

#### Scenario: Supply publish transaction fails

- GIVEN Producer 發布供應批次時其中一步失敗
- WHEN transaction 回滾
- THEN 批次 SHALL 保持原狀態
- AND MUST NOT 出現已發布但無來源關聯的資料

### Requirement: Security Baseline

系統 MUST 遵守安全開發基線：密碼雜湊、CSRF 防護、輸入驗證、輸出編碼、速率限制、依賴掃描、祕密掃描、最小權限與安全 Header。

#### Scenario: Repeated login failures occur

- GIVEN 同一帳號或來源連續登入失敗
- WHEN 超過政策門檻
- THEN 系統 SHALL 限流或暫時鎖定
- AND SHALL 記錄安全事件
- AND 不得洩漏帳號是否存在

### Requirement: Browser and Responsive Support

Web UI SHALL 支援最新兩個主要版本的 Chrome、Edge、Firefox、Safari，並支援寬度 360 px 以上的手機瀏覽。設備控制頁 MUST 避免因響應式排列造成誤觸。

#### Scenario: Producer uses a phone

- GIVEN viewport 寬度為 360 px
- WHEN Producer 查看 Dashboard 與告警
- THEN 主要資訊 SHALL 可讀取且不需水平捲動
- AND 高風險控制 SHALL 需要明確確認

### Requirement: Accessibility

主要使用流程 SHOULD 達到 WCAG 2.1 AA 基線，包括鍵盤操作、焦點可見、語意標籤、替代文字與足夠對比。

#### Scenario: Keyboard-only navigation

- GIVEN 使用者不使用滑鼠
- WHEN 操作登入、Dashboard、告警與確認對話框
- THEN 所有必要控制 SHALL 可由鍵盤到達與操作
- AND 焦點順序 SHALL 合理

### Requirement: Localization

使用者介面 SHALL 以繁體中文為預設並保留語系擴充能力。日期、時間、數字與單位 SHALL 依 Locale 顯示，但 API 與資料庫使用標準格式。

#### Scenario: Taiwan locale displays telemetry

- GIVEN 使用者 Locale 為 zh-TW、時區為 Asia/Taipei
- WHEN 查看溫度與時間
- THEN UI SHALL 顯示攝氏與本地時間
- AND API SHALL 保持 UTC ISO 8601 與標準 unit code

### Requirement: Recovery Objectives

MVP 正式環境 SHOULD 以 RPO 24 小時、RTO 8 小時作為最低起始目標；上線前 MUST 依實際商業風險重新核准。

#### Scenario: Primary database is lost

- GIVEN 發生資料庫故障
- WHEN 執行災難復原程序
- THEN 系統 SHALL 能由有效備份還原
- AND SHALL 驗證關鍵資料、權限與命令狀態
- AND SHALL 產生事故與復原報告

### Requirement: Maintainability and Quality Gates

合併至 main 前 MUST 通過格式化、靜態分析、單元測試、Feature Tests、Contract Tests 與 OpenSpec 驗證。不得透過刪除測試或降低安全限制使檢查通過。

#### Scenario: Contract test fails

- GIVEN PR 修改 MQTT 或 AI Schema
- WHEN Contract Test 顯示破壞相容性
- THEN PR MUST 不得合併
- AND 開發者 SHALL 建立版本遷移或修正實作
