# GPT2 everytime

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/fpem123/GPT2-FairyTales)

This project generate everytime community style korean text using GPT-2 model.

Origin notebook: [Colab](https://colab.research.google.com/drive/1p6DIxsesi3eJNPwFwvMw0MeM5LkSGoPW?usp=sharing&fbclid=IwAR1kejoqnhL738Za3M_BsGnjjJrayGq5AG3hH8UUBX3dRwCK6JvT4loZ88A#scrollTo=fJWeAhLF7rdh)

### How to use

    * First, Fill what the character will say in text. This will be base of script.
    * Second, Choose text style category.
    * And then, Fill number in length. Text is created as long as "length". I recommend between 100 and 300.
    * If length is so big, generate time will be long.

### Post parameter

    text: The base of generated text.
    category: The text style category.
    length: The size of generated text.


### Output format

    {"0": generated text}


## * With CLI *

### Input example

    curl -X POST "https://master-gpt2-everytime-fpem123.endpoint.ainize.ai/everytime" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=님들 오늘 수업" -F "category=대학생 잡담방" -F "length=100"

### Output example


    {
      "0": "<unused4> 님들 오늘 수업끝나고 수업시간에 뭐하나요? ᄉᄇ<unused2>어제 전공공부 다  ⁇ 끝나서 늦게까지 남아서 하고 나왔는데<unused2>아  ⁇
            끝나갈시간이네 다들 과제끝났다  ⁇  얘두라 저번에 술취한 애한테 카톡보냈는데 답장이 없네? 나랑 대화 가능? 이거 뭐냐 이 미친새끼...  ⁇  
            와 진짜 자살생각하구 이 시간에 전화해서 내가 전화"
    }


## * With swagger *

API page: [Ainize](https://ainize.ai/fpem123/gpt2-everytime?branch=master)

## * With a Demo *

Demo page: [End-point](https://master-gpt2-everytime-fpem123.endpoint.ainize.ai/)