#!/usr/bin/env python3
"""
初始化动态数据数据库
版本: 2.1
日期: 2026-04-22
特性: 安全初始化 - 只创建缺失的表，不覆盖已有数据
"""

from evolution_db import EvolutionDB


def main():
    print("=" * 60)
    print("影视制作工作区 - 动态数据数据库初始化")
    print("=" * 60)
    
    # 初始化数据库（自动检查已存在会安全连接）
    db = EvolutionDB(auto_init=True)
    
    print("\n" + "=" * 60)
    print("数据库状态检查")
    print("=" * 60)
    
    # 检查数据库状态
    status = db.check_db_status()
    
    # 显示详细状态
    print("\n[路径] " + status['path'])
    print("[表结构]")
    for table, state in status['tables'].items():
        count = status['stats'].get(f'{table}_count', 0)
        if state == 'OK':
            print(f"  ✅ {table} (记录: {count})")
        else:
            print(f"  ❌ {table} (MISSING)")
    
    print("\n" + "=" * 60)
    print("初始化摘要")
    print("=" * 60)
    
    # 获取当前状态
    state = db.get_agent_state()
    summary = db.get_summary()
    
    print(f"\n[当前阶段] {state.get('current_stage')}")
    print(f"[当前集数] {state.get('current_episode')}")
    print(f"[问题总数] {summary.get('total_issues_identified', 0)}")
    print(f"[已解决问题] {summary.get('issues_resolved', 0)}")
    print(f"[活跃检查点] {summary.get('active_checkpoints_count', 0)}")
    
    print("\n" + "=" * 60)
    print("数据库已就绪！")
    print("=" * 60)
    print("\n快速命令:")
    print("  查看当前状态     - 显示当前工作状态")
    print("  查看统计          - 显示统计信息")
    print("  查看检查点        - 显示活跃检查点")
    print("  查看问题列表      - 显示所有问题")
    print("  初始化数据库      - 初始化或检查数据库")
    print("  导出数据备份      - 导出JSON格式备份")
    print("\n详细使用 'python evolution_db.py help' 查看完整帮助")
    
    db.close()


if __name__ == '__main__':
    main()
