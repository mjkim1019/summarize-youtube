import os
from openai import OpenAI

from transcript import *

#url = 'https://www.youtube.com/watch?v=1SizhsIcqEY'
#url = 'https://www.youtube.com/watch?v=2TL3DgIMY1g'
#url = 'https://www.youtube.com/watch?v=TSX47s0Eet0'
#url = 'https://youtube.com/shorts/6RlW4zfZLlQ?si=iJICXuMuBjm5Kd1r'
#url = 'https://www.youtube.com/watch?v=cwf_pVRq1P4'
#url = 'https://youtube.com/shorts/8-Cw-oHaG7k?si=1u9crixRPP8xYRNs'

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def summarize_youtube_video(captions):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {'role': 'system', 'content': '당신은 전문적인 요약을 제공하는 어시스턴트입니다.'},
            {'role': 'assistant', 'content': 'Summarize in Korean in 200 characters of this video.'},
            {'role': 'user', 'content': captions}
        ],
        max_tokens=200,
    )
    summary = response.choices[0].message.content

    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {'role': 'system', 'content': '당신은 전문적인 요약을 제공하는 어시스턴트입니다.'},
            {'role': 'assistant', 'content': "output a list of three tags for this blog post "
                                             "in a list such as ['item1', 'item2', 'item3']"},
            {'role': 'user', 'content': captions}
        ]
    )
    tags = response.choices[0].message.content

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {'role': 'system', 'content': '당신은 전문적인 요약을 제공하는 어시스턴트입니다.'},
            {'role': 'assistant', 'content': "다음과 같은 category [" +
                                             "기술, 부동산, 꿀팁, 자취, 돈, 공부, 취미, 영화&드라마, 책, 갓생" +
                                             "] 중에 어디 소속으로 들어가면 좋을지, 가장 가까운 거 1개 선택해서 출력해줘. 적합한 category가 없으면 새로 생성해줘." +
                                             "list 형태로 예를 들어 ['category'] 이렇게 출력해줘."
             },
            {'role': 'user', 'content': captions}
        ]
    )
    category = response.choices[0].message.content

    print('>>>SUMMARY:')
    print(summary)
    print('>>>TAGS:')
    print(tags)
    print('>>>CATEGORY:')
    print(category)



def summarize_youtube_video2(output):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {'role': 'system', 'content': '당신은 전문적인 요약을 제공하는 어시스턴트입니다.'},
            {'role': 'assistant', 'content': "다음 content로 보내지는 텍스트를 읽고 다음 요구사항을 들어줘.\n" +
                    "\t1\t텍스트를 summarize하여 “summary”를 한 문장으로 생성하여 “summary” 부분에 100자로 출력해줘.\n" +
                    "\t2\t텍스트의 제목을 추출해서 “subject” 부분에 출력해줘.\n" +
                    "\t3\t블로그 포스트에 쓰일 알맞는 keyword(tag)를 명사형으로 3개 추출해서 “keyword” 부분에 출력해줘.\n" +
                    "\t4\t텍스트에 어울리는 category를 [" + "기술, 부동산, 꿀팁, 자취, 돈, 공부, 취미, 영화&드라마, 책, 갓생" + "] 중에 3개 선택해서 “category” : 부분에 출력해줘. 어울리는 category가 없다고 판단되면 새로 생성해줘.\n" +
                    "\t5\t출력 형식은 다음과 같이 json 형식으로 출력해줘. { } 안의 내용만 출력해줘. json 형식을 제외한 텍스트는 한 글자도 출력하지 않는다. 추가 설명, 주의사항 등 일절 작성하지 마. 제발 지켜줘\n" +
                    "{\n" +
                    "\t“subject” : “주제”,\n" 
                    "\t“summary” : “요약한 내용”,\n" +
                    "\t“keyword” : [“키워드1”, “키워드2”, “키워드3”],\n" +
                    "\t“category” : [\"카테고리1\", \"카테고리2\", \"카테고리3\"]\n" +
                    "}\n"},
            {'role': 'user', 'content': output}
        ]
    )
    summaryJson = response.choices[0].message.content

    print('>>>SUMMARY JSON:')
    print(summaryJson)

def main():
    url = 'https://www.youtube.com/watch?v=1SizhsIcqEY'

    # 사용자가 동영상 ID를 입력
    video_url = input("Enter the YouTube video URL: ")
    video_id = extract_video_id(video_url)

    # 동영상 정보 가져오기
    video_info = get_video_info(video_id)
    if video_info:
        print("Title:", video_info["title"])
        print("Channel:", video_info["channel_title"])
        print("Thumbnail URL:", video_info["thumbnail"])
        print("View Count:", video_info["view_count"])
    else:
        print("Could not retrieve video information.")

    # 자막 가져오기
    captions = get_video_captions(video_id)
    #print("Captions:", captions)

    # 요약하기
    summarize_youtube_video(captions)

    summarize_youtube_video2(captions)

# 프로그램의 시작점
if __name__ == "__main__":
    main()

