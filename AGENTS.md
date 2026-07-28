# AGENTS.md

## 專案定位

AiotInOne 是可擴充的 AIoT 整合平台，第一個產品場景為智慧農業三方平台：

- 生產端：農民、農場管理者、合作社
- 銷售端：通路商、採購商、零售商
- 消費端：一般消費者
- 治理端：系統管理員，不列入商業三方角色

## 強制開發流程

1. 開始工作前先閱讀 `openspec/project.md` 與相關 change。
2. 新功能、重大重構、資料模型變更、API 契約變更，都必須先建立 OpenSpec change。
3. change 至少包含：
   - `proposal.md`
   - `design.md`
   - `tasks.md`
   - `specs/<capability>/spec.md`
4. 需求使用 SHALL／MUST 表達，並提供 Given／When／Then 驗收情境。
5. 未完成規格與驗收條件前，不得直接進入大規模實作。
6. 完成實作後必須執行測試、OpenSpec verify，並更新文件後才能歸檔。

## 技術原則

- 核心平台：PHP 8.3+、Laravel 12+。
- AI 推論：Python 3.12+、FastAPI，透過 HTTP API 或 Queue 與 Laravel 解耦。
- IoT：ESP32、MQTT；Broker 優先採 EMQX 或 Mosquitto。
- 資料庫：PostgreSQL；快取與 Queue 採 Redis。
- 前端：Laravel Blade + Livewire 或 Inertia + Vue 3，由 change 明確決策。
- 本機環境：Docker Compose。
- API 必須版本化，預設 `/api/v1`。
- 所有時間以 UTC 儲存，前端依 `Asia/Taipei` 顯示。

## 安全與品質

- 禁止把 API Key、資料庫密碼、MQTT 密碼提交到 Git。
- IoT 裝置不得共用永久憑證，每台裝置必須有獨立身分。
- 遠端控制水泵、風扇、閥門等設備，必須有權限檢查、逾時、冪等與安全停止機制。
- AI 建議不得直接等同控制命令；自動執行必須經規則引擎與安全限制。
- 不得為了通過測試刪除既有功能、測試或驗證邏輯。
- 禁止未經規格允許的大量刪除或重寫程式碼。
- 每個功能必須具備測試與可觀測性紀錄。

## 文件語言

- 使用者與產品文件以繁體中文為主。
- 程式碼、類別、函式、資料表與 API 欄位使用英文。
- 提交訊息採 Conventional Commits。
