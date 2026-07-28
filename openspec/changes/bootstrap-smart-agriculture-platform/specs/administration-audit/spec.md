# Administration and Audit Capability

## Purpose

定義平台治理後台、管理員權限、設定版本、稽核紀錄、安全事件與支援查詢。

### Requirement: Administrative Role Separation

系統 SHALL 區分 `platform_admin`、`support_operator`、`security_auditor` 與 `ai_governor` 等治理權限，且高風險操作 MUST 依最小權限原則限制。

#### Scenario: Support operator changes platform security settings

- GIVEN 使用者只有 support_operator 權限
- WHEN 嘗試修改 MQTT 憑證政策
- THEN 系統 SHALL 回傳 403
- AND SHALL 記錄被拒絕的管理操作

### Requirement: Organization and User Governance

授權管理員 SHALL 能查詢、停用與恢復帳號或組織，但不得直接取得使用者密碼、裝置祕密或未遮罩 Token。

#### Scenario: Administrator suspends an organization

- GIVEN 組織存在重大違規或安全事件
- WHEN platform_admin 提交停用原因
- THEN 系統 SHALL 將組織標記為 suspended
- AND SHALL 阻止新的私有資料寫入與設備命令
- AND SHALL 記錄原因、操作者、時間與影響範圍

### Requirement: Immutable Audit Trail

所有敏感操作 SHALL 建立 append-only 稽核事件，至少包含 actor、action、resource、organization、result、reason、IP/Client metadata、correlation ID 與 timestamp。

#### Scenario: Device credential is rotated

- GIVEN 授權使用者輪替裝置憑證
- WHEN 操作成功
- THEN 系統 SHALL 建立稽核事件
- AND 稽核內容 MUST NOT 包含新舊祕密明文

#### Scenario: Audit record modification is attempted

- GIVEN 稽核事件已建立
- WHEN 一般應用流程嘗試更新或刪除
- THEN 系統 MUST 拒絕操作
- AND SHALL 產生安全事件

### Requirement: Configuration Versioning

告警政策、AI Prompt、模型路由、資料保存、裝置安全限制與公開追溯白名單等設定 MUST 版本化並支援查看差異與回滾。

#### Scenario: Alert policy is rolled back

- GIVEN 新版告警政策造成誤報
- WHEN 授權管理員回滾至前一核准版本
- THEN 系統 SHALL 建立新生效版本指向回滾內容
- AND SHALL 保留原版本與回滾原因

### Requirement: Security Incident Management

系統 SHALL 支援建立、分類、指派、調查與關閉安全事件，嚴重度至少包含 low、medium、high、critical。

#### Scenario: Repeated unauthorized MQTT publish is detected

- GIVEN 同一憑證多次向未授權 Topic 發布
- WHEN 超過安全門檻
- THEN 系統 SHALL 建立或更新安全事件
- AND MAY 自動撤銷憑證
- AND SHALL 通知 security_auditor

### Requirement: Support Access Control

支援人員查看租戶資料 SHALL 具有明確原因、最小資料範圍、時效與稽核；高敏感資料 SHOULD 採遮罩或核准流程。

#### Scenario: Support opens a producer account

- GIVEN Producer 提出支援單
- WHEN support_operator 進入協助模式
- THEN 系統 SHALL 要求輸入支援原因
- AND SHALL 顯示支援模式標記
- AND SHALL 記錄所有查詢與操作

### Requirement: Administrative Export

管理員匯出使用者、設備、AI 或稽核資料時 SHALL 套用權限、遮罩、時間範圍與下載有效期限。

#### Scenario: Audit export is generated

- GIVEN security_auditor 具有匯出權限
- WHEN 申請指定期間稽核報表
- THEN 系統 SHALL 以非同步工作產生檔案
- AND SHALL 提供短效下載連結
- AND SHALL 記錄匯出範圍與下載事件
