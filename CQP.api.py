import ctypes
import struct
import base64
from html import escape, unescape

import CQP
from core.utils import *

CQDll = ctypes.WinDLL('CQP.dll')

'''
#表情_惊讶			"0"
#表情_撇嘴			"1"
#表情_色			"2"
#表情_发呆			"3"
#表情_得意			"4"
#表情_流泪			"5"
#表情_害羞			"6"
#表情_闭嘴			"7"
#表情_睡			"8"
#表情_大哭			"9"
#表情_尴尬			"10"
#表情_发怒			"11"
#表情_调皮			"12"
#表情_呲牙			"13"
#表情_微笑			"14"
#表情_难过			"15"
#表情_酷			"16"
#表情_抓狂			"18"
#表情_吐			"19"
#表情_偷笑			"20"
#表情_可爱			"21"
#表情_白眼			"22"
#表情_傲慢			"23"
#表情_饥饿			"24"
#表情_困			"25"
#表情_惊恐			"26"
#表情_流汗			"27"
#表情_憨笑			"28"
#表情_大兵			"29"
#表情_奋斗			"30"
#表情_咒骂			"31"
#表情_疑问			"32"
#表情_晕			"34"
#表情_折磨			"35"
#表情_衰			"36"
#表情_骷髅			"37"
#表情_敲打			"38"
#表情_再见			"39"
#表情_发抖			"41"
#表情_爱情			"42"
#表情_跳跳			"43"
#表情_猪头			"46"
#表情_拥抱			"49"
#表情_蛋糕			"53"
#表情_闪电			"54"
#表情_炸弹			"55"
#表情_刀			"56"
#表情_足球			"57"
#表情_便便			"59"
#表情_咖啡			"60"
#表情_饭			"61"
#表情_玫瑰			"63"
#表情_凋谢			"64"
#表情_爱心			"66"
#表情_心碎			"67"
#表情_礼物			"69"
#表情_太阳			"74"
#表情_月亮			"75"
#表情_强			"76"
#表情_弱			"77"
#表情_握手			"78"
#表情_胜利			"79"
#表情_飞吻			"85"
#表情_怄火			"86"
#表情_西瓜			"89"
#表情_冷汗			"96"
#表情_擦汗			"97"
#表情_抠鼻			"98"
#表情_鼓掌			"99"
#表情_糗大了		"100"
#表情_坏笑			"101"
#表情_左哼哼		"102"
#表情_右哼哼		"103"
#表情_哈欠			"104"
#表情_鄙视			"105"
#表情_委屈			"106"
#表情_快哭了		"107"
#表情_阴险			"108"
#表情_亲亲			"109"
#表情_吓			"110"
#表情_可怜			"111"
#表情_菜刀			"112"
#表情_啤酒			"113"
#表情_篮球			"114"
#表情_乒乓			"115"
#表情_示爱			"116"
#表情_瓢虫			"117"
#表情_抱拳			"118"
#表情_勾引			"119"
#表情_拳头			"120"
#表情_差劲			"121"
#表情_爱你			"122"
#表情_不			"123"
#表情_好			"124"
#表情_转圈			"125"
#表情_磕头			"126"
#表情_回头			"127"
#表情_跳绳			"128"
#表情_挥手			"129"
#表情_激动			"130"
#表情_街舞			"131"
#表情_献吻			"132"
#表情_左太极		"133"
#表情_右太极		"134"
#表情_双喜			"136"
#表情_鞭炮			"137"
#表情_灯笼			"138"
#表情_发财			"139"
#表情_K歌			"140"
#表情_购物			"141"
#表情_邮件			"142"
#表情_帅			"143"
#表情_喝彩			"144"
#表情_祈祷			"145"
#表情_爆筋			"146"
#表情_棒棒糖		 "147"
#表情_喝奶			"148"
#表情_下面			"149"
#表情_香蕉			"150"
#表情_飞机			"151"
#表情_开车			"152"
#表情_高铁左车头	 "153"
#表情_车厢			"154"
#表情_高铁右车头	 "155"
#表情_多云			"156"
#表情_下雨			"157"
#表情_钞票			"158"
#表情_熊猫			"159"
#表情_灯泡			"160"
#表情_风车			"161"
#表情_闹钟			"162"
#表情_打伞			"163"
#表情_彩球			"164"
#表情_钻戒			"165"
#表情_沙发			"166"
#表情_纸巾			"167"
#表情_药			"168"
#表情_手枪			"169"
#表情_青蛙			"170"
'''

# 认证码
CQP.AC = -1
# 事件回调启用禁止
CQP.enable = False
# 事件_忽略
CQP.EVENT_IGNORE = 0
# 事件_拦截
CQP.EVENT_BLOCK = 1
# 请求_通过
CQP.REQUEST_ALLOW = 1
# 请求_拒绝
CQP.REQUEST_DENY = 2
# 请求_群添加
CQP.REQUEST_GROUPADD = 1
# 请求_群邀请
CQP.REQUEST_GROUPINVITE = 2
# 调试 灰色
CQP.CQLOG_DEBUG = 0
# 信息 黑色
CQP.CQLOG_INFO = 10
# 信息(成功) 紫色
CQP.CQLOG_INFOSUCCESS = 11
# 信息(接收) 蓝色
CQP.CQLOG_INFORECV = 12
# 信息(发送) 绿色
CQP.CQLOG_INFOSEND = 13
# 警告 橙色
CQP.CQLOG_WARNING = 20
# 错误 红色
CQP.CQLOG_ERROR = 30

# 提示框退出酷Q，致命错误 深红
CQP.CQLOG_FATAL = 40


def cq_face(faceId):
    ''' #表情_* 开头常量 '''
    return '[CQ:face,id={}]'.format(faceId)


def cq_emoji(emoji):
    ''' emoji的unicode编号 '''
    return '[CQ:emoji,id={}]'.format(emoji)


def cq_at(QQID=-1, space=False):
    '''
    @某人(at)
        QQID: -1 为全体
    '''
    return '[CQ:at,qq={}]{}'.format(QQID if QQID != -1 else 'all', ' ' if space else '')


def cq_shake():
    ''' 窗口抖动(shake) - 仅支持好友 '''
    return '[CQ:shake]'


def cq_music(musicId, webType='qq', style=''):
    '''
    发送音乐(music)
        musicId     音乐的歌曲数字ID
        webType     目前支持 qq/QQ音乐 163/网易云音乐 xiami/虾米音乐，默认为qq
        style       指定分享样式
    '''
    return '[CQ:music,id={},type={},style={}]'.format(musicId, escape(webType), style)


def cq_contact(QQID, type='qq'):
    '''
    发送名片分享(contact)
        QQID        类型为qq，则为帐号；类型为group，则为群号
        type        目前支持 qq/好友分享 group/群分享
    '''
    return '[CQ:contact,type={},id={}]'.format(type, QQID)


def cq_share(shareUrl, title='', content='', imggeUrl=''):
    '''
    发送链接分享(share)
        shareUrl   分享链接
        title       分享的标题，建议12字以内
        content     分享的简介，建议30字以内
        imggeUrl   分享的图片链接，留空则为默认图片
    '''
    return '[CQ:share,url={},title={},content={},image={}]'.format(shareUrl, title, content, imggeUrl)


def cq_location(x, y, addressName, address, zoom=15):
    '''
    发送位置分享(location)
        x               经度
        y               纬度
        addressName     地点名称，建议12字以内
        address         地址，建议20字以内
        zoom            放大倍数 默认为 15
    '''
    return '[CQ:location,lat={},lon={},zoom={},title={},content={}]'.format(y, x, zoom, escape(addressName),
                                                                            escape(address))


def cq_music2(shareUrl, musicUrl, title='', content='', imageUrl=''):
    '''
    发送音乐自定义分享(music)
        shareUrl    点击分享后进入的音乐页面（如歌曲介绍页）
        musicUrl    音乐的音频链接（如mp3链接）
        title       音乐的标题，建议12字以内
        content     音乐的简介，建议30字以内
        imageUrl    音乐的封面图片链接，留空则为默认图片
    '''
    return '[CQ:music,type=custom,url={},audio={},title={},content={},image={}]'.format(shareUrl, musicUrl, title,
                                                                                        content, imageUrl)


def cq_image(imagePath):
    '''
    发送图片(image)
        imagePath   将图片放在 data\image 下，并填写相对路径。如 data\image\1.jpg 则填写 1.jpg
    '''
    return '[CQ:image,file={}]'.format(escape(imagePath))


def cq_record(recordPath):
    '''
    发送语音(record)
        recordPath   将语音放在 data\record 下，并填写相对路径。如 data\record\1.amr 则填写 1.amr
    '''
    return '[CQ:record,file={}]'.format(escape(recordPath))


"""
* 发送私聊消息, 成功返回消息ID
* QQID 目标QQ号
* msg 消息内容
"""


def _CQ_sendPrivateMsg(authCode: int, QQID: int, msg: str) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        QQID = ctypes.c_longlong(QQID)
        msg = ctypes.c_char_p(bytes(msg, 'gbk'))
        result = CQDll.CQ_sendPrivateMsg(authCode, QQID, msg)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.sendPrivateMsg = _CQ_sendPrivateMsg

"""
* 发送群消息, 成功返回消息ID
* groupid 群号
* msg 消息内容
"""


def _CQ_sendGroupMsg(authCode: int, groupid: int, msg: str) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        msg = ctypes.c_char_p(bytes(msg, 'gbk'))
        CQDll.CQ_sendGroupMsg(authCode, groupid, msg)
        return 1

        result = 1
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.sendGroupMsg = _CQ_sendGroupMsg

"""
* 发送讨论组消息, 成功返回消息ID
* discussid 讨论组号
* msg 消息内容
"""


def _CQ_sendDiscussMsg(authCode: int, discussid: int, msg: str) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        discussid = ctypes.c_longlong(discussid)
        msg = ctypes.c_char_p(bytes(msg, 'gbk'))
        result = CQDll.CQ_sendDiscussMsg(authCode, discussid, msg)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.sendDiscussMsg = _CQ_sendDiscussMsg

"""
* 撤回消息
* msgid 消息ID
"""


def _CQ_deleteMsg(authCode: int, msgid: int) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        msgid = ctypes.c_longlong(msgid)
        result = CQDll.CQ_deleteMsg(authCode, msgid)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.deleteMsg = _CQ_deleteMsg

"""
* 发送赞 发送手机赞
* QQID QQ号
"""


def _CQ_sendLike(authCode: int, QQID: int) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        QQID = ctypes.c_longlong(QQID)
        result = CQDll.CQ_sendLike(authCode, QQID)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.sendLike = _CQ_sendLike

"""
* 置群员移除
* groupid 目标群
* QQID QQ号
* rejectaddrequest 不再接收此人加群申请，请慎用
"""


def _CQ_setGroupKick(authCode: int, groupid: int, QQID: int, rejectaddrequest: bool) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        QQID = ctypes.c_longlong(QQID)
        rejectaddrequest = ctypes.c_bool(rejectaddrequest)
        result = CQDll.CQ_setGroupKick(authCode, groupid, QQID, rejectaddrequest)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupKick = _CQ_setGroupKick

"""
* 置群员禁言
* groupid 目标群
* QQID QQ号
* duration 禁言的时间，单位为秒。如果要解禁，这里填写0。
"""


def _CQ_setGroupBan(authCode: int, groupid: int, QQID: int, duration: int) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        QQID = ctypes.c_longlong(QQID)
        duration = ctypes.c_longlong(duration)
        result = CQDll.CQ_setGroupBan(authCode, groupid, QQID, duration)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupBan = _CQ_setGroupBan

"""
* 置群管理员
* groupid 目标群
* QQID QQ号
* setadmin true:设置管理员 false:取消管理员
"""


def _CQ_setGroupAdmin(authCode: int, groupid: int, QQID: int, setadmin: bool) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        QQID = ctypes.c_longlong(QQID)
        setadmin = ctypes.c_bool(setadmin)
        result = CQDll.CQ_setGroupAdmin(authCode, groupid, QQID, setadmin)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupAdmin = _CQ_setGroupAdmin

"""
* 置全群禁言
* groupid 目标群
* enableban true:开启 false:关闭
"""


def _CQ_setGroupWholeBan(authCode: int, groupid: int, enableban: bool) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        enableban = ctypes.c_bool(enableban)
        result = CQDll.CQ_setGroupWholeBan(authCode, groupid, enableban)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupWholeBan = _CQ_setGroupWholeBan
"""
* 置匿名群员禁言
* groupid 目标群
* anomymous 群消息事件收到的 anomymous 参数
* duration 禁言的时间，单位为秒。不支持解禁。
"""


def _CQ_setGroupAnonymousBan(authCode: int, groupid: int, anomymous: str, duration: int) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        anomymous = ctypes.c_char_p(bytes(anomymous, 'gbk'))
        duration = ctypes.c_longlong(duration)
        result = CQDll.CQ_setGroupAnonymousBan(authCode, groupid, anomymous, duration)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupAnonymousBan = _CQ_setGroupAnonymousBan

"""
* 置群匿名设置
* groupid 目标群
* enableanomymous true:开启 false:关闭
"""


def _CQ_setGroupAnonymous(authCode: int, groupid: int, enableanomymous: bool) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        enableanomymous = ctypes.c_bool(enableanomymous)
        result = CQDll.CQ_setGroupAnonymous(authCode, groupid, enableanomymous)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupAnonymous = _CQ_setGroupAnonymous

"""
* 置群成员名片
* groupid 目标群
* QQID 目标QQ
* newcard 新名片(昵称)
"""


def _CQ_setGroupCard(authCode: int, groupid: int, QQID: int, newcard: str) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        QQID = ctypes.c_longlong(QQID)
        newcard = ctypes.c_char_p(bytes(newcard, 'gbk'))
        result = CQDll.CQ_setGroupCard(authCode, groupid, QQID, newcard)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupCard = _CQ_setGroupCard

"""
* 置群退出 慎用, 此接口需要严格授权
* groupid 目标群
* isdismiss 是否解散 true:解散本群(群主) false:退出本群(管理、群成员)
"""


def _CQ_setGroupLeave(authCode: int, groupid: int, isdismiss: bool) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        isdismiss = ctypes.c_bool(isdismiss)
        result = CQDll.CQ_setGroupLeave(authCode, groupid, isdismiss)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupLeave = _CQ_setGroupLeave

"""
* 置群成员专属头衔 需群主权限
* groupid 目标群
* QQID 目标QQ
* newspecialtitle 头衔（如果要删除，这里填空）
* duration 专属头衔有效期，单位为秒。如果永久有效，这里填写-1。
"""


def _CQ_setGroupSpecialTitle(authCode: int, groupid: int, QQID: int, newspecialtitle: str, duration: int) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        groupid = ctypes.c_longlong(groupid)
        QQID = ctypes.c_longlong(QQID)
        newspecialtitle = ctypes.c_char_p(bytes(newspecialtitle, 'gbk'))
        duration = ctypes.c_longlong(duration)
        result = CQDll.CQ_setGroupSpecialTitle(authCode, groupid, QQID, newspecialtitle, duration)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupSpecialTitle = _CQ_setGroupSpecialTitle

"""
* 置讨论组退出
* discussid 目标讨论组号
"""


def _CQ_setDiscussLeave(authCode: int, discussid: int) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        discussid = ctypes.c_longlong(discussid)
        result = CQDll.CQ_setDiscussLeave(authCode, discussid)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setDiscussLeave = _CQ_setDiscussLeave

"""
* 置好友添加请求
* responseflag 请求事件收到的 responseflag 参数，加好友时对方发来的理由
* responseoperation REQUEST_ALLOW 或 REQUEST_DENY
* remark 添加后的好友备注
"""


def _CQ_setFriendAddRequest(authCode: int, responseflag: str, responseoperation: int, remark: str) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        responseflag = ctypes.c_char_p(bytes(responseflag, 'gbk'))
        responseoperation = ctypes.c_int(responseoperation)
        remark = ctypes.c_char_p(bytes(remark, 'gbk'))
        result = CQDll.CQ_setFriendAddRequest(authCode, responseflag, responseoperation, remark)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setFriendAddRequest = _CQ_setFriendAddRequest

"""
* 置群添加请求
* responseflag 请求事件收到的 responseflag 参数，加群时对方发来的加群理由
* requesttype根据请求事件的子类型区分 REQUEST_GROUPADD 或 REQUEST_GROUPINVITE
* responseoperation  REQUEST_ALLOW 或 REQUEST_DENY
* reason 操作理由，仅 REQUEST_GROUPADD 且 REQUEST_DENY 时可用，拒绝加群时给对方回复的拒绝理由
"""


def _CQ_setGroupAddRequestV2(authCode: int, responseflag: str, requesttype: int, responseoperation: int,
                             reason: str) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        responseflag = ctypes.c_char_p(bytes(responseflag, 'gbk'))
        requesttype = ctypes.c_int(requesttype)
        responseoperation = ctypes.c_int(responseoperation)
        reason = ctypes.c_char_p(bytes(reason, 'gbk'))
        result = CQDll.CQ_setGroupAddRequestV2(authCode, responseflag, requesttype, responseoperation, reason)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setGroupAddRequestV2 = _CQ_setGroupAddRequestV2

"""
* 取群成员信息
* groupid 目标QQ所在群
* QQID 目标QQ号
* nocache 不使用缓存
"""


def _CQ_getGroupMemberInfoV2(authCode: int, gourpId: int, QQID, useCache=False) -> [dict]:
    authCode = ctypes.c_int(authCode)
    gourpId = ctypes.c_longlong(gourpId)
    QQID = ctypes.c_longlong(QQID)
    useCache = ctypes.c_bool(useCache)
    result = CQDll.CQ_getGroupMemberInfoV2(authCode, gourpId, QQID, useCache)
    source = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')
    # 读取数据
    resultList = []

    data = base64.b64decode(source)
    if len(data) < 4:
        return []

    u = Unpack(data)
    count = u.GetInt()

    for _ in range(count):
        if u.Len() <= 0:
            return resultList
        # 读取列表数据
        _data = Unpack(u.GetToken())
        item = {
            '群号': _data.GetLong(),
            'QQID': _data.GetLong(),
            '昵称': _data.GetLenStr(),
            '名片': _data.GetLenStr(),
            '性别': _data.GetInt(),
            '年龄': _data.GetInt(),
            '地区': _data.GetLenStr(),
            '加群时间': _data.GetInt(),
            '最后发言': _data.GetInt(),
            '等级_名称': _data.GetLenStr(),
            '管理权限': _data.GetInt(),
            '不良记录成员': _data.GetInt() == 1,
            '专属头衔': _data.GetLenStr(),
            '专属头衔过期时间': _data.GetInt(),
            '允许修改名片': _data.GetInt() == 1
        }
        resultList.append(item)
    return resultList


CQP.getGroupMemberInfoV2 = _CQ_getGroupMemberInfoV2

"""
* 取陌生人信息
* QQID 目标QQ
* nocache 不使用缓存
"""


def _CQ_getStrangerInfo(authCode: int, QQID: int, useCache=False) -> dict:
    authCode = ctypes.c_int(authCode)
    QQID = ctypes.c_longlong(QQID)
    result = CQDll.CQ_getStrangerInfo(authCode, QQID, useCache)
    source = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')

    # 读取数据
    resultList = []

    data = base64.b64decode(source)
    if len(data) < 4:
        return []

    u = Unpack(data)

    return {
        'QQID': u.GetLong(),
        '昵称': u.GetLenStr(),
        '性别': u.GetInt(),
        '年龄': u.GetInt()
    }


CQP.getStrangerInfo = _CQ_getStrangerInfo

"""
* 添加日志
* priority 优先级，CQP.CQLOG_* 开头的常量
* category 类型    日志标题
* content 内容
"""


def _CQ_addLog(authCode: int, priority: int, category: str, content: str) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        priority = ctypes.c_int(priority)
        category = ctypes.c_char_p(bytes(category, 'gbk'))
        content = ctypes.c_char_p(bytes(content, 'gbk'))
        result = CQDll.CQ_addLog(authCode, priority, category, content)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.addLog = _CQ_addLog

"""
* 取Cookies 慎用, 此接口需要严格授权
"""


def _CQ_getCookies(authCode: int) -> str:
    try:
        authCode = ctypes.c_int(authCode)
        result = CQDll.CQ_getCookies(authCode)
        result = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')
        return result
    except:
        return ''


CQP.getCookies = _CQ_getCookies

"""
* 取CsrfToken 慎用, 此接口需要严格授权
"""


def _CQ_getCsrfToken(authCode: int) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        result = CQDll.CQ_getCsrfToken(authCode)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.getCsrfToken = _CQ_getCsrfToken

"""
* 取登录QQ
"""


def _CQ_getLoginQQ(authCode: int) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        result = CQDll.CQ_getLoginQQ(authCode)
        result = result = ctypes.c_longlong(result).value
        return result
    except:
        return -1


CQP.getLoginQQ = _CQ_getLoginQQ

"""
* 取登录QQ昵称
"""


def _CQ_getLoginNick(authCode: int) -> str:
    try:
        authCode = ctypes.c_int(authCode)
        result = CQDll.CQ_getLoginNick(authCode)
        result = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')
        return result
    except:
        return ''


CQP.getLoginNick = _CQ_getLoginNick

"""
* 取应用目录，返回的路径末尾带"\"
"""


def _CQ_getAppDirectory(authCode: int) -> str:
    try:
        authCode = ctypes.c_int(authCode)
        result = CQDll.CQ_getAppDirectory(authCode)
        result = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')
        return result
    except:
        return ''


CQP.getAppDirectory = _CQ_getAppDirectory

"""
* 置致命错误提示
* errorinfo 错误信息
"""


def _CQ_setFatal(authCode: int, errorinfo: str) -> int:
    try:
        authCode = ctypes.c_int(authCode)
        errorinfo = ctypes.c_char_p(bytes(errorinfo, 'gbk'))
        result = CQDll._CQ_setFatal(authCode, errorinfo)
        result = result = ctypes.c_int32(result).value
        return result
    except:
        return -1


CQP.setFatal = _CQ_setFatal

"""
* 接收语音，接收消息中的语音(record),返回保存在 \data\record\ 目录下的文件名
* file 收到消息中的语音文件名(file), 可用get_message_records(msg)[0] 获取第一个
* outformat 应用所需的语音文件格式，目前支持 mp3 amr wma m4a spx ogg wav flac
"""


def _CQ_getRecord(authCode: int, file: str, format: str) -> str:
    authCode = ctypes.c_int(authCode)
    file = ctypes.c_char_p(bytes(file, 'gbk'))
    format = ctypes.c_char_p(bytes(format, 'gbk'))
    result = CQDll.CQ_getRecordV2(authCode, file, format)
    return ctypes.c_char_p(result).value.decode('gbk', errors='ignore')


CQP.getRecord = _CQ_getRecord

"""
* 接收图片
* file 收到消息中的图片文件名(file), get_message_images(msg)[0] 获取第一个
"""


def _CQ_getImage(authCode: int, file: str) -> str:
    authCode = ctypes.c_int(authCode)
    file = ctypes.c_char_p(bytes(file, 'gbk'))
    result = CQDll.CQ_getImage(authCode, file)
    return ctypes.c_char_p(result).value.decode('gbk', errors='ignore')


CQP.getImage = _CQ_getImage

"""
* 接收语音，接收消息中的语音(record),返回保存在 \data\record\ 目录下的文件名
* file 收到消息中的语音文件名(file), 可用get_message_records(msg)[0] 获取第一个
* format 应用所需的语音文件格式，目前支持 mp3 amr wma m4a spx ogg wav flac
"""


def _CQ_getRecordV2(authCode: int, file: str, format: str) -> str:
    authCode = ctypes.c_int(authCode)
    file = ctypes.c_char_p(bytes(file, 'gbk'))
    format = ctypes.c_char_p(bytes(format, 'gbk'))
    result = CQDll.CQ_getRecordV2(authCode, file, format)
    return ctypes.c_char_p(result).value.decode('gbk', errors='ignore')


CQP.getRecordV2 = _CQ_getRecordV2

"""
* 获取群成员列表
* gourpId 群号
"""


def _CQ_getGroupMemberList(authCode: int, gourpId: int) -> [dict]:
    authCode = ctypes.c_int(authCode)
    gourpId = ctypes.c_longlong(gourpId)
    result = CQDll.CQ_getGroupMemberList(authCode, gourpId)

    source = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')

    # 读取数据
    resultList = []

    data = base64.b64decode(source)
    if len(data) < 4:
        return []

    u = Unpack(data)
    count = u.GetInt()

    for _ in range(count):
        if u.Len() <= 0:
            return resultList
        # 读取列表数据
        _data = Unpack(u.GetToken())
        item = {
            '群号': _data.GetLong(),
            'QQID': _data.GetLong(),
            '昵称': _data.GetLenStr(),
            '名片': _data.GetLenStr(),
            '性别': _data.GetInt(),
            '年龄': _data.GetInt(),
            '地区': _data.GetLenStr(),
            '加群时间': _data.GetInt(),
            '最后发言': _data.GetInt(),
            '等级_名称': _data.GetLenStr(),
            '管理权限': _data.GetInt(),
            '不良记录成员': _data.GetInt() == 1,
            '专属头衔': _data.GetLenStr(),
            '专属头衔过期时间': _data.GetInt(),
            '允许修改名片': _data.GetInt() == 1
        }
        resultList.append(item)
    return resultList


CQP.getGroupMemberList = _CQ_getGroupMemberList

"""
* 获取群列表
"""


def _CQ_getGroupList(authCode: int) -> [dict]:
    authCode = ctypes.c_int(authCode)
    result = CQDll.CQ_getGroupList(authCode)
    source = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')

    # 读取数据
    resultList = []

    data = base64.b64decode(source)
    if len(data) < 4:
        return []

    u = Unpack(data)
    count = u.GetInt()

    for _ in range(count):
        if u.Len() <= 0:
            return resultList
        # 读取列表数据
        _data = Unpack(u.GetToken())
        item = {
            '群号': _data.GetLong(),
            '名称': _data.GetLenStr(),
        }
        resultList.append(item)
    return resultList


CQP.getGroupList = _CQ_getGroupList

"""
* 获取好友列表
"""


def _CQ_getFriendList(authCode: int) -> [dict]:
    authCode = ctypes.c_int(authCode)
    result = CQDll.CQ_getGroupList(authCode)

    source = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')

    # 读取数据
    resultList = []

    data = base64.b64decode(source)
    if len(data) < 4:
        return []

    u = Unpack(data)
    count = u.GetInt()

    for _ in range(count):
        if u.Len() <= 0:
            return resultList
        # 读取列表数据
        _data = Unpack(u.GetToken())
        item = {
            '帐号': _data.GetLong(),
            '昵称': _data.GetLenStr(),
            '备注': _data.GetLenStr(),
        }
        resultList.append(item)
    return resultList


CQP.getFriendList = _CQ_getFriendList

"""
* 是否可发送语音
"""


def _CQ_canSendRecord(authCode: int) -> bool:
    return ctypes.c_int(CQDll.CQ_canSendRecord(authCode)).value > 0


CQP.canSendRecord = _CQ_canSendRecord

"""
* 是否可发送图片
"""


def _CQ_canSendImage(authCode: int) -> bool:
    return ctypes.c_int(CQDll.CQ_canSendImage(authCode)).value > 0


CQP.canSendImage = _CQ_canSendImage

"""
* 取Cookies 慎用, 此接口需要严格授权
* domain 域名，例如：qq.com
"""


def _CQ_getCookiesV2(authCode: int, domain: str) -> str:
    try:
        authCode = ctypes.c_int(authCode)
        domain = ctypes.c_char_p(bytes(domain, 'gbk'))
        result = CQDll.CQ_getCookiesV2(authCode, domain)
        result = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')
        return result
    except:
        return ''


CQP.getCookiesV2 = _CQ_getCookiesV2

"""
* 取群信息
* gourpId  群号
* useCache 是否使用缓存
"""


def _CQ_getGroupInfo(authCode: int, gourpId: int, useCache=False) -> [dict]:
    authCode = ctypes.c_int(authCode)
    gourpId = ctypes.c_longlong(gourpId)
    useCache = ctypes.c_bool(useCache)
    result = CQDll.CQ_getGroupInfo(authCode, gourpId, useCache)

    source = ctypes.c_char_p(result).value.decode('gbk', errors='ignore')

    # 读取数据
    resultList = []

    data = base64.b64decode(source)
    if len(data) < 4:
        return []

    u = Unpack(data)
    count = u.GetInt()

    for _ in range(count):
        if u.Len() <= 0:
            return resultList
        # 读取列表数据
        _data = Unpack(u.GetToken())
        item = {
            '群号': _data.GetLong(),
            '名称': _data.GetLenStr(),
            '当前人数': _data.GetInt(),
            '人数上限': _data.GetInt(),
        }
        resultList.append(item)
    return resultList


CQP.getGroupInfo = _CQ_getGroupInfo

"""
* 发送赞 发送手机赞
* QQID QQ号
"""


def _CQ_sendLikeV2(authCode: int, QQID: int) -> int:
    authCode = ctypes.c_int(authCode)
    QQID = ctypes.c_longlong(QQID)
    result = CQDll.CQ_sendLikeV2(authCode, QQID)
    result = ctypes.c_int32(result).value
    return result


CQP.sendLikeV2 = _CQ_sendLikeV2
