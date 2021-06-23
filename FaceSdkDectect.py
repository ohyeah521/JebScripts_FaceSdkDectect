# -*- coding: utf-8 -*-
# FaceSdkDectect
# Code by：我是土匪


import re
from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.actions import Actions, ActionContext, ActionCommentData, ActionXrefsData
from com.pnfsoftware.jeb.core.events import JebEvent, J
from com.pnfsoftware.jeb.core.output import AbstractUnitRepresentation, UnitRepresentationAdapter
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem
from com.pnfsoftware.jeb.core.units.code.java import IJavaSourceUnit, IJavaStaticField, IJavaNewArray, IJavaConstant, IJavaCall, IJavaField, IJavaMethod, IJavaClass

face_sdk_classes={
    # 旷视科技
    u'旷视科技-www.megvii.com': r'com.megvii.facepp\S*',
    u'旷视科技-www.megvii.com': r'com.megvii.idcardquality\S*',
    u'旷视科技-www.megvii.com': r'com.megvii.kas\S*',
    u'旷视科技-www.megvii.com': r'com.megvii.kassilentlive.sdk\S*',
    u'旷视科技-www.megvii.com': r'megvii.openapi.access\S*',
    
    # 商汤科技
    u'商汤科技-www.sensetime.com': r'com.sensetime.senseid.sdk\S*',
    
    # 平安科技
    u'平安科技-tech.pingan.com': r'com.pingan.ai.face.entity\S*',
    u'平安科技-tech.pingan.com': r'com.pingan.ai.face.manager\S*',
    
    # 科大讯飞
    u'科大讯飞-www.iflytek.com': r'com.iflytek.cloud.FaceRequest\S*',
    u'科大讯飞-www.iflytek.com': r'com.iflytek.cloud.FaceDetector\S*',
    
    # 海鑫科金
    u'海鑫科金-www.hisign.com.cn': r'com.hisign.FaceSDK\S*',
    u'海鑫科金-www.hisign.com.cn': r'com.hisign.facedetectv1small\S*',
    u'海鑫科金-www.hisign.com.cn': r'com.hisign.matching.UvcInputAPI\S*',
    
    # 爱莫科技    
    u'爱莫科技-www.aimall-tech.com': r'com.aimall.sdk.faceactiondetector\S*',
    u'爱莫科技-www.aimall-tech.com': r'com.aimall.sdk.trackerdetector\S*',
    u'爱莫科技-www.aimall-tech.com': r'com.aimall.core\S*',
    
    # 百度
    u'百度AI-www.ai.baidu.com': r'com.baidu.idl.facesdk\S*',
    
    # (杭州小孔成像)
    u'杭州小孔成像-www.dface.tech': r'com.dface.api.FaceDetect\S*',
    u'杭州小孔成像-www.dface.tech': r'com.dface.api.FaceCompare\S*',
    u'杭州小孔成像-www.dface.tech': r'com.dface.api.FaceTrack\S*',
    u'杭州小孔成像-www.dface.tech': r'com.dface.dto.LicenseInfoType\S*',
   

    # Seetatech中科视拓
    u'中科视拓-www.seetatech.com': r'com.seeta.sdk\S*',
    
    # 云从科技
    u'广州云从科技-www.cloudwalk.com': r'cn.cloudwalk.FaceInterface\S*',
    u'广州云从科技-www.cloudwalk.com': r'cn.cloudwalk.callback.FaceInfoCallback\S*',
    u'广州云从科技-www.cloudwalk.com': r'cn.cloudwalk.sdk.FaceInfo\S*',
    u'广州云从科技-www.cloudwalk.com': r'cn.cloudwalk.sdk.realtime.FaceInfoCallback\S*',
    u'广州云从科技-www.cloudwalk.com': r'cn.cloudwalk.libproject\S*',
    
    
    # 杭州虹软
    u'杭州虹软科技-www.ai.arcsoft.com.cn': r'com.arcsoft.facetracking\S*',
    u'杭州虹软科技-www.ai.arcsoft.com.cn': r'com.arcsoft.facerecognition\S*',
    
    # FaceTec
    u'FaceTec-dev.facetec.com/': r'com.facetec.sdk.FaceTecSDK\S*',
    u'FaceTec-dev.facetec.com/': r'com.facetec.sdk.FaceTecSessionStatus\S*',
    u'FaceTec-dev.facetec.com/': r'com.facetec.sdk.FaceTecSDKStatus\S*',
    

    # 依图科技
    u'上海依图科技-https://www.yitutech.com/': r'com.yitutech.face\S*',

    
    
}
found_sdk=[]
class FaceSdkDectect(IScript):

    def run(self, ctx):
        global face_sdk_classes
        global found_sdk
        engctx = ctx.getEnginesContext()
        if not engctx:
            print('Back-end engines not initialized')
            return

        projects = engctx.getProjects()
        if not projects:
            print('There is no opened project')
            return

        project = projects[0] # Get current project(IRuntimeProject)
        print('Decompiling code units of %s...' % project)

        codeUnit = RuntimeProjectUtil.findUnitsByType(project, ICodeUnit, False) # Get the current codeUnit(ICodeUnit)
    
        for unit in codeUnit:
            classes = unit.getClasses() # Get a reference to the Java class defined in this unit
          
            for cls in classes:
                # print(cls)
                for (key, value) in face_sdk_classes.items():
                    pattern =  re.compile(value, re.I)
                    x = pattern.search(str(cls))
                    if(x):
                        found_sdk.append(key)
        found_sdk = list(set(found_sdk))
        print("FaceSdkDectect ------------------------------------------------")
        for sdk in found_sdk:
            print(sdk.encode('utf-8', errors='ignore').decode('utf-8'))
        print("FaceSdkDectect ------------------------------------------------")
                 
 