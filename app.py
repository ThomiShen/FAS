from flask import Flask, render_template, request,url_for,redirect
app = Flask(__name__)
import os
from docx import Document
from cut import StockInfoExtractor
from collections import defaultdict
import AI
from kline import  StockKLinePlotter
import akshare as ak
import zhifu
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        word_file=request.files['docxFile']
        if word_file:
            # 保存文件到指定的上传文件夹
            filename = os.path.join(app.config['UPLOAD_FOLDER'], word_file.filename)
            word_file.save(filename)
            doc=Document(word_file)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            content = '\n'.join(fullText)
            # api='sess-bcEjvU9LZMr2FcwCoMJRD1FOaoXv51Zia0CkS1T7'
            # ai=AI.Evaluator(api)
#             prompt="""
#             上面的内容是最近的热点信息，你作为金融数据分析师，我希望你提取这个信息中上市公司的股票信息，根据提供的信息，我需要知道上市公司的股票信息。
# 请确保返回的数据格式为：{股票名称1:股票代码1:股票1主营业务简介}、{股票名称2:股票代码2:股票2主营业务简介}...。
# 例如：{大富科技:300134:国内领先的移动通信设备......}、{宜安科技:300328:公司在新能源汽车、液态金属新材料行业.....}。请确保每个公司的信息都按照这种格式返回，并且不要添加任何额外的内容或注释。
#             """
            # content=content+'\n'+prompt
            # information=ai.get_evaluation(content)
            # result=ai.extract_company_info(information)
            cut=StockInfoExtractor()
            result=cut.get_stock_details(content)
            # 将股票按照行业分类
            industry_dict = {}
            for stock in result:
                industry = stock[2]
                if industry not in industry_dict:
                    industry_dict[industry] = []
                industry_dict[industry].append(stock)
        return render_template('zhifudaima.html', content=industry_dict )
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/visualization')
def visualization():
    return render_template('visualization.html')
@app.route('/information')
def information():
    huilv = ak.fx_spot_quote().loc[0][2]
    return render_template('information.html',huilv=huilv)

@app.route('/zhifudaima', methods=['GET', 'POST'])
def result():
    return render_template('zhifudaima.html')
@app.route('/zhifudaima_detail/<zhifudaima_code>',methods=['GET', 'POST'])
def zhifudaima_detail(zhifudaima_code):
    #股票代码查找股票的详细信息
    zhifudaima_info = zhifu.zhifu_info(zhifudaima_code)
    return render_template('zhifudaima_detail.html', zhifudaima_info=zhifudaima_info)


if __name__ == '__main__':
    app.run(debug=True)



