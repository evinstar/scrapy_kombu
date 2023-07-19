# -*- coding:utf-8 -*-
# @Filename:    constants.py
# @Author:      andy
# @Time:        2023/2/7 14:24

COMPANY_NAME = 'companyName'  # string	公司名称

# 联系方式
FINGER_PRINT = 'fingerprint'  # string	URL指纹
URL = 'url'  # string	URL
DETAIL_URL = 'detailUrl'
UPDATE_DATE = 'updatedDate'  # Date	更新时间
ADDRESS = 'address'  # string	联系方式地址
QQ = 'qq'  # string	qq号
TELEPHONE_FIXED = 'telephoneFixed'  # string	固话（一个/多个）
TELEPHONE_MOBILE = 'telephoneMobile'  # string	手机（一个/多个）
TELEPHONE = 'telephone'  # string	无法区分手机或者固话
EMAIL = 'email'  # string	邮箱
CONTACT = 'contact'  # string	联系人
GENDER = 'gender'  # string	性别
POSITION = 'position'  # string	职位
WECHAT = 'wechat'  # string	微信账号
TAGS = 'tags'  # 认证标签
# POSTCODE = 'postCode'  # string 邮编，我自己加的

FIELD_REFLECT = {
    '公司名称': COMPANY_NAME,
    '传真': TELEPHONE_FIXED,
    '其他联系方式': TELEPHONE,
    '其它联系方式': TELEPHONE,
    '联系方式': TELEPHONE,
    '地址': ADDRESS,
    '电话': TELEPHONE,
    # '邮编': POSTCODE,
    '联系人': CONTACT,
    '职位': POSITION,
    '手机': TELEPHONE,
    '微信': WECHAT
}

# 经营概况
BUSINESS_SCOPE = "bussinessScope"  # string 经营范围
BUSINESS_PRODUCT = "bussinessProduct"  # string 主营产品
COMPANY_TYPE = "companyType"  # string 企业类型:有限责任公司
INDUSTRY = "industry"  # string 主营行业
BUSINESS_MODEL = "bussinessModel"  # string 经营模式:生产型
BUSINESS_MODEL_TYPE = "bussinessModelType"  # string 经营模式:生产型
REGISTER_ADDRESS = "registerAddress"  # string 注册地址
ESTABLISHED_DATE = "establishedDate"  # string 成立日期
INV_TYPE = "invType"  # string 法人代表/负责人
BUSINESS_ADDRESS = "businessAddress"  # string 经营地址
BUSINESS_LICENSE_NUM = "businessLicenseNum"  # string 营业执照号码
BUSINESS_STATUS = "businessStatus"  # string 经营状态
SCALE = "scale"  # string 员工人数
LICENSE_INSTITUTION = "licenseInstitution"  # string 发证机关
ANNUAL_TURNOVER = "annualTurnover"  # string 年营业额
MONTHLY_TURNOVER = "monthlyTurnover"  # string 月营业额
BRAND = "brand"  # string 经营品牌
REGISTER_CAPITAL = "registerCapital"  # string 注册资金
BUSINESS_CLIENT = "businessClient"  # string 客户群
BUSINESS_MARKET = "businessMarket"  # string 主要市场
MONTH_YIELD = "monthYield"  # string 月产量
FACTORY_AREA = "factoryArea"  # string 厂房面积
CITY = "city"  # string 所属城市
OEM_SERVICE = "OEMService"  # string 提供OEM服务
QUALITY_CONTROL = "qualityControl"  # string 质量控制
WEBSITE = "website"  # string 公司网站
MGT_CERT = "mgtCert"  # string 管理体系认证
CERT_INFO = "certInfo"  # string 认证信息
ANNUAL_EXP_VOLUME = "annualExpVolume"  # string 年出口额
ANNUAL_IMP_VOLUME = "annualImpVolume"  # string 年进口额
REGISTER_BANK = "registerBank"  # string 开户银行
BANK_ACCOUNT = "bankAccount"  # string 开户银行
CREDIT_PERSON = "creditPerson"  # string 资信参考人
RESEARCH_RECRUIT_NUM = "researchRecruitNum"  # string 研发部门人数
CERTIFICATE = "certificate"  # string 荣誉及证书
TAX_NUMBER = "taxNumber"  # string 税号
MEMBER_EVALUATION = "memberEvaluation"  # string 会员评价
SHAREHOLDER_NUM = "shareholderNum"  # string 股东人数
WAREHOUSE_AREA = "warehouseArea"  # string 库房面积
BRANCH_OFFICE_NUM = "branchOfficeNum"  # string 分支机构个数
COMPANY_INFO = "companyInfo"  # string 公司描述
BUSINESS_FROM = "bussinessFrom"  # string 核准日期
CATEGORY = "category"  # string 所属分类
POPULAR_VALUE = "popularValue"  # string 人气值
BUSINESS_TO = "bussinessTo"  # string 经营期限
PRO_QUALITY_CERT = "proQualityCert"  # string 产品质量认证
CRAFT = "craft"  # string 工艺
PROCESS_METHOD = "processMethod"  # string 加工方式
BUY_PRODUCT = "buyProduct"  # string 采购产品
VALUE_ADDED_SERVICE = "valueAddedService"  # string 增值服务
CARRY_GOODS = "carryGoods"  # string 承载货物类型
WAREHOUSE_INFO = "warehouseInfo"  # string 仓库信息
ADVANTAGE_ROUTE = "advantageRoute"  # string 优势路线
VEHICLE_RESOURCE = "vehicleResource"  # string 车辆资源
COMPANY_OUTLET = "companyOutlet"  # string 公司网点
COMPANY_SHORT_NAME = "companyShortName"  # string 公司简称

# 招聘
WELFARE_TAGS = "welfareTags"  # string[] 福利标签
# WELFARE = "welfare"  # string 福利
EDUCATION = "education"  # string 教育学历
CAREER_DURATION = "careerDuration"  # string 工作年限
RECRUIT_REGION = "recruitRegion"  # string 招聘地区
JOB_NAME = "jobName"  # string 职位名称
PAY = "pay"  # string 薪资
# JOB_TAGS = "jobTags"  # string[] 工作标签
JOB_INTRO = "jobIntro"  # string 职位介绍
RECRUITER_POSITION = "recruiterPosition"  # string 招聘人员职位
RECRUITER_NAME = "recruiterName"  # string 招聘人员姓名
RECRUITER_ACTIVE_TIME = "recruiterActiveTime"  # string 招聘人员在线时间
RECRUITER_VERIFY_TAG = "recruiterVerifyTag"  # string 招聘人员认证标签
RECRUITER_AVATAR_URL = "recruiterAvatarUrl"  # string 招聘人员头像地址
JOB_COUNT = "jobCount"  # string 招聘职位数量
JOB_PERSON_COUNT = "jobPersonCount"  # string 招聘职位人数
JOB_RELEASE_DATE = "jobReleaseDate"  # string 职位发布日期

PROXY_DISABLED = 'proxy_disabled'  # 是否不使用代理
PROXY_DIRECT = 'proxy_direct'  # 是否直接从代理商获取代理

REQUEST_DUPE = 'request_dupe'  # 是否启用request 数据库去重

DELIVERY_TAG = 'delivery_tag'
COLLECT_NUM = 'collectNum'
COLLECT_TIME = 'collectTime'
HAS_COLLECTED_NUM = 'has_collected_num'

UNIQUE_ID = 'uniqueId'
ID = 'id'
