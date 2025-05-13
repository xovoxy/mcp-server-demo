import os
import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("desttop_files")


@mcp.tool()
def getFiles():
    " 获取当前桌面的文件 "
    # Get desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Get all txt files in desktop directory
    txt_files = [f for f in os.listdir(desktop_path) if f.endswith('.txt')]

    # Print the txt files found
    print("Text files found on desktop:")
    return "\n---\n".join(txt_files)


def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT
        )
    """)

@mcp.tool()
def add_task_to_db(title: str, description: str, sql: str) -> str:
    """将任务添加到数据库中

    Args:
        title (str): 任务标题
        description (str): 任务描述
        sql (str): 根据任务标题(title)和任务描述(description)，生成一条插入的sql，必填项。表的结构为 CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT
        )
    """
    
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return "add task success"
    except Exception as e:
        return f"add task failed, error {e}"
    
@mcp.tool()
def getTask() -> dict:
    """ 获取所有任务 """
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("select * from tasks")
        tasks = cursor.fetchall()
        conn.close()
        task_list = [
            {"任务标题": task[1], "任务描述": task[2]} for task in tasks
        ]
        
        return {"success": True, "tasks": task_list}
    except Exception as e:
        print(f"get task error {e}")
        return {"success": False, "error": e}


if __name__ == "__main__":
    init_db()
    mcp.run(transport="stdio")
