import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


letter_dict = {
    1: 'a',
    2: 'b',
    3: 'c',
    4: 'd',
    5: 'e',
    6: 'f',
    7: 'g',
    8: 'h',
    9: 'i',
    10: 'j',
    11: 'k',
    12: 'l',
    13: 'm',
    14: 'n',
    15: 'o',
    16: 'p',
    17: 'q',
    18: 'r',
    19: 's', 
    20: 't',
    21: 'u',
    22: 'v',
    23: 'w', 
    24: 'x',
    25: 'y',
    26: 'z'
}
words = ['HELLO',
         'WORLD',
         'PYTHON',
         'CODE',
         '1234',
         'OPENAI',
         'MORSE',
         'QUIZ',
         'GAME',
         '2024']
morse_code_dict = {
    'A': '.-',
    'B': '-…',
    'C': '-.-.',
    'D': '-..', 
    'E': '.',
    'F': '..-.',
    'G': '–-.', 
    'H': '….',
    'I': '..',
    'J': '.–--',
    'K': '-.-',
    'L': '.-..',
    'M': '–-',
    'N': '-.',
    'O': '–--', 
    'P': '.–-.',
    'Q': '-–.-',
    'R': '.-.',
    'S': '…',
    'T': '-',
    'U': '..-',
    'V': '…-',
    'W': '.–-',
    'X': '-..-',
    'Y': '-.–-',
    'Z': '-–..',
    '0': '-----',
    '1': '.––--',
    '2': '..–--',
    '3': '…–-', 
    '4': '….-',
    '5': '…..',
    '6': '-….',
    '7': '–-…',
    '8': '–--..',
    '9': '––--.'
}


#############################################################
async def show_morse_code_table(message):
    morse_table = "摩斯密碼對照表:\n"
    for i, (char, morse) in enumerate(morse_code_dict.items()):
        morse_table += f"{char}: {morse} "
        if (i + 1) % 5 == 0:
            morse_table += "\n"
    await message.channel.send(morse_table)
##############################################
async def show_intro_message(message,level):
    await message.channel.send(f"\n歡迎來到關卡 {level}！")
    await message.channel.send("在這個關卡中，你將挑戰自我，完成以下題目。祝你好運！")
    await message.channel.send("傳送任意字母 開始…")
    await bot.wait_for('message')
###############################################################
async def morse_choice_quiz(message):
    await show_intro_message(message, 1)
    await show_morse_code_table(message)  # 顯示摩斯密碼對照表

    questions = [
        {"question": "...", "options": ["A: E", "B: S", "C: I", "D: H"], "answer": "B"},
        {"question": "-.-.", "options": ["A: A", "B: C", "C: K", "D: B"], "answer": "B"},
        {"question": ".--", "options": ["A: R", "B: T", "C: W", "D: J"], "answer": "C"},
        {"question": "-..", "options": ["A: D", "B: G", "C: V", "D: N"], "answer": "A"},
        {"question": ".---", "options": ["A: P", "B: J", "C: Q", "D: I"], "answer": "B"}
    ]

    score = 0

    for q in questions:
        await message.channel.send(f"\n請解碼摩斯密碼: {q['question']}")
        for option in q['options']:
            await message.channel.send(option)

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            user_answer_msg = await bot.wait_for('message', timeout=30.0, check=check)
            user_answer = user_answer_msg.content.strip().upper()

            if user_answer == q['answer']:
                await message.channel.send("答對了！")
                score += 1
            else:
                await message.channel.send(f"答錯了！正確答案是: {q['answer']}")
        except asyncio.TimeoutError:
            await message.channel.send("你没有在規定時間内回答，跳過這題。")

    await message.channel.send(f"\n摩斯密碼選擇題結束！你的總得分是: {score}/{len(questions)}")
    return score
###################################################
async def multiple_choice_quiz(message):
    await show_intro_message(message, 2)

    questions = [
        {"question": "第一題: 三杯雞裡面的三杯不包含下列哪寫調味料",
        "options":  ["A: 麻油", "B: 烏醋", "C: 醬油", "D: 米酒"], "answer": "B"},
        {"question": "第二題: 在比賽時 超越第二名會變成第幾名",
        "options": ["A: 第二名", "B: 最後一名", "C: 第三名", "D: 第一名"], "answer": "A"},
        {"question": "第三題: 過山刀是哪一種",
        "options": ["A: 刀", "B: 植物", "C: 食物", "D: 蛇"], "answer": "D"},
        {"question": "第四題: 小說哈利波特中，以下哪個選項不是其中一個學院的名稱",
        "options": ["A: 雷文克勞", "B: 鄧不利多", "C: 葛來分多", "D: 史萊哲林"], "answer": "B"},
        {"question": "第五題: 義大利在地圖上看起來像?",
        "options": ["A: 番薯", "B: 長靴", "C: 秋海棠", "D: 鑽石"], "answer": "B"}
    ]

    score = 0

    for q in questions:
        await message.channel.send(f"\n{q['question']}")
        for option in q['options']:
            await message.channel.send(option)
        
        # 定义过滤器来检查输入是否有效
        def check(m):
            return m.author == message.author and m.channel == message.channel and m.content.upper() in ['A', 'B', 'C', 'D']
        
        try:
            user_answer = await bot.wait_for('message', check=check)
            if user_answer.content.upper() == q['answer']:
                await message.channel.send("答對了！")
                score += 1
            else:
                await message.channel.send(f"答錯了！正確答案是: {q['answer']}")
        
        except asyncio.TimeoutError:
            await message.channel.send("你没有在規定時間內回應，該題算錯誤！")

    await message.channel.send(f"\n選擇題結束！你的總得分是: {score}/{len(questions)}")
    return score
#######################################
async def morse_quiz_game(message):
    await show_intro_message(message,3)
    await show_morse_code_table(message) # 顯示摩斯密碼對照表
    score = 0
    total_questions = 5
    selected_words = random.sample(words, total_questions)
    def check(m):
        return m.author == message.author and m.channel == message.channel
    for i, word in enumerate(selected_words):
        await message.channel.send(f"\n第 {i + 1} 題: '{word}'")
        await message.channel.send("提示: 打完一個字母或數字的摩斯密碼後需要空一格再繼續輸入。")
    
        user_input = await bot.wait_for('message', check=check)
        user_input1 = user_input.content.strip()
        correct_answer = ' '.join(morse_code_dict[char] for char in word)
    
        if user_input1.lower().replace(" ","") == correct_answer.lower().replace(" ",""):
            await message.channel.send("恭喜你，答對了！")
            score += 1
        else:
            await message.channel.send(f"很遺憾，正確答案是: {correct_answer}")

    await message.channel.send(f"\n摩斯密碼解碼遊戲結束！你的總得分是: {score}/{total_questions}")
    return score
##############################################
# 轉字母
def number_to_letter(num):
    return letter_dict.get(num)
############################################
async def send_totalscore(message):
    total_score = morse_choice_score + multiple_choice_score + morse_quiz_score
    await message.channel.send(f"\n遊戲結束！你的總得分是: {total_score}/15")

#################################################
async def ultimate_challenge(message):
    # chose a random answer
    answer = random.randint(1, 26)
    answer_letter = number_to_letter(answer)

    await message.channel.send("小試身手:终級字母!\n玩法就是將終極密碼的數字换成A~Z的字母!")
    await message.channel.send("請輸入字母:")

    # 檢查用戶的輸入(chat gpt)
    def check(m):
        return m.author == message.author and m.channel == message.channel
    while True:
        try:
            user_input = await bot.wait_for('message', timeout=30.0, check=check)
            user_letter = user_input.content.lower()

            if user_letter in letter_dict.values():
                user_answer = list(letter_dict.keys())[list(letter_dict.values()).index(user_letter)]

                if user_answer > answer:
                    await message.channel.send("輸入的字母的數字值大於终級字母的數字值!")
                elif user_answer < answer:
                    await message.channel.send("輸入的字母的數字值小於终級字母的數字值")
                else:
                    await message.channel.send(f"恭喜你! 你輸入的字母 {user_letter} 是正确的!")
                    break
            else:
                await message.channel.send("輸入的字母無效!")

        except asyncio.TimeoutError:
            await message.channel.send("你没有在規定時間内輸入字母，挑戰失败!")
            break
    await message.channel.send("恭喜你完成了終極字母挑戰！接下來是摩斯密碼選擇題。")
    morse_choice_score = await morse_choice_quiz(message)
    
    await message.channel.send("接下來是一般選擇題。")
    multiple_choice_score = await multiple_choice_quiz(message)
    
    await message.channel.send("最後是摩斯密碼測驗。")
    morse_quiz_score = await morse_quiz_game(message)
    
    # 計算總分
    total_score = morse_choice_score + multiple_choice_score + morse_quiz_score
    await message.channel.send(f"\n所有挑戰結束！你的總得分是: {total_score}/15")
    await message.channel.send("在漫長的人生旅途上,當你感到無聊時,不妨來找我抒發時間吧!")
    await message.channel.send("重新喚起我只需要輸入Hello喔!")


####################################
#成功登錄時回傳TERMINAL
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
#############################
# 處理消息
@bot.event
async def on_message(message):
    #忽略機器人自己發送的訊息
    if message.author == bot.user:
        return

    if message.content.lower() == 'hello':
        await message.channel.send('歡迎来到挑戰者園地!\n您是否接受挑戰呢?')

        # waiting for reply
        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            response = await bot.wait_for('message', timeout=30.0, check=check)
            if response.content.lower() in ["yes", "是"]:
                await ultimate_challenge(message)
            else:
                await message.channel.send("不是哥們?\n你搞我啊?")
        except asyncio.TimeoutError:
            await message.channel.send("你没有在規定時間內回應，挑戰取消!")


    await bot.process_commands(message)
# DcBOT TOKEN:
bot.run('')#yourdcbot token
