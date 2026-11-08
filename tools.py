from datetime import datetime

def get_current_time() ->str:
    """返回当前日期时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression: str) -> str:
    """计算数学表达式，比如 ‘23 * 45 + 1’ """
    try:
        return str(eval(expression))  # demo 用 eval，生产环境别这么干
    except Exception as e:
        return f"计算失败：{e}"

# 把函数的“说明书”写给大模型看（JSON Schema 格式）
tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_current_time",
            "description" : "获取当前的日期和时间",
            "parameters" : {
                "type" : "object",
                "properties" : {}     # 因为获取当前时间没有参数，所以"required"也不需要
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "calculate",                  # 工具(函数)名
            "description" : "计算一个数学表达式",      # 这个工具是干嘛的（大模型主要靠这句话来决定要不要用它！！）
            "parameters" : {                       # 参数，可能多个
                "type" : "object",                 # 告诉大模型，你要传给我的这组参数是一个“对象”
                "properties" : {                  # 定义传参字段的规则，可能有多个传参，每个参数字段一个单独字典定义规则
                    "expression" : {               # "expression"表达式参数字段规则
                        "type" : "string",                        # 告诉大模型，这个字段的数据类型必须是字符串（不能传数字 23*45，得传带引号的 "23*45"）
                        "description" : "要计算的表达式，如 23*45"   # 这是最关键的！ 告诉大模型这个字段是干嘛用的。如果大模型想算 10+20，看到这个描述，它就知道要在 expression 里填 "10+20"
                    }
                },
                "required" : ["expression"]     # 传参（必填），因为可能需要多个传参所以是列表
            }
        }
    }
]

# 函数名 -> 实际函数 的映射
tools_map = {"get_current_time" : get_current_time, "calculate" : calculate}