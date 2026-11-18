# Bootstrap 規格解析修復候選

2026-11-13，baseline `7f309213dae7714fa44f6d6630daa2c26f061148`。
使用 npm 官方 registry 的 `@fission-ai/openspec@2.0.0`；package engines 為 Node >=22.12.0，本機 Node 24.22.1 符合。README 的 20.19.0 門檻不適用此工具版本；本文件提供釘版指令，不以 latest 隱式更新。

## 查核與修復

原 17 個 capability 將 108 個 Requirement 放在 Purpose 區，官方 CLI 全部忽略，造成 17 個 No delta sections 與整個 change 無 delta 的錯誤。此次只在每個 capability 第一條 Requirement 前加入 `## ADDED Requirements`，沒有變更需求內容、SHALL/MUST/SHOULD、情境或驗收門檻。移除新增標頭後與 baseline 17/17 檔逐字一致。

```bash
OPENSPEC_TELEMETRY=0 npm exec --yes --package @fission-ai/openspec@2.0.0 -- openspec list --json
OPENSPEC_TELEMETRY=0 npm exec --yes --package @fission-ai/openspec@2.0.0 -- openspec show bootstrap-smart-agriculture-platform --json --deltas-only
OPENSPEC_TELEMETRY=0 npm exec --yes --package @fission-ai/openspec@2.0.0 -- openspec validate bootstrap-smart-agriculture-platform --no-interactive
OPENSPEC_TELEMETRY=0 npm exec --yes --package @fission-ai/openspec@2.0.0 -- openspec validate bootstrap-smart-agriculture-platform --strict --no-interactive
python -m unittest discover -s tests -v
```

結果：一般 validate 有效但帶 3 警告；strict 仍不通過。警告為 Optimistic Concurrency、Dashboard Performance、Accessibility 使用 SHOULD 而非 SHALL/MUST。不可為消除警告擅自提高或降低產品承諾；需後續規格決策。結構防回歸 3/3 PASS（含原始缺標頭與非 delta 區隱藏需求的負向案例）。

此候選不代表階段 0 完整驗收、產品實作或正式部署完成。沒有執行 init/update 以免覆寫原有工具整合/治理文件；沒有 archive、任務勾完成、主線 spec 提升、Broker/真裝置連線、控制命令、身分憑證或正式服務。首次 CLI 執行顯示預設匿名 telemetry 提示，後續命令明確使用環境變數停用；未變更全域設定。
