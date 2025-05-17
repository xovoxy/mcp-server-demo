import os
import sqlite3
import requests
import hashlib
import time
import hmac
from urllib.parse import urlencode
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

@mcp.tool()
def get_weather(city: str) -> dict:
    """获取指定城市的天气信息
    
    Args:
        city (str): 城市名称，如"beijing"
    """
    try:
        # API URL
        url = "https://api.seniverse.com/v3/weather/now.json"
        
        # 参数
        params = {
            'key': "SgM08cTbvwPvOp82s",
            'location': city,
            'language': 'zh-Hans',
            'unit': 'c'
        }
        
        # 如果提供了secret，使用HMAC-SHA1签名
        if api_secret:
            params['ts'] = int(time.time())  # 当前时间戳
            params['uid'] = 'YOUR_USER_ID'  # 替换为您的用户ID
            
            # 构建签名
            signature_string = urlencode(sorted(params.items()))
            signature = hmac.new(
                api_secret.encode(),
                signature_string.encode(),
                hashlib.sha1
            ).hexdigest()
            
            params['sig'] = signature
        
        # 发送请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果请求失败则抛出异常
        
        # 解析响应
        data = response.json()
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def write_to_txt(content: str, filename: str) -> dict:
    """Write content to a specified txt file
    
    Args:
        content (str): Content to write to the file
        filename (str): Name of the txt file (with .txt extension)
    """
    try:
        # Get desktop path
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Create full file path
        file_path = os.path.join(desktop_path, filename)
        
        # Check if filename ends with .txt
        if not filename.endswith('.txt'):
            return {
                "success": False,
                "error": "Filename must end with .txt extension"
            }
            
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return {
            "success": True,
            "message": f"Content successfully written to {filename}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# def init_db():
#     conn = sqlite3.connect("tasks.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS tasks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL,
#             description TEXT
#         )
#     """)

# @mcp.tool()
# def add_task_to_db(title: str, description: str, sql: str) -> str:
#     """将任务添加到数据库中

#     Args:
#         title (str): 任务标题
#         description (str): 任务描述
#         sql (str): 根据任务标题(title)和任务描述(description)，生成一条插入的sql，必填项。表的结构为 CREATE TABLE IF NOT EXISTS tasks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL,
#             description TEXT
#         )
#     """
    
#     try:
#         conn = sqlite3.connect("tasks.db")
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         conn.commit()
#         conn.close()
#         return "add task success"
#     except Exception as e:
#         return f"add task failed, error {e}"
    
# @mcp.tool()
# def getTask() -> dict:
#     """ 获取所有任务 """
#     try:
#         conn = sqlite3.connect("tasks.db")
#         cursor = conn.cursor()
#         cursor.execute("select * from tasks")
#         tasks = cursor.fetchall()
#         conn.close()
#         task_list = [
#             {"任务标题": task[1], "任务描述": task[2]} for task in tasks
#         ]
        
#         return {"success": True, "tasks": task_list}
#     except Exception as e:
#         print(f"get task error {e}")
#         return {"success": False, "error": e}


if __name__ == "__main__":
    # init_db()
    mcp.run(transport="stdio")
