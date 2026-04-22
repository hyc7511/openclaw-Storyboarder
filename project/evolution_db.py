#!/usr/bin/env python3
"""
影视制作工作区动态数据数据库管理工具
版本: 2.1
日期: 2026-04-22
说明: 
- 统一管理所有动态数据 - Agent状态、问题记录、检查点等
- 支持安全初始化 - 只创建缺失的表，不覆盖已有数据
- 对话友好的API设计
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any


class EvolutionDB:
    """动态数据数据库管理类 - 完整版本"""
    
    def __init__(self, db_path: str = "evolution_log.db", auto_init: bool = True):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库文件路径
            auto_init: 是否自动初始化（如果数据库不存在）
        """
        self.db_path = db_path
        self.conn = None
        
        if auto_init:
            self._ensure_db_exists()
        else:
            if os.path.exists(self.db_path):
                self.conn = sqlite3.connect(self.db_path)
                self.conn.row_factory = sqlite3.Row
    
    def _ensure_db_exists(self):
        """确保数据库和表结构存在 - 安全初始化"""
        if not os.path.exists(self.db_path):
            print(f"[创建] 数据库不存在，正在创建: {self.db_path}")
            self._create_database()
        else:
            print(f"[连接] 数据库已存在，正在连接: {self.db_path}")
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            # 安全检查 - 确保所有表都存在
            self._verify_or_create_tables()
    
    def _create_database(self):
        """创建数据库和表结构 - 安全初始化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())
        else:
            self._create_tables_fallback(cursor)
        
        conn.commit()
        conn.close()
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        print(f"[完成] 数据库已创建")
    
    def _create_tables_fallback(self, cursor):
        """备用表创建方案（安全创建）"""
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT DEFAULT '1.0',
            current_episode TEXT,
            current_stage TEXT DEFAULT 'init',
            stages_json TEXT,
            agents_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''
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
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_checkpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checkpoint TEXT NOT NULL,
            stage TEXT NOT NULL,
            trigger_issue TEXT NOT NULL,
            check_items TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS evolution_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_issues_identified INTEGER DEFAULT 0,
            issues_resolved INTEGER DEFAULT 0,
            active_checkpoints_count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # INSERT OR IGNORE 确保不覆盖已有数据
        cursor.execute('INSERT OR IGNORE INTO agent_state (id) VALUES (1)')
        cursor.execute('INSERT OR IGNORE INTO evolution_summary (id) VALUES (1)')
    
    def _verify_or_create_tables(self):
        """验证表存在，缺失的话安全创建"""
        cursor = self.conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = []
        required_tables = ['agent_state', 'issue_log', 'active_checkpoints', 'evolution_summary']
        
        for table in required_tables:
            if table not in tables:
                missing_tables.append(table)
        
        if missing_tables:
            print(f"[警告] 发现缺失表: {missing_tables}")
            print("[修复] 正在创建缺失的表...")
            # 重新执行schema.sql来创建缺失的表
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    cursor.executescript(f.read())
                self.conn.commit()
                print("[完成] 缺失表已创建")
        else:
            print("[检查] 所有表结构正常")
    
    def check_db_status(self) -> Dict:
        """检查数据库状态（对话友好）"""
        cursor = self.conn.cursor()
        
        status = {
            "exists": True,
            "path": self.db_path,
            "tables": {},
            "stats": {}
        }
        
        # 检查表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in ['agent_state', 'issue_log', 'active_checkpoints', 'evolution_summary']:
            if table in tables:
                status["tables"][table] = "OK"
                # 获取记录数
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                status["stats"][f"{table}_count"] = count
            else:
                status["tables"][table] = "MISSING"
        
        return status
    
    def get_agent_state(self) -> Dict:
        """获取Agent状态"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM agent_state WHERE id = 1')
        row = cursor.fetchone()
        
        state = dict(row) if row else {}
        
        if state.get('stages_json'):
            state['stages'] = json.loads(state['stages_json'])
        else:
            state['stages'] = {
                "director_analysis": {"status": "pending", "last_updated": None, "review_count": 0},
                "art_design": {"status": "pending", "last_updated": None, "review_count": 0},
                "storyboard": {"status": "pending", "last_updated": None, "review_count": 0}
            }
        
        if state.get('agents_json'):
            state['agents'] = json.loads(state['agents_json'])
        else:
            state['agents'] = {
                "director": {"context": {}, "resumable": True},
                "art-designer": {"context": {}, "resumable": True},
                "storyboard-artist": {"context": {}, "resumable": True}
            }
        
        return state
    
    def update_agent_state(self, current_episode: Optional[str] = None,
                          current_stage: Optional[str] = None,
                          stages: Optional[Dict] = None,
                          agents: Optional[Dict] = None):
        """更新Agent状态"""
        cursor = self.conn.cursor()
        
        update_data = {}
        if current_episode is not None:
            update_data['current_episode'] = current_episode
        if current_stage is not None:
            update_data['current_stage'] = current_stage
        if stages is not None:
            update_data['stages_json'] = json.dumps(stages, ensure_ascii=False)
        if agents is not None:
            update_data['agents_json'] = json.dumps(agents, ensure_ascii=False)
        
        if not update_data:
            return
        
        update_data['updated_at'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f"{k} = ?" for k in update_data.keys()])
        values = list(update_data.values()) + [1]
        
        cursor.execute(f'UPDATE agent_state SET {set_clause} WHERE id = ?', values)
        self.conn.commit()
    
    def add_issue(self, description: str, problem_type: str,
                  responsible_agent: str, affected_stage: str,
                  checkpoint_added: Optional[str] = None) -> str:
        """添加新问题记录"""
        timestamp = datetime.now().isoformat()
        issue_id = f"ISSUE-{self._get_next_issue_id()}"
        
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO issue_log 
            (issue_id, timestamp, description, problem_type, responsible_agent, affected_stage, checkpoint_added)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (issue_id, timestamp, description, problem_type, responsible_agent, affected_stage, checkpoint_added))
            
            self._increment_issue_count()
            
            if checkpoint_added:
                self._add_checkpoint(checkpoint_added, affected_stage, problem_type)
            
            self.conn.commit()
            return issue_id
            
        except sqlite3.IntegrityError:
            self.conn.rollback()
            cursor.execute('''
            UPDATE issue_log 
            SET occurrence_count = occurrence_count + 1, updated_at = CURRENT_TIMESTAMP
            WHERE problem_type = ? AND status = 'active'
            ''', (problem_type,))
            self.conn.commit()
            return self._get_issue_id_by_type(problem_type)
    
    def _get_next_issue_id(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute('SELECT MAX(id) FROM issue_log')
        result = cursor.fetchone()
        return (result[0] or 0) + 1
    
    def _get_issue_id_by_type(self, problem_type: str) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT issue_id FROM issue_log WHERE problem_type = ? AND status = ? LIMIT 1',
                      (problem_type, 'active'))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def _add_checkpoint(self, checkpoint: str, stage: str, trigger_issue: str,
                       check_items: Optional[List[str]] = None):
        cursor = self.conn.cursor()
        
        check_items_json = json.dumps(check_items, ensure_ascii=False) if check_items else None
        
        try:
            cursor.execute('''
            INSERT INTO active_checkpoints (checkpoint, stage, trigger_issue, check_items)
            VALUES (?, ?, ?, ?)
            ''', (checkpoint, stage, trigger_issue, check_items_json))
            self._increment_checkpoint_count()
        except sqlite3.IntegrityError:
            pass
    
    def get_checkpoints(self, stage: Optional[str] = None) -> List[Dict]:
        cursor = self.conn.cursor()
        
        if stage:
            cursor.execute('SELECT * FROM active_checkpoints WHERE stage = ? AND is_active = 1', (stage,))
        else:
            cursor.execute('SELECT * FROM active_checkpoints WHERE is_active = 1')
        
        checkpoints = [dict(row) for row in cursor.fetchall()]
        
        for cp in checkpoints:
            if cp.get('check_items'):
                try:
                    cp['check_items'] = json.loads(cp['check_items'])
                except:
                    pass
        
        return checkpoints
    
    def get_issues(self, status: Optional[str] = None) -> List[Dict]:
        cursor = self.conn.cursor()
        if status:
            cursor.execute('SELECT * FROM issue_log WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor.execute('SELECT * FROM issue_log ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_summary(self) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM evolution_summary WHERE id = 1')
        result = cursor.fetchone()
        return dict(result) if result else {}
    
    def resolve_issue(self, issue_id: str):
        cursor = self.conn.cursor()
        
        cursor.execute('''
        UPDATE issue_log SET status = 'resolved', updated_at = CURRENT_TIMESTAMP WHERE issue_id = ?
        ''', (issue_id,))
        
        cursor.execute('UPDATE evolution_summary SET issues_resolved = issues_resolved + 1')
        
        cursor.execute('''
        UPDATE active_checkpoints SET is_active = 0 WHERE trigger_issue IN (
            SELECT problem_type FROM issue_log WHERE issue_id = ?
        )
        ''', (issue_id,))
        
        cursor.execute('''
        UPDATE evolution_summary SET active_checkpoints_count = (
            SELECT COUNT(*) FROM active_checkpoints WHERE is_active = 1
        )
        ''')
        
        self.conn.commit()
    
    def _increment_issue_count(self):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE evolution_summary SET total_issues_identified = total_issues_identified + 1')
    
    def _increment_checkpoint_count(self):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE evolution_summary SET active_checkpoints_count = (SELECT COUNT(*) FROM active_checkpoints WHERE is_active = 1)')
    
    def export_to_json(self, output_file: str = "data_export.json"):
        data = {
            "version": "2.1",
            "last_updated": datetime.now().isoformat(),
            "agent_state": self.get_agent_state(),
            "issue_log": self.get_issues(),
            "active_checkpoints": self.get_checkpoints(),
            "evolution_summary": self.get_summary()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return output_file
    
    def import_from_json(self, input_file: str):
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'agent_state' in data:
            state = data['agent_state']
            self.update_agent_state(
                current_episode=state.get('current_episode'),
                current_stage=state.get('current_stage'),
                stages=state.get('stages'),
                agents=state.get('agents')
            )
    
    def migrate_from_json(self, agent_state_path: Optional[str] = None,
                       evolution_log_path: Optional[str] = None):
        """从旧的JSON文件迁移数据"""
        migrated = []
        
        if agent_state_path and os.path.exists(agent_state_path):
            with open(agent_state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.update_agent_state(
                    current_episode=state.get('current_episode'),
                    current_stage=state.get('current_stage'),
                    stages=state.get('stages'),
                    agents=state.get('agents')
                )
            migrated.append("agent_state")
        
        if evolution_log_path and os.path.exists(evolution_log_path):
            with open(evolution_log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for issue in data.get('issue_log', []):
                    self.add_issue(
                        issue.get('description', ''),
                        issue.get('problem_type', ''),
                        issue.get('responsible_agent', ''),
                        issue.get('affected_stage', ''),
                        issue.get('checkpoint_added')
                    )
            migrated.append("evolution_log")
        
        return migrated
    
    def close(self):
        if self.conn:
            self.conn.close()


def main():
    import sys
    db = EvolutionDB()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init':
            status = db.check_db_status()
            print("=" * 50)
            print("数据库状态检查")
            print("=" * 50)
            for table, state in status['tables'].items():
                count = status['stats'].get(f'{table}_count', 0)
                print(f"  {table}: {state} (记录: {count})")
            print("=" * 50)
        
        elif command == 'state':
            state = db.get_agent_state()
            summary = db.get_summary()
            print("=" * 50)
            print("当前状态")
            print("=" * 50)
            print(f" 当前阶段: {state.get('current_stage')}")
            print(f" 当前集数: {state.get('current_episode')}")
            print(f" 问题总数: {summary.get('total_issues_identified', 0)}")
            print(f" 已解决: {summary.get('issues_resolved', 0)}")
        
        elif command == 'summary':
            summary = db.get_summary()
            print("=" * 50)
            print("统计摘要")
            print("=" * 50)
            print(f" 问题总数: {summary.get('total_issues_identified', 0)}")
            print(f" 已解决: {summary.get('issues_resolved', 0)}")
            print(f" 活跃检查点: {summary.get('active_checkpoints_count', 0)}")
        
        elif command == 'list-issues':
            issues = db.get_issues()
            print("=" * 50)
            print(f"问题列表 ({len(issues)})")
            print("=" * 50)
            for issue in issues:
                status_mark = "✅" if issue['status'] == 'resolved' else "🔴"
                print(f"  {status_mark} {issue['issue_id']}: {issue['description']}")
        
        elif command == 'checkpoints':
            checkpoints = db.get_checkpoints()
            print("=" * 50)
            print(f"活跃检查点 ({len(checkpoints)})")
            print("=" * 50)
            for cp in checkpoints:
                print(f"  {cp['checkpoint']} ({cp['stage']})")
        
        elif command == 'export':
            out_file = sys.argv[2] if len(sys.argv) > 2 else "data_export.json"
            exported_file = db.export_to_json(out_file)
            print(f"数据已导出到: {exported_file}")
        
        elif command == 'migrate':
            agent_path = sys.argv[2] if len(sys.argv) > 2 else ".agent-state.json"
            evol_path = sys.argv[3] if len(sys.argv) > 3 else "evolution_log.json"
            migrated = db.migrate_from_json(agent_path, evol_path)
            print(f"已迁移: {', '.join(migrated)}")
        
        elif command == 'status':
            status = db.check_db_status()
            print("=" * 50)
            print("数据库状态")
            print("=" * 50)
            print(f"  路径: {status['path']}")
            print("  表:")
            for table, state in status['tables'].items():
                count = status['stats'].get(f'{table}_count', 0)
                print(f"    {table}: {state} (记录: {count})")
        
        elif command == 'help':
            print("=" * 50)
            print("影视制作数据库工具 v2.1")
            print("=" * 50)
            print("可用命令:")
            print("  init         - 安全初始化数据库")
            print("  state        - 显示当前状态")
            print("  summary      - 显示统计摘要")
            print("  list-issues  - 列出所有问题")
            print("  checkpoints  - 列出活跃检查点")
            print("  export       - 导出为JSON备份")
            print("  migrate      - 从旧JSON迁移")
            print("  status       - 检查数据库状态")
            print("  help         - 显示帮助")
            print("\n对话式命令（在OpenClaw中）:")
            print("  查看当前状态, 查看统计, 列出问题")
            print("  查看检查点, 初始化数据库")
        
        else:
            print(f"未知命令: {command}")
            print("使用 'help' 查看帮助")
    
    else:
        print("=" * 50)
        print("影视制作数据库工具 v2.1")
        print("=" * 50)
        print("使用 'help' 查看帮助")
    
    db.close()


if __name__ == '__main__':
    main()
