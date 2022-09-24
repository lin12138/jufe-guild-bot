from botpy.message import Message
from botpy.forum import Thread
from botpy.types.forum import Post, Reply
from math import ceil
import re
def get_thread_prohibit_tip(thread: Thread, title, content, mb, ban_word):
    s = f"""【帖子违规】
触发人频道内昵称：{mb["nick"]} 
触发人用户昵称：{mb["user"]["username"]}
触发人频道ID：{thread.author_id}
触发人加入时间：{mb["joined_at"]}
违禁词所在子频道：<#{thread.channel_id}>
触发违禁词：{ban_word}
【帖子标题】{title}
【帖子内容如下】
{content}
————————
如需踢出请发送：%%1
如需拉黑请发送：%%2
如需解除禁言请发送：%%3
如需加白名单请发送：%%4
指令数字可以排列组合，如发送%%34即为解除禁言+加白"""
    return s

def get_post_prohibit_tip(post: Post, mb, ban_word):
    s = f"""【帖子回复违规】
触发人频道内昵称：{mb["nick"]} 
触发人用户昵称：{mb["user"]["username"]}
触发人频道ID：{post['author_id']}
触发人加入时间：{mb["joined_at"]}
违禁词所在子频道：<#{post['channel_id']}>
触发违禁词：{ban_word}
【消息原文如下】
{post['post_info']['content']}
————————
如需踢出请发送：%%1
如需拉黑请发送：%%2
如需解除禁言请发送：%%3
如需加白名单请发送：%%4
指令数字可以排列组合，如发送%%34即为解除禁言+加白"""
    return s

def get_prohibit_tip(message: Message, mb, ban_word):
    s = f"""【发言违规】
触发人频道内昵称：{mb["nick"]} 
触发人用户昵称：{mb["user"]["username"]}
触发人频道ID：{message.author.id}
触发人加入时间：{mb["joined_at"]}
违禁词所在子频道：<#{message.channel_id}>
触发违禁词：{ban_word}
【消息原文如下】
{message.content}
————————
如需踢出请发送：%%1
如需拉黑请发送：%%2
如需解除禁言请发送：%%3
如需加白名单请发送：%%4
指令数字可以排列组合，如发送%%34即为解除禁言+加白"""
    return s

def re_detector(content: str, guild_id="17019816109928716791"):
    black_word = ''
    with open(f"./data/{guild_id}/正则违禁词列表.txt", 'r', encoding='utf-8') as f:
        txt = f.read()
        words_list = txt.split('|')
        for word in words_list:
            if word != '':
                result = re.match(word, content, re.I)
                if result:
                    black_word = result.re.pattern
                    break
        return black_word

def word_detector(content: str, guild_id="17019816109928716791"):
    black_word = ''
    with open(f"./data/{guild_id}/聊天违禁词列表.txt", 'r', encoding='utf-8') as f:
        txt = f.read()
        words_list = txt.split('|')
        for word in words_list:
            if word in content and word != '':
                black_word = word
        return black_word

def pic_detector(content: str, guild_id="17019816109928716791"):
    black_word = ''
    with open(f"./data/{guild_id}/图片违禁词列表.txt", 'r', encoding='utf-8') as f:
        txt = f.read()
        words_list = txt.split('|')
        for word in words_list:
            if word in content and word != '':
                black_word = word
        return black_word

def get_all_word_page(page: int = 0, kind: str = "聊天", guild_id="17019816109928716791"):  # 页码和查询类型
    numOfEachPage = 10  # 设置每页多少个梗
    with open(f"./data/{guild_id}/{kind}违禁词列表.txt", 'r', encoding='utf-8') as f:
        txt = f.read()
        allList = txt.split('|')[:-1]
        keysList = allList[numOfEachPage * page:numOfEachPage * (page + 1)]
        strToReturn = f"为您查询全部{kind}违禁词，第{page + 1}/{ceil(len(allList) / numOfEachPage)}页\n请发送【@机器人 /删除违禁词 {kind} 序号】删除违禁词\n——————————\n"
        baseJokeNum = numOfEachPage * page  # 每页第一个梗的序号
        for i in range(len(keysList)):
            strToReturn += f"{baseJokeNum + i + 1}、{keysList[i]}\n"  # 添加到待返回文本中
        return strToReturn.rstrip()

def add_banword(word: str, kind: str = "聊天", guild_id="17019816109928716791"):
    with open(f"./data/{guild_id}/{kind}违禁词列表.txt", 'a', encoding='utf-8') as f:
        f.write(word+"|")
        return

def del_banword(num, kind: str = "聊天", guild_id="17019816109928716791"):
    all_word = ''
    with open(f"./data/{guild_id}/{kind}违禁词列表.txt", 'r', encoding='utf-8') as f:
        all_word = f.read()
        f.close()
    word_list = all_word.split('|')[:-1]
    word_list.pop(int(num))
    new_list = ''
    for word in word_list:
        new_list += word + '|'
    with open(f"./data/{guild_id}/{kind}违禁词列表.txt", 'w', encoding='utf-8') as f:
        f.write(new_list)
        f.close()