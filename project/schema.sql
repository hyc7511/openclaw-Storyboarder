-- 影视制作工作区动态数据数据库 Schema
-- 版本: 2.1
-- 日期: 2026-04-22
-- 说明: 所有高频读写的动态数据统一使用 SQLite 管理
-- 特性: 安全初始化 - 只创建缺失的表，不覆盖已有数据

-- =============================================
-- 1. Agent 状态管理（agent_state）
-- =============================================
-- 记录当前进度、保存中间结果、支持断点续传
CREATE TABLE IF NOT EXISTS agent_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT DEFAULT '1.0',
    current_episode TEXT,
    current_stage TEXT DEFAULT 'init',
    
    -- 阶段状态（JSON存储）
    stages_json TEXT,
    
    -- 各 Agent 上下文（JSON存储）
    agents_json TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 默认初始化一条记录（如果不存在）
INSERT OR IGNORE INTO agent_state (id) VALUES (1);

-- =============================================
-- 2. 问题历史记录（issue_log）
-- =============================================
CREATE TABLE IF NOT EXISTS issue_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id TEXT NOT NULL UNIQUE,
    timestamp TEXT NOT NULL,
    description TEXT NOT NULL,
    problem_type TEXT NOT NULL,
    responsible_agent TEXT NOT NULL,
    affected_stage TEXT NOT NULL,
    checkpoint_added TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    occurrence_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 3. 活跃检查点（active_checkpoints）
-- =============================================
CREATE TABLE IF NOT EXISTS active_checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checkpoint TEXT NOT NULL,
    stage TEXT NOT NULL,
    trigger_issue TEXT NOT NULL,
    check_items TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 4. 演进统计汇总（evolution_summary）
-- =============================================
CREATE TABLE IF NOT EXISTS evolution_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_issues_identified INTEGER DEFAULT 0,
    issues_resolved INTEGER DEFAULT 0,
    active_checkpoints_count INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 默认初始化一条记录（如果不存在）
INSERT OR IGNORE INTO evolution_summary (id) VALUES (1);

-- =============================================
-- 5. 素材库索引（asset_index）- 可选
-- =============================================
CREATE TABLE IF NOT EXISTS asset_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_type TEXT NOT NULL, -- 'character' 或 'scene'
    asset_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    episode_id TEXT,
    file_path TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 索引优化（IF NOT EXISTS 确保安全）
-- =============================================
CREATE INDEX IF NOT EXISTS idx_issue_log_status ON issue_log(status);
CREATE INDEX IF NOT EXISTS idx_issue_log_agent ON issue_log(responsible_agent);
CREATE INDEX IF NOT EXISTS idx_issue_log_type ON issue_log(problem_type);
CREATE INDEX IF NOT EXISTS idx_active_checkpoints_stage ON active_checkpoints(stage);
CREATE INDEX IF NOT EXISTS idx_asset_index_type ON asset_index(asset_type);
