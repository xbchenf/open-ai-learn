import sys
import os
import gradio as gr
from gui import gui_interface

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator

# 检查当前模块是否是主模块，只有在脚本直接执行时才为True
if __name__ == "__main__":
    # 创建ArgumentParser对象，用于处理命令行参数
    argument_parser = ArgumentParser()
    # 调用解析函数，解析命令行参数
    args = argument_parser.parse_arguments()

    # 检查解析出的参数中是否包含GUI参数，如果包含则启动GUI模式
    if args.gui:
        # 调用gui_interface模块的launch_gui函数，传入解析出的参数
        gui_interface.launch_gui(args)
    else:
        # 如果不是GUI模式，则启动命令行模式
        # 创建ConfigLoader对象，用于加载配置文件
        config_loader = ConfigLoader(args.config)
        # 调用load_config函数，加载配置文件
        config = config_loader.load_config()
        # 根据用户选择的不同模型，创建不同的模型对象
        if args.model_type == "OpenAIModel":
            args.openai_model = args.openai_model or config['OpenAIModel']['model']
            args.openai_api_key = args.openai_api_key or os.environ.get('OPENAI_API_KEY') or config['OpenAIModel']['api_key']
            model = OpenAIModel(model=args.openai_model, api_key=args.openai_api_key)
        elif args.model_type == "GLMModel":
            args.timeout = args.timeout or config['GLMModel']['timeout']
            args.model_url = args.model_url or config['GLMModel']['model_url']
            model = GLMModel(model_url=args.model_url, timeout=args.timeout)
        else:
            raise ValueError("Invalid model_type specified. Please choose either 'GLMModel' or 'OpenAIModel'.")

        # 设置要翻译的书籍文件，如果命令行参数中没有则取配置文件中的值
        pdf_file_path = args.book if args.book else config['common']['book']

        # 设置文件格式，如果命令行参数中没有则取配置文件中的值
        args.file_format = args.file_format if args.file_format else config['common']['file_format']
        # 调用check_argument函数，检查参数是否完整
        argument_parser.check_argument(args)

        # 创建PDFTranslator对象，传入OpenAIModel对象
        translator = PDFTranslator(model)
        # 调用translate_pdf函数，开始翻译PDF文件
        translator.translate_pdf(pdf_file_path, args.file_format)
