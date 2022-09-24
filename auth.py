"""
创建者 4
超管 10683655
管理员 2
二级管理员 10798081
怒频管理员 10798202
认证沃沃头 10069519

长颈鹿之橙 10037377
鞋垫之紫 10037350
蜘蛛之紫 10037398
鲨鱼之蓝 10037392
忆雨之绿 10037346
认证沃沃头 10069519
"""
# 是否创建者、是否管理员、是否其他管理员、管理员权限比大小、普通成员权限比大小
role_list = {
    "创建者": '4',
    "管理员": '2',
    "金色传说": '10032972',
    "社团/学生会骨干": '11338290',
    "朝乾夕惕": '10485863',
    # 普通成员
    "登峰造极": '10485862',
    "萌宠记录员": '10495678',
    "咔哒美好": '10495679',
    "自律先锋": '10180313',
    "独树一帜": '10038677',
    "一路有你": '11342346',
    "麦庐园校区": '10178262',
    "蛟桥园校区": '10178261',
    "枫林园校区": '11997463',
    "我是新生": '10869892',
    "酱菜元老": '10038591',
    "机器人": '12011376'
}
auth_list = {
    role_list["创建者"]: 11,
    role_list["管理员"]: 10,
    role_list["金色传说"]: 9,
    role_list["社团/学生会骨干"]: 8,
    role_list["朝乾夕惕"]: 8,
    # 普通成员
    role_list["登峰造极"]: 7,
    role_list["萌宠记录员"]: 6,
    role_list["咔哒美好"]: 5,
    role_list["自律先锋"]: 4,
    role_list["独树一帜"]: 3,
    role_list["一路有你"]: 2,
    role_list["麦庐园校区"]: 2,
    role_list["蛟桥园校区"]: 2,
    role_list["枫林园校区"]: 2,
    role_list["我是新生"]: 2,
    role_list["酱菜元老"]: 2,
    role_list["一路有你"]: 2,
    role_list["机器人"]: 2
}


# 获取用户最高权限对应的身份组序号
def get_highest_auth_role(roles_list):
    top_role = 0
    for role in roles_list:
        if role not in auth_list:
            continue
        if auth_list[role] >= auth_list[top_role]:
            top_role = role
    return top_role


# 获取用户最高权限对应的权限级别
def get_highest_auth_level(roles_list):
    top_auth = 0
    for role in roles_list:
        if role not in auth_list:
            continue
        if auth_list[role] >= top_auth:
            top_auth = auth_list[role]
    return top_auth


def is_creator(roles_list):
    return True if '4' in roles_list else False


def is_admin(roles_list):
    return True if '4' in roles_list or '2' in roles_list else False


# def is_other_admin(roles_list: list):
#     return True if 7 <= get_highest_auth_level(roles_list) <= 11 else False


def is_bigger_than(roles_list, base):  # 身份组列表与基准权限身份组，base填身份组号码
    base_auth = auth_list[base]
    for role in set(roles_list).intersection(set(auth_list.keys())):
        if auth_list[role] >= base_auth:
            return True  # 大于等于base
    return False  # 小于base
