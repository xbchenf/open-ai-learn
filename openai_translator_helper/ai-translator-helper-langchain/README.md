# OpenAI-based Document Translation Project

本项目基于OpenAI实现文档语言的翻译，可以将输入的文本从一种语言翻译成另一种语言。

## 安装

首先，你需要安装Python 3.7或者更高的版本。

然后，你可以使用pip来安装项目的依赖：

```bash
pip install -r requirements.txt
```

## 使用

项目的主要接口是`main`函数。可以通过以下方式调用：

```python
python ai_translator-helper/main.py --model_type OpenAIModel --api_key $OPENAI_API_KEY  --gui
```


你也可以在命令行里面运行
```python
# Set your api_key as an env variable
export OPENAI_API_KEY="sk-xxx"
python ai_translator/main.py --model_type OpenAIModel --api_key $OPENAI_API_KEY --book your_book

```


```python
## Windows CMD 窗口调用命令
python openai-translator-pro/main.py --model_type OpenAIModel --openai_api_key %OPENAI_KEY%  --gui
```

这将会将"你上传的文件翻译成目标语言！

## 功能

- 支持多种语言的翻译
- 基于OpenAI底层框架，能够提供准确且流畅的翻译
- 可以处理大量文本的翻译

## 贡献
这个项目很多代码也是来自于开源网站，感谢代码的作者，感谢社区
如果你对此项目感兴趣并且想要为之贡献代码，欢迎提交pull requests。如果发现bug或者有新的功能需求，也欢迎提交issues。

## 开源协议

该项目是在MIT开源协议下发布的。有关详情，请参阅[LICENSE](LICENSE)。

## 联系我们

如果你有任何问题或者建议，可以通过电子邮件联系我们：`your-email@example.com`。

## 免责声明

这只是一个基于OpenAI的翻译项目，任何人在使用此项目时，必须遵守OpenAI的使用政策，我们对使用此项目可能产生的任何损失或者问题不承担任何责任。

