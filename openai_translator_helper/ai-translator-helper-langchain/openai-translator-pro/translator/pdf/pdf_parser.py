import pdfplumber
from typing import Optional
from document import Book, Page, Content, ContentType, TableContent, Paragraph
from exceptions.exceptions import PageOutOfRangeException
from utils import LOG

class PDFParser:
    def __init__(self):
        pass

    # 定义parse_pdf函数，用于解析PDF文件
    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        # 创建一个Book对象
        book = Book(pdf_file_path)

        # 打开PDF文件
        with pdfplumber.open(pdf_file_path) as pdf:
            # 如果指定了解析的页数，并且大于实际的页数，则抛出PageOutOfRangeException错误
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            # 如果没有指定解析的页数，则解析全部的页数；否则解析指定的页数
            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            # 遍历需要解析的页数
            for pdf_page in pages_to_parse:
                # 创建一个Page对象
                page = Page()
                # 解析文字
                words = pdf_page.extract_words()
                # 解析表格
                tables = pdf_page.extract_tables()

                # 从原文中移除表格中的内容
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            if cell is not None:
                                idx = 0
                                # 在单词列表中搜索和单元格内容匹配的单词，并将其移除
                                while idx < len(words):
                                    match, next_idx = self.words_match_cell(words, idx, cell)
                                    if match:
                                        del words[idx:next_idx]
                                        idx = next_idx - 1
                                    idx += 1

                # 按照top值将单词分组，以检测行
                lines = {}
                for word in words:
                    lines.setdefault(word['top'], []).append(word)

                # 将分组后的行按照top值进行排序
                grouped_lines = sorted(lines.values(), key=lambda l: l[0]['top'])

                # 根据行之间的空白空间或大间距构建段落
                paragraphs = []
                current_paragraph = []
                previous_bottom = 0
                for line_words in grouped_lines:
                    # 假设间隔大于10的行表示新段落的开始
                    if previous_bottom and (line_words[0]['top'] - previous_bottom) > 10:
                        paragraphs.append(current_paragraph)
                        current_paragraph = []

                    # 向当前段落中添加行
                    current_paragraph.extend(line_words)
                    previous_bottom = line_words[0]['bottom']

                # 将最后一个段落添加到段落列表中
                if current_paragraph:
                    paragraphs.append(current_paragraph)

                # 创建Content对象，内容类型为TEXT，原文为空字符串
                content = Content(content_type=ContentType.TEXT, original="")
                for paragraph_words in paragraphs:
                    # 将段落中的单词连接成字符串
                    paragraph_text = " ".join([word['text'] for word in paragraph_words])

                    # 从第一个单词中提取样式
                    style = self.extract_style_from_word(paragraph_words[0])

                    # 向original属性中添加每个段落，并插入分隔符
                    if content.original:
                        content.original += '\n' + "¶¶¶" + '\n'
                    content.original += paragraph_text

                    # 构建段落布局
                    layout = {
                        'top': paragraph_words[0]['top'],
                        'bottom': paragraph_words[-1]['bottom']
                    }
                    # 创建Paragraph对象，并添加到Content对象中
                    paragraph = Paragraph(text=paragraph_text, layout=layout, style=style)
                    content.add_paragraph(paragraph)
                # 更新Content对象的布局
                content.update_layout()

                # 将Content对象添加到Page对象中
                page.add_content(content)

                # 处理表格
                tables_objects = pdf_page.find_tables()
                for table_index, table_obj in enumerate(tables_objects):
                    # 获取表格的边界
                    table_bbox = table_obj.bbox
                    # 构建表格布局
                    table_layout = {
                        'top': table_bbox[1],
                        'bottom': table_bbox[3],
                        'left': table_bbox[0],  # 获取表格的左边界
                        'right': table_bbox[2]  # 获取表格的右边界
                    }
                    # 创建TableContent对象，并添加到Page对象中
                    table = TableContent(tables[table_index], layout=table_layout)
                    page.add_content(table)
                    # 打印表格内容
                    LOG.debug(f"[table]\n{table}")

                # 将Page对象添加到Book对象中
                book.add_page(page)

        # 返回Book对象
        return book

    # 使用扩展匹配从文本中删除表格单元格中的文字。扩展匹配：在检查是否移除一个单词之前，考虑单词及其后面的几个单词与单元格内容的匹配。
    def words_match_cell(self, words, start_idx, cell_text):
        end_idx = start_idx
        combined_text = ''
        cell_text_cleaned = cell_text.replace("\n", " ").strip()  # 对单元格文本进行清理，替换换行符为空格
        
        while end_idx < len(words) and combined_text.strip() != cell_text_cleaned:
            combined_text += ' ' + words[end_idx]['text']
            end_idx += 1

        return combined_text.strip() == cell_text_cleaned, end_idx

    #   这个方法没有完全实现，只简单估计了文本大小
    def extract_style_from_word(self, word):
         # Use 'top' and 'bottom' to estimate the font size
        font_height = word['bottom'] - word['top']
        
        style = {
            "size": font_height,  # Use the calculated font height as size
            "font": word.get('font', None),  # Example to extract font. Adjust based on Word object's attributes
            # You may need more intricate logic to determine 'bold' and 'italy' properties based on font names or other attributes.
            "bold": "Bold" in word.get('font', ''),
            "italy": "Ital" in word.get('font', '') or "Italic" in word.get('font', '')
        }
        return style

    