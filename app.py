import openai
import os
import gradio as gr
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정 (환경 변수에서 가져오기)
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

# ChatGPT API 호출 함수
def generate_script_with_gpt(grade, num_people, duration, key_phrases, key_words):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a skilled playwright specializing in role-playing scripts as a teacher. You excel at writing scripts with easy words, especially for elementary school students. You can write engaging role-play scripts using educationally appropriate words and situations that help students learn key expressions in a fun way."},
            {"role": "user", "content": f"Create a role-play script for grade {grade} Korean elementary school students. The script should play for {duration} seconds. Include {num_people} balanced roles in the script. Key phrases: {key_phrases}. Key words: {key_words}. The format of the script is 'name:line' and provide Korean translation in the next line."}
        ]
    )

    script = response['choices'][0]['message']['content']
    return script
# Gradio 인터페이스에서 호출할 함수
def generate_script(grade, num_people, duration, key_phrases, key_words):
    script = generate_script_with_gpt(grade, num_people, duration, key_phrases, key_words)
    return script

def download_audio(script):
    from gtts import gTTS
    tts = gTTS(script, lang='ko')
    audio_file_path = "script_audio.mp3"
    tts.save(audio_file_path)
    return audio_file_path

def download_script(script):
    script_file_path = "script.txt"
    with open(script_file_path, "w", encoding="utf-8") as file:
        file.write(script)
    return script_file_path

# Gradio 인터페이스 생성
with gr.Blocks() as demo:
    with gr.Row():
        grade_dropdown = gr.Dropdown(choices=["1", "2", "3", "4", "5", "6"], label="학년")
        num_people_slider = gr.Slider(minimum=2, maximum=10, value=4, step=1, label="상황극 인원")
        duration_slider = gr.Slider(minimum=30, maximum=300, value=30, step=1, label="길이(초)")
    key_phrases_input = gr.Textbox(label="주요 표현 입력")
    with gr.Row():
        key_words_input = gr.Textbox(label="주요 단어 입력", lines=5)
        script_output = gr.Textbox(label="상황극 대본", lines=20)
    with gr.Row():
        audio_download_button = gr.Button("음성파일 다운로드")
        script_download_button = gr.Button("대본 다운로드")

    generate_button = gr.Button("상황극 대본 생성")

    generate_button.click(fn=generate_script,
                          inputs=[grade_dropdown, num_people_slider, duration_slider, key_phrases_input, key_words_input],
                          outputs=script_output)
    audio_download_button.click(fn=download_audio, inputs=script_output, outputs=[])
    script_download_button.click(fn=download_script, inputs=script_output, outputs=[])

# Gradio 앱 실행
demo.launch()
