# -*- coding: utf-8 -*-
import os
import time
import trial
from datetime import datetime
import auth
import banwords
from msg_id import *
import json
from tx_ocr import ocr
import botpy
from botpy import BotAPI

from botpy.ext.command_util import Commands
from botpy.message import Message
from botpy.user import Member
from botpy.forum import Thread
from botpy.types.forum import Post, Reply, AuditResult
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))


@Commands(name=("踢出", "移除", "/踢出", "/移除"))
async def remove_members(api: BotAPI, message: Message, params=None):
    if auth.is_bigger_than(message.member.roles, auth.role_list["金色传说"]) and params is not None:
        await message.reply(content=f"被@人的ID：{message.mentions[1].id}，已踢出")
        await api.get_delete_member(message.guild_id, message.mentions[1].id)
    else:
        await message.reply(content='【群管模块】权限不足！需拥有【金色传说】以上权限身份组！')
    return True


@Commands(name=("拉黑", "/拉黑"))
async def blacklist_members(api: BotAPI, message: Message, params=None):
    botpy.logger.info(params)
    # 第一种用reply发送消息
    if auth.is_bigger_than(message.member.roles, auth.role_list["管理员"]) and params is not None:
        await message.reply(content=f"被@人的ID：{message.mentions[1].id}，已拉黑并删除3天内消息")
        await api.get_delete_member(message.guild_id, message.mentions[1].id, True, 3)
    else:
        await message.reply(content='【群管模块】权限不足！需拥有【管理员】以上权限身份组！')
    return True


@Commands(name=("加白", "/加白"))
async def add_whitelist(api: BotAPI, message: Message, params=None):
    botpy.logger.info(params)
    user_id = ''
    if auth.is_bigger_than(message.member.roles, auth.role_list["管理员"]) and params is not None:
        if len(message.mentions) <= 1 and str(params).isdigit():
            user_id = str(params)
        elif len(message.mentions) >= 2:
            user_id = message.mentions[1].id
        else:
            await message.reply(content='【白名单模块】请填写用户ID！')
            return True
        await api.create_guild_role_member(
            guild_id=message.guild_id,
            role_id=auth.role_list['独树一帜'],
            user_id=user_id
        )
        botpy.logger.info('已添加白名单，已添加【独树一帜】身份组。')
        await message.reply(content='【白名单模块】已添加白名单，已添加【独树一帜】身份组。')
    else:
        await message.reply(content='【白名单模块】权限不足！需拥有【金色传说】以上权限身份组！')
    return True


@Commands(name=("删白", "/删白"))
async def del_whitelist(api: BotAPI, message: Message, params=None):
    # 第一种用reply发送消息
    if auth.is_bigger_than(message.member.roles, auth.role_list["管理员"]) and params is not None:
        if len(message.mentions) <= 1 and str(params).isdigit():
            user_id = str(params)
        elif len(message.mentions) >= 2:
            user_id = message.mentions[1].id
        else:
            await message.reply(content='【白名单模块】请填写用户ID！')
            return True
        await api.delete_guild_role_member(
            guild_id=message.guild_id,
            role_id=auth.role_list['独树一帜'],
            user_id=user_id
        )
        botpy.logger.info('【白名单模块】已删除白名单，已移除【独树一帜】身份组。')
        await message.reply(content='【白名单模块】已删除白名单，已移除【独树一帜】身份组。')
    else:
        await message.reply(content='【白名单模块】权限不足！需拥有【金色传说】以上权限身份组！')
    return True


@Commands(name=("/查信息", "查信息"))
async def get_user_info(api: BotAPI, message: Message, params=None):
    line = ''
    mb = None
    if auth.is_bigger_than(message.member.roles, auth.role_list["金色传说"]) and params is not None:  # 检查用户身份组，2为管理员，4为频道主
        botpy.logger.info("【查询模块】收到查信息指令")
        mb = await api.get_guild_member(guild_id=message.guild_id, user_id=message.mentions[1].id)
        line += f'【查询模块】为您查询<@!{message.mentions[1].id}>：\n'
        line += f'ID：{message.mentions[1].id}\n'
        line += f'用户名：{mb["user"]["username"]}\n'
        line += f'频内昵称：{mb["nick"]}\n'
        line += f'加入时间：{mb["joined_at"]}\n'
        line += f'是否在白名单：{str(auth.is_bigger_than(message.member.roles, auth.role_list["独树一帜"]))}\n'
        line += '头像：'
    else:
        line += "【查询模块】权限不足！需拥有【金色传说】以上权限身份组！"
    await message.reply(content=line, image=mb["user"]["avatar"] if mb is not None else None)
    return True


@Commands(name="测试")
async def test(api: BotAPI, message: Message, params=None):
    botpy.logger.info(message.guild_id)
    apis = await api.get_permissions(message.guild_id)
    x = 1
    return True


@Commands(name=("违禁词列表", "/违禁词列表", "查看违禁词", "/查看违禁词"))
async def query_wordlist(api: BotAPI, message: Message, params=None):
    ban_kind = ''
    page = 0
    if params != '':
        params_list = params.split(' ', 1)
        if len(params_list) == 1:
            if params.isdigit():
                ban_kind = '聊天'
                page = int(params_list[0]) - 1
            else:
                ban_kind = params_list[0]
                page = 0
        elif len(params_list) == 2:
            ban_kind = params_list[0]
            page = int(params_list[1]) - 1
        else:
            ban_kind = '聊天'
            page = 0
    else:
        ban_kind = '聊天'
        page = 0
    await message.reply(content=banwords.get_all_word_page(page, ban_kind, message.guild_id))
    return True


@Commands(name=("添加违禁词", "/添加违禁词"))
async def add_banword(api: BotAPI, message: Message, params=None):
    if auth.is_bigger_than(message.member.roles, auth.role_list["金色传说"]):
        params_list = params.split(' ', 1)
        if len(params_list) == 2:
            ban_kind = params_list[0]
            word = params_list[1]
            if ban_kind not in ['聊天', '昵称', '正则', '图片']:
                await message.reply(content=f"【违禁词模块】缺乏必要的参数\n命令格式：@机器人 添加违禁词 类型 违禁词")
                return True
            banwords.add_banword(word, ban_kind, message.guild_id)
            await message.reply(content=f"【违禁词添加成功】{ban_kind}违禁词：{word}")
        else:
            await message.reply(content=f"【违禁词模块】缺乏必要的参数\n命令格式：@机器人 添加违禁词 类型 违禁词")
    else:
        await message.reply(content=f"【违禁词模块】<@{message.author.id}>权限不足！")
    return True


@Commands(name=("删除违禁词", "/删除违禁词"))
async def del_banword(api: BotAPI, message: Message, params=None):
    if auth.is_bigger_than(message.member.roles, auth.role_list["金色传说"]):
        botpy.logger.info(f'【违禁词模块】删除违禁词')
        params_list = params.split(' ', 1)
        ban_kind = '聊天'
        num = 0
        if len(params_list) == 1:
            if params.isdigit():
                ban_kind = '聊天'
                num = int(params_list[0]) - 1
            else:
                ban_kind = params_list[0]
                num = 0
        elif len(params_list) == 2:
            ban_kind = params_list[0]
            num = int(params_list[1]) - 1
        banwords.del_banword(num, ban_kind, message.guild_id)
        await message.reply(content=f"【违禁词删除成功】{ban_kind}违禁词序号：{num+1}")
    else:
        await message.reply(content=f"【违禁词模块】<@{message.author.id}>权限不足！")
    return True


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        handlers = [
            remove_members,
            get_user_info,
            blacklist_members,
            query_wordlist,
            add_banword,
            del_banword,
            add_whitelist,
            del_whitelist,
            test
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return

    async def on_guild_member_add(self, member: Member):
        mb = await self.api.get_guild_member(guild_id=member.guild_id, user_id=member.user.id)
        botpy.logger.info(f'【进人模块】已检测到成员进入频道，ID：{member.user.id}，用户名：{mb["user"]["username"]}')
        line = ''
        line += f'【进人提醒】<@!{member.user.id}>：已加入频道\n'
        line += f'ID：{member.user.id}\n'
        line += f'用户名：{mb["user"]["username"]}\n'
        line += f'频内昵称：{mb["nick"]}\n'
        line += f'加入时间：{mb["joined_at"]}\n'
        line += '头像：'
        await self.api.post_message(channel_id="1681323", msg_id=get_msg_id(), content=line,
                                    image=mb["user"]["avatar"] if mb is not None else None)

    async def on_message_create(self, message: Message):
        # 注册指令handler
        ocr_result = ''
        url = ''
        ban_words = ''
        ocr_ban_words = ''

        botpy.logger.info(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t【私域消息】作者ID：{message.author.id}，子频道ID：{message.channel_id}，消息内容：{message.content if message.content is not None else '【图片消息】'}")
        set_msg_id(message.id)
        if message.content is not None and auth.is_bigger_than(message.member.roles, auth.role_list['金色传说']):
            if message.content[:2] == '%%' and message.content.lstrip('%%').isdigit():
                s = message.content.lstrip('%%')
                todolist = [False, False, False, False, False]
                user_id = trial.get_user()
                for i in s:
                    if 1 <= int(i) <= 4:
                        todolist[int(i)] = True
                if not any(todolist):
                    await message.reply(content=f"请正确输入指令！")
                    return
                for x in range(1, 5):
                    if todolist[x]:
                        if x == 1:
                            await self.api.get_delete_member(message.guild_id, user_id, False, 0)
                            botpy.logger.info(f"【群管模块】{user_id}：已执行踢出操作。")
                            await message.reply(content=f"用户ID：{user_id}\n已执行踢出操作。")
                        elif x == 2:
                            await self.api.get_delete_member(message.guild_id, user_id, True, 3)
                            botpy.logger.info(f"【群管模块】{user_id}：已执行拉黑操作，已撤回近3天内全部消息。")
                            await message.reply(content=f"用户ID：{user_id}\n已执行拉黑操作，已撤回近3天内全部消息。")
                        elif x == 3:
                            await self.api.mute_member(guild_id=message.guild_id, user_id=user_id,
                                                       mute_seconds="0")
                            botpy.logger.info(f"【群管模块】{user_id}：已解除禁言。")
                            await message.reply(content=f"用户ID：{user_id}\n已解除禁言。")
                        elif x == 4:
                            await self.api.create_guild_role_member(
                                guild_id=message.guild_id,
                                role_id=auth.role_list['独树一帜'],
                                user_id=user_id
                            )
                            botpy.logger.info(f"【群管模块】{user_id}：已添加白名单，已加入【独树一帜】身份组。")
                            await message.reply(content=f"用户ID：{user_id}\n已添加白名单，已加入【独树一帜】身份组。")
            return

        if not auth.is_bigger_than(message.member.roles, auth.role_list['独树一帜']):
            # 不属于白名单，执行违规检测
            # 开始文字违规检测
            if len(message.attachments) != 0:
                # 消息为纯图片
                for att in message.attachments:
                    url = 'https://' + att.url
                    ocr_result += ocr(url)
                    botpy.logger.info("文字识别结果" + ocr_result)
            if message.content is not None:
                ban_words = banwords.word_detector(message.content)
            if ocr_result != '':
                ocr_ban_words = banwords.pic_detector(ocr_result)
            if ban_words != '' or ocr_ban_words != '':
                botpy.logger.info("触发普通违禁词：" + ban_words)
                mb = await self.api.get_guild_member(guild_id=message.guild_id, user_id=message.author.id)
                msg = banwords.get_prohibit_tip(message, mb, ban_words if ban_words != '' else ocr_ban_words)
                # botpy.logger.info(msg)
                await self.api.recall_message(channel_id=message.channel_id, message_id=message.id, hidetip=True)
                await self.api.mute_member(guild_id=message.guild_id, user_id=message.author.id, mute_seconds="300")
                await self.api.post_message(channel_id="1598678", msg_id=message.id, content=msg, image=url if url != '' else None)
                trial.set_user(message.author.id)
                return

            re_words = banwords.re_detector(message.content)
            if re_words != '':
                botpy.logger.info("触发正则违禁词：" + re_words)
                mb = await self.api.get_guild_member(guild_id=message.guild_id, user_id=message.author.id)
                await self.api.recall_message(channel_id=message.channel_id, message_id=message.id, hidetip=True)
                await self.api.mute_member(guild_id=message.guild_id, user_id=message.author.id, mute_seconds="300")
                msg = banwords.get_prohibit_tip(message, mb, ban_words)
                await self.api.post_message(channel_id="1598678", msg_id=message.id, content=msg)
                trial.set_user(message.author.id)
                return
        else:
            botpy.logger.info("权限大于独树一帜，不执行违规检测")

    # TODO 咔哒美好和萌宠记录员添加
    async def on_forum_thread_create(self, thread: Thread):
        """
        论坛主题发布
        """
        mb = await self.api.get_guild_member(guild_id=thread.guild_id,user_id=thread.author_id)
        content = ""
        title = thread.thread_info.title.paragraphs[0].elems[0].text.text
        content_json = thread.thread_info.content.paragraphs
        botpy.logger.info(f"【收到帖子】频道ID：{thread.guild_id}，子频道ID：{thread.channel_id}，标题：{title}，内容：{content}")
        if auth.is_bigger_than(mb['roles'], auth.role_list['独树一帜']):
            botpy.logger.info("【违禁词检测】已在白名单，不检测违禁词。")
            return
        for k in content_json:
            content += k.elems[0].text.text

        ban_words = banwords.word_detector(title)
        if ban_words != '':
            botpy.logger.info("帖子标题触发违禁词：" + ban_words)
        else:
            ban_words = banwords.word_detector(content)
            if ban_words != '':
                botpy.logger.info("帖子内容触发违禁词：" + ban_words)
            else:
                return

        msg = banwords.get_thread_prohibit_tip(thread, title, content, mb, ban_words)
        await self.api.delete_thread(channel_id=thread.channel_id, thread_id=thread.thread_info.thread_id)
        await self.api.mute_member(guild_id=thread.guild_id, user_id=thread.author_id, mute_seconds="300")
        await self.api.post_message(channel_id="1598678", msg_id=get_msg_id(), content=msg)
        trial.set_user(thread.author_id)
        return

    async def on_forum_thread_update(self, thread: Thread):
        """
        此处为处理该事件的代码
        """

    async def on_forum_post_create(self, post: Post):
        content = json.loads(post['post_info']['content'])['paragraphs'][0]['elems'][0]['text']['text']
        botpy.logger.info(f"【收到帖子回复】子频道ID：{post['channel_id']}，作者ID：{post['author_id']}，回复内容：{content}")
        # mb = await self.api.get_guild_member(guild_id=post['guild_id'], user_id=post['author_id'])
        # if auth.is_bigger_than(mb['roles'], auth.role_list['独树一帜']):
        #     botpy.logger.info("【违禁词检测】已在白名单，不检测违禁词。")
        #     return
        # ban_words = banwords.word_detector(content)
        # if ban_words == '':
        #     return
        # else:
        #     msg = banwords.get_prohibit_tip(post, mb, ban_words)
        #     # del post
        #     return

    async def on_forum_reply_create(self, reply: Reply):
        """
        此处为处理该事件的代码
        """

    async def on_forum_thread_delete(self, thread: Thread):
        """
        此处为处理该事件的代码
        """


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True, guild_messages=True, direct_message=True, guild_members=True,
                            forums=True)
    client = MyClient(intents=intents, is_sandbox=False)
    client.run(appid=test_config["appid"], token=test_config["token"])
