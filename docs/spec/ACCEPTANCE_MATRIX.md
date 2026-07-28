# AiotInOne MVP 驗收矩陣

## 使用方式

- P0：MVP 上線前必須通過。
- P1：可在 MVP 後段完成，但不得破壞 P0。
- 每項驗收需附測試名稱、執行結果、版本與證據連結。
- 任何標記完成的項目都必須能對應 OpenSpec Requirement 與 Scenario。

## 1. Identity and Tenancy

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| IAM-001 | P0 | 四類角色登入後進入正確入口 | Feature/E2E |
| IAM-002 | P0 | Producer A 無法讀寫 Producer B 的農場 | Policy/Feature |
| IAM-003 | P0 | Merchant 無法操作農場設備 | API Authorization |
| IAM-004 | P0 | Consumer 無法讀取非公開追溯資料 | Feature |
| IAM-005 | P0 | 組織最後一位 owner 不可被移除 | Domain/Feature |
| IAM-006 | P0 | 邀請 Token 單次使用且過期失效 | Feature |
| IAM-007 | P1 | 多組織切換不發生資料交叉 | E2E |

## 2. Farm Operations

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| FARM-001 | P0 | Producer 可建立農場、田區與作物批次 | Feature |
| FARM-002 | P0 | 作物批次非法狀態轉換被拒絕 | Domain |
| FARM-003 | P0 | AI 不可未確認覆寫人工採收預估 | Integration |
| FARM-004 | P0 | 農務紀錄保存用量、單位、時間、操作者 | Feature |
| FARM-005 | P0 | 採收紀錄可建立 draft 供應批次 | Feature |
| FARM-006 | P1 | 追溯修正以 correction event 完成 | Domain |

## 3. Device Lifecycle

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| DEV-001 | P0 | 每台裝置取得獨立識別與憑證 | Integration |
| DEV-002 | P0 | 啟用 Token 無法重複使用 | Security |
| DEV-003 | P0 | 停用或撤銷裝置不能發布資料 | MQTT Integration |
| DEV-004 | P0 | 裝置不能發布至其他農場 Topic | MQTT ACL |
| DEV-005 | P0 | 心跳逾時後裝置變為 offline | Scheduled Job |
| DEV-006 | P1 | 校正逾期資料標記 quality | Integration |
| DEV-007 | P1 | 退役不刪除歷史資料 | Feature |

## 4. Telemetry and Alerts

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| TEL-001 | P0 | ESP32 模擬器可送四類感測值 | End-to-End |
| TEL-002 | P0 | Schema 或單位錯誤不寫入正式 readings | Contract/Integration |
| TEL-003 | P0 | 相同 device/message_id 不重複寫入 | Integration |
| TEL-004 | P0 | 最新值在正常負載 10 秒內顯示 | Performance/E2E |
| TEL-005 | P0 | 七天小時聚合按時間排序且帶單位 | API Feature |
| ALT-001 | P0 | 門檻持續超標只建立一個 active alert | Domain/Integration |
| ALT-002 | P0 | 數值恢復時更新原告警為 resolved | Integration |
| ALT-003 | P0 | 無權限使用者不能確認告警 | Authorization |
| ALT-004 | P1 | 重複通知被抑制並支援升級 | Integration |

## 5. Device Command Safety

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| CMD-001 | P0 | 超過最長執行時間的命令被拒絕 | Domain/API |
| CMD-002 | P0 | 相同 idempotency key 不重複發布 | Integration |
| CMD-003 | P0 | 過期命令在雲端與裝置端皆拒絕 | Contract/Simulator |
| CMD-004 | P0 | 未回報命令轉為 timeout 並通知 | Scheduled/Integration |
| CMD-005 | P0 | AI Service 無控制 Broker 憑證 | Security/Config |
| CMD-006 | P0 | emergency stop 阻止所有啟動命令 | Domain/E2E |
| CMD-007 | P1 | 晚到結果觸發狀態重新同步 | Integration |

## 6. AI

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| AI-001 | P0 | 三方角色使用不同 Prompt 模板 | Contract/Feature |
| AI-002 | P0 | AI 結果包含模型、版本、可信度與解釋 | Contract |
| AI-003 | P0 | 不合法 JSON 不寫入正式 insight | Contract/Integration |
| AI-004 | P0 | 有效快取存在時不呼叫 LLM | Unit/Integration |
| AI-005 | P0 | 來源資料或 Prompt 版本變更使快取失效 | Unit |
| AI-006 | P0 | Provider 故障時核心監控仍可用 | Resilience/E2E |
| AI-007 | P0 | Usage Ledger 保存 Token、延遲、成本與 cache 狀態 | Integration |
| AI-008 | P0 | Secret/個資不傳入外部 Provider | Security |
| AI-009 | P1 | unsafe 回饋建立治理審查事件 | Feature |

## 7. Marketplace and Traceability

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| MKT-001 | P0 | Producer 可發布有效供應批次 | Feature |
| MKT-002 | P0 | 發布量超過來源量被拒絕或需核准理由 | Domain |
| MKT-003 | P0 | Merchant 可搜尋與建立採購需求 | Feature |
| MKT-004 | P0 | 並行保留不得造成負庫存 | Concurrency |
| MKT-005 | P1 | 詢價流程不被呈現為正式訂單 | E2E |
| TRC-001 | P0 | QR 公開頁不需登入 | E2E |
| TRC-002 | P0 | 公開頁不洩漏精確位置、憑證、原始資料與私人聯絡 | Security |
| TRC-003 | P0 | 撤回批次仍顯示明確狀態 | Feature |
| TRC-004 | P0 | 食安通知優先於 AI 促銷或料理推薦 | Integration |

## 8. Administration, Data and Operations

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| ADM-001 | P0 | support_operator 無法修改安全設定 | Authorization |
| ADM-002 | P0 | 稽核事件不可由一般流程修改或刪除 | Database/Domain |
| ADM-003 | P0 | Prompt、告警與安全設定可查看版本與回滾 | Feature |
| ADM-004 | P0 | 裝置憑證輪替稽核不含祕密明文 | Security |
| DATA-001 | P0 | 原始 payload 依政策清理且保留聚合 | Scheduled/Integration |
| DATA-002 | P0 | Secret 不出現在應用日誌 | Security Test |
| OPS-001 | P0 | Laravel、FastAPI、PostgreSQL、Redis、MQTT health 通過 | Environment |
| OPS-002 | P0 | AI 故障時平台顯示 degraded 而非整體失效 | Resilience |
| OPS-003 | P0 | 可從備份在隔離環境完成還原演練 | Operations Evidence |
| OPS-004 | P1 | 關鍵流程可由 correlation ID 跨服務追蹤 | Observability |

## 9. Nonfunctional Gates

| ID | Priority | 驗收條件 | 建議測試 |
|---|---|---|---|
| NFR-001 | P0 | 最新值 API p95 ≤ 500 ms（基準環境） | Load Test |
| NFR-002 | P0 | 七天小時聚合 API p95 ≤ 1.5 s | Load Test |
| NFR-003 | P0 | ingestion 持續處理 100 msg/s、錯誤率 < 1% | Load Test |
| NFR-004 | P0 | 360 px 手機版主要流程無水平捲動 | Responsive E2E |
| NFR-005 | P0 | 高風險控制需明確確認並防誤觸 | UX/E2E |
| NFR-006 | P1 | 主要流程符合 WCAG 2.1 AA 基線 | Accessibility Audit |
| NFR-007 | P0 | lint、static analysis、tests、contracts、OpenSpec verify 全通過 | CI/Local Gate |

## 10. 最終完成條件

- 所有 P0 項目通過。
- P1 未完成項目具有 Issue、風險與預定 change。
- 測試不得以 skip、刪除驗證或硬編碼成功結果規避。
- OpenAPI、JSON Schema、MQTT 契約與實作同步。
- `openspec verify` 通過。
- 完成規格同步與 `/opsx:archive` 前人工驗收差異。
