import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
def ocr(url: str):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential("AKIDb1B4h5C2arrgIeka9RTEivqVt0pOghRv", "FDuOgmdEbiZAXfYCk24qMegSyFG1WmmW")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.GeneralEfficientOCRRequest()
        params = {
            "ImageUrl": url
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个GeneralEfficientOCRResponse的实例，与请求对象对应
        resp = client.GeneralEfficientOCR(req)
        # 输出json格式的字符串回包
        dic = json.loads(resp.to_json_string(), strict=False)
        ocr_result = ''
        for s in dic["TextDetections"]:
            ocr_result += s['DetectedText']
        # print(ocr_result)
        return ocr_result
    except TencentCloudSDKException as err:
        print(err)

ocr('https://gchat.qpic.cn/qmeetpic/94396271637902305/1634868-2217775316-F5B7620C7F3E1D7A1DC07E9BBE249223/0')
