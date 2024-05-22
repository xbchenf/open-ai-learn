# 在 gui_interface.py 中
import gradio as gr
import os
from utils import LOG, ConfigLoader
from model import OpenAIModel, GLMModel
from translator import PDFTranslator

# 定义一个全局变量来存储args
global_args = None

def translate_with_gui(pdf_tempfile, target_language, model_type, output_format):
    global global_args
    # 获取文件的真实路径
    pdf_path = pdf_tempfile.name

    # 转换语言输入
    language_mapping = {
        "中文": "Chinese",
        "日语": "Japanese",
        "西班牙语": "Spanish"
    }
    target_language = language_mapping.get(target_language, "Chinese")  # 默认为中文

    # 记录PDF文件路径和目标语言
    LOG.debug(f"PDF文件路径: {pdf_path}")
    LOG.debug(f"目标语言: {target_language}")

    config_loader = ConfigLoader(global_args.config)
    config = config_loader.load_config()

    #model = OpenAIModel(model=config['OpenAIModel']['model'], api_key=os.environ.get('OPENAI_API_KEY') or config['OpenAIModel']['api_key'])
    if model_type== "OpenAIModel":
        model = OpenAIModel(model=config['OpenAIModel']['model'], api_key=os.environ.get('OPENAI_API_KEY') or config['OpenAIModel']['api_key'])
    elif model_type == "GLMModel":
        model = GLMModel(model_url=config['GLMModel']['timeout'], timeout=config['GLMModel']['model_url'])
    else:
            model = OpenAIModel(model=config['OpenAIModel']['model'], api_key=os.environ.get('OPENAI_API_KEY') or config['OpenAIModel']['api_key'])
    output_format = output_format if output_format else config['common']['file_format']

    if output_format == "word" or output_format == "Markdown":
        return "暂不支持Markdown和word格式，请选择其他输出格式。"

    translator = PDFTranslator(model)

    output_path = translator.translate_pdf(pdf_path, output_format, target_language=target_language)
    return f"翻译成功! 输出到：{output_path}"

def launch_gui(args):
    global global_args
    global_args = args
    iface = gr.Interface(
        fn=translate_with_gui,
        inputs=[
            gr.File(label="上传PDF文件"),
            gr.Dropdown(choices=["中文", "日语", "西班牙语"], value="中文", label="选择目标语言"),  # 这里添加了default参数
            gr.Dropdown(choices=["OpenAIModel", "GLMModel"], value="OpenAIModel", label="选择大模型"),  # 这里添加了default参数
            gr.Radio(choices=["PDF", "Markdown","word"], value="PDF", label="选择输出格式")  # 选择输出格式

        ],
        outputs=gr.Textbox(label="输出结果")
    )
    iface.launch()

