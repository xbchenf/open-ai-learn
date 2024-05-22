# 导入json包
import json

# 导入quart（python的异步web框架）和quart_cors（quart的CORS（跨源资源共享）支持）
import quart
import quart_cors
from quart import request

# 创建一个允许来自 "https://chat.openai.com" 的跨域请求的quart应用
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# 用于跟踪待办事项的字典。如果Python会话重新启动，这些数据将不会被保存。
_TODOS = {}

# 定义一个POST请求的处理函数，接受一个用户名作为URL路径的一部分
@app.post("/todos/<string:username>")
async def add_todo(username):
    # 获取请求的json数据，force参数设置为True，即无论header的content-type是什么都强制解析为json
    request = await quart.request.get_json(force=True)
    # 如果用户名在_TODOS字典中不存在，则初始化一个空列表
    if username not in _TODOS:
        _TODOS[username] = []
    # 将待办事项添加到对应用户的待办事项列表中
    _TODOS[username].append(request["todo"])
    # 返回一个带有200状态码和'OK'响应体的HTTP响应
    return quart.Response(response='OK', status=200)

# 定义一个GET请求的处理函数，接受一个用户名作为URL路径的一部分，返回该用户的所有待办事项
@app.get("/todos/<string:username>")
async def get_todos(username):
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

# 定义一个DELETE请求的处理函数，接受一个用户名作为URL路径的一部分，删除该用户的指定待办事项
@app.delete("/todos/<string:username>")
async def delete_todo(username):
    request = await quart.request.get_json(force=True)
    todo_idx = request["todo_idx"]
    # 如果待办事项的索引在合理范围内，就删除那个待办事项，否则不做任何事情
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)

# 定义一个GET请求的处理函数，返回一个图像文件
@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

# 定义一个GET请求的处理函数，返回一个包含插件信息的JSON文件
@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

# 定义一个GET请求的处理函数，返回一个OpenAPI规范的YAML文件
@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

# 主函数，运行这个quart应用
def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

# 如果这个脚本是直接运行而非被导入，则运行主函数
if __name__ == "__main__":
    main()
