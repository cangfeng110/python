import os
import sys
import time
import json
import hashlib
import pymongo
import requests
import argparse
from bson.objectid import ObjectId
from contextlib import closing
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

global defaultUrlUcdf
global defaultUrlOthers
global defaultUploadUcdfUrl
global defaultUploadOthersUrl
global defaultDeleteUcdfUrl
global defaultDeleteOthersUrl

defaultUrlUcdf = "http://10.0.195.159/ucdf/"
defaultUrlOthers = "http://10.0.195.159/map/"
defaultUploadUcdfUrl = "http://10.0.195.159/.tool/upload_file.php"
defaultUploadOthersUrl = "http://10.0.195.159/.tool/upload_file.php"
defaultDeleteUcdfUrl = "http://10.0.195.159/.tool/delete_file.php"
defaultDeleteOthersUrl = "http://10.0.195.159/.tool/delete_file.php"

class MongoDB:
    def __init__(self, host, port):
        self.client = pymongo.MongoClient(host=host, port=port)

    def getDBHandle(self, dbName):
        return self.client[dbName]

    def getCollByDB(self, dbName, collName):
        db = self.getDBHandle(dbName)
        collNames = db.collection_names()
        if collName in collNames:
            return collNames, db[collName], db
        else:
            return collNames, None, db

    def creatCollByDB(self, dbName, collName):
        db = self.getDBHandle(dbName)
        collNames = db.collection_names()
        return collNames, db[collName], db

    def creatNewColl(self, dbName, collName):
        db = self.client[dbName]
        collHandle = db["%s" % collName]
        return collHandle

    def findByTag(self, coll, tag):
        return coll.find(tag)

    def findMany(self, coll, number=None):
        res = []
        if number is None:
            for x in coll.find():
                res.append(x)
        else:
            for x in coll.find().limit(int(number)):
                res.append(x)
        return res

    def insertMany(self, coll, docList):
        ret = coll.insert_many(docList)
        if len(ret.inserted_ids) == len(docList):
            return True
        else:
            return False

    def findOneByDoc(self, coll, doc):
        res = None
        res = coll.find_one(doc)
        return res

    def updateOneByTag(self, coll, condition, dic):
        res = coll.update_one(condition, {'$set': dic})
        return res.matched_count, res.modified_count

    def updateManyByTag(self, coll, condition, meet):
        res = coll.update_many(condition, meet)
        return res.matched_count, res.modified_count

    def deleteMany(self, coll, condition):
        res = coll.delete_many(condition)
        return res.deleted_count


class FileTransfer:
    def __init__(self):
        pass

    def parseUrl(self, url):
        url = url.split("/")
        mapOrUcdf = url[-4]
        label = url[-3]
        caseId = url[-2]
        fileName = url[-1]
        return mapOrUcdf, label, caseId, fileName

    def deleteFile(self, url):
        mapOrUcdf, label, caseId, fileName = self.parseUrl(url)
        if url.find("ucdf") >= 0:
            url = defaultDeleteUcdfUrl
        else:
            url = defaultDeleteOthersUrl

        data = { "name": fileName, "label":label, "caseId": caseId, "to": mapOrUcdf}
        r = requests.post(url, data=data)
        status = False
        if str(r).find("200") >= 0:
            status = True
        else:
            status = False
        return status

    def uploadFile(self, url, file, fileName, label, caseId):
        progress = 0
        caseId = "case" + str(caseId)
        serverFolder = "ucdf"
        if file.find("ucdf") >= 0:
            url = defaultUploadUcdfUrl
            serverFolder = "ucdf"
        else:
            url = defaultUploadOthersUrl
            serverFolder = "map"

        def my_callback(monitor):
            progress = (monitor.bytes_read / monitor.len) * 100
            # print("Uploading progress: %d" %progress)

        e = MultipartEncoder(fields={"label":label, "caseId": caseId, "to": serverFolder, 'file1': (fileName, open(file, 'rb'))})
        m = MultipartEncoderMonitor(e, my_callback)
        r = requests.post(url, data=m, headers={'Content-Type': m.content_type})
        status = False
        # print(r.text)
        if str(r).find("200") >= 0:
            status = True
        else:
            status = False
        return status

    def downLoadFile(self, url, filePath):
        nowJd = 0
        status = False
        with closing(requests.get(url, stream=True)) as response:
            chunkSize = 1024
            contentSize = int(response.headers['content-length'])
            dataCount = 0
            with open(filePath, "wb") as file:
                for data in response.iter_content(chunk_size=chunkSize):
                    file.write(data)
                    dataCount = dataCount + len(data)
                    nowJd = (dataCount / contentSize) * 100
        if int(nowJd) == 100:
            status = True
        return status


class UserInterface:
    def __init__(self, host, port):
        self.fileTransfer = FileTransfer()
        self.mongoDB = MongoDB(host, port)
        self.session = ""

    def startSession(self):
        self.session = self.mongoDB.client.start_session()
        self.session.start_transaction()

    def endSession(self):
        self.session.end_session()

    def abortSession(self):
        self.session.abort_transaction()

    def commitSession(self):
        self.session.commit_transaction()

    def findAllLabel(self, label=None):
        self.mongoDB.findByTag(label)

    def getDBHandle(self, dbName):
        return self.mongoDB.getDBHandle(dbName)

    def creatNewLabel(self, dbName, label):
        newHandle = self.mongoDB.creatNewColl(dbName, label)
        return newHandle

    def getJsonContent(self, file):
        flag = True
        data = None
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except Exception as e:
            flag = False
        return data, flag

    def getJsonContentByCase(self, workdir):
        filePath = None
        data = None
        flag = False
        for root, dirs, files in os.walk(workdir):
            for file in files:
                if file.find(".case.json") >= 0:
                    filePath = os.path.join(root, file)
            break
        if filePath is not None:
            data, flag = self.getJsonContent(filePath)
        return data, flag, filePath

    def getCasesContentWhenDelete(self, folder):
        allCases = self.getCasesByFolder(folder)
        newCases = []
        casesPath = []
        for case in allCases:
            if len(case) == 0:
                continue
            temp = case[0]
            tempWorkdir = os.path.dirname(temp)
            data, _, _ = self.getJsonContentByCase(tempWorkdir)
            newCases.append(data)
            casesPath.append(tempWorkdir)
        return newCases, casesPath

    def getCasesWhenSubmit(self, folder):
        allCases = self.getCasesByFolder(folder)
        newCases = []
        for case in allCases:
            if len(case) == 0:
                continue
            temp = case[0]
            tempWorkdir = os.path.dirname(temp)
            jsonPath = self.jsonCountAndPath(tempWorkdir)
            if jsonPath is not None:
                for jsonFile in jsonPath:
                    case.append(jsonFile)
            newCases.append(case)
        return newCases

    def replaceAndMerge(self, sourceContent, updateContent):
        for k in updateContent:
            if k not in sourceContent:
                sourceContent[k] = updateContent[k]
            elif type(sourceContent[k]) is dict and type(updateContent[k]) is dict:
                sourceContent[k] = self.replaceAndMerge(sourceContent[k], updateContent[k])
            else:
                sourceContent[k] = updateContent[k]
        return sourceContent

    def formatOneDoc(self, caseWithJson, label, caseId, update=False):
        doc = {}
        docList = []
        errorJson = None
        localPath = None
        lastJson = None
        for file in caseWithJson:
            if file.find(".case.json") >= 0:
                localPath = os.path.dirname(file)
                if update:
                    lastJson, flag = self.getJsonContent(file)
                continue
            if file.find("json") >= 0 and file.find("uos_common.json") < 0:
                updateJson, flag = self.getJsonContent(file)
                if updateJson is not None:
                    if updateJson.has_key("_id"):
                        del updateJson["_id"]
                    if flag:
                        doc = self.replaceAndMerge(doc, updateJson)
                        continue
                    else:
                        errorJson = file
                        break
            if file.find("ucdf") >= 0:
                if localPath is None:
                    localPath = os.path.dirname(file)
                url = defaultUrlUcdf + label +"/" + "case" + str(caseId) + "/" + os.path.basename(file)
            else:
                if localPath is None:
                    localPath = os.path.dirname(file)
                url = defaultUrlOthers + label + "/" + "case" + str(caseId) + "/" + os.path.basename(file)
            doc["label"] = label
            doc["caseId"] = caseId
            if doc.has_key("Resource"):
                doc["Resource"].append(url)
            else:
                doc["Resource"] = []
                doc["Resource"].append(url)
        if lastJson is not None:
            doc = self.replaceAndMerge(lastJson, doc)
        docList.append(doc)
        return docList, errorJson, localPath

    def jsonCountAndPath(self, folder):
        countJson = 0
        filePath = None
        fileList = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.find("json") >= 0:
                    filePath = os.path.join(root, file)
                    countJson = countJson + 1
                    fileList.append(filePath)
            break
        if countJson != 0:
            filePath = fileList

        return filePath

    def getCasesByFolder(self, folder):
        allCases = []
        for root, dirs, files in os.walk(folder):
            case = []
            for file in files:
                file = os.path.join(root, file)
                case.append(file)

            hasHmap = hasUcdf = False
            for file in case:
                if file.find("hmap") >= 0:
                    hasHmap = True
                if file.find("ucdf") >= 0:
                    hasUcdf = True
            if hasHmap and hasUcdf:
                allCases.append(case)

            for dir in dirs:
                dir = os.path.join(root, dir)
                if os.path.isdir(dir):
                    self.getCasesByFolder(dir)
        return allCases

    def getNewCaseId(self, dbName, sumName, labelName):
        isCurrentId = False
        isSlotId = False
        caseRecordIdHandle, _,  flag = self.creatCollection(dbName, sumName)
        res = caseRecordIdHandle.find_one({"name":"labels"})
        if res is not None:
            if res.has_key(labelName):
                if res[labelName].has_key("slot") and len(res[labelName]["slot"]) != 0:
                    newCaseId = int(res[labelName]["slot"][0])
                    isSlotId = True
                else:
                    currentId = res[labelName]["currentId"]
                    newCaseId = int(currentId) + 1
                    isCurrentId = True
            else:
                newCaseId = 0
                isCurrentId = True
        else:
            newCaseId = 0
            isCurrentId = True
            insertRes = {}
            insertRes["name"] = "labels"
            caseRecordIdHandle.insert_one(insertRes)

        self.updateCaseId(dbName, sumName, labelName,  newCaseId, isCurrentId, isSlotId)
        return newCaseId, caseRecordIdHandle, isCurrentId, isSlotId

    def updateCaseId(self, dbName, sumName, labelName, caseId, isCurrentId=False, isSlotId=False):
        caseRecordIdHandle, _,  flag = self.getCollection(dbName, sumName)
        res = caseRecordIdHandle.find_one({"name":"labels"})
        if res.has_key(labelName):
            pass
        else:
            res[labelName] = {}

        if isCurrentId and not isSlotId:
            res[labelName]["currentId"] = caseId

        if not isCurrentId and isSlotId:
            sameIds = []
            for id in range(len(res[labelName]["slot"])):
                if int(res[labelName]["slot"][id]) == caseId:
                    sameIds.append(id)
            try:
                for index in range(len(sameIds)):
                    res[labelName]["slot"].remove(caseId)
            except Exception as ListError:
                print(ListError)

        if not isCurrentId and not isSlotId:
            if res[labelName].has_key("slot"):
                if caseId in res[labelName]["slot"]:
                    pass
                else:
                    res[labelName]["slot"].append(caseId)
            else:
                res[labelName]["slot"] = []
                res[labelName]["slot"].append(caseId)

        self.updateOne(caseRecordIdHandle, {"name":"labels"}, res)

    def getMd5(self, file):
        with open(file, 'rb') as fp:
            data = fp.read()
        fileMd5 = hashlib.md5(data).hexdigest()
        return fileMd5

    def constructCaseById(self, case):
        urlList = []
        fileList = []
        fileNames = []
        for file in case:
            fileName = os.path.basename(file)
            if file.find(".case.json") >= 0:
                continue
            if fileName.find("ucdf") >= 0:
                urlList.append(defaultUploadUcdfUrl)
            else:
                urlList.append(defaultUploadOthersUrl)
            # fileName = str(self.getMd5(file)) + "." + file.split(".")[-1]
            fileList.append(file)
            fileNames.append(fileName)

        return urlList, fileList, fileNames

    def uploadCase(self, case, label, id):
        urlList, fileList, fileNames = self.constructCaseById(case)
        flag, leftFile = self.uploadFile(urlList, fileList, fileNames, label, id)
        return flag, leftFile

    def updateCaseRecordData(self, recordDBHandle,  newCaseId, meet):
        return self.updateOne(recordDBHandle, newCaseId, meet)

    def createdCaseDir(self, dir):
        ids = []
        nowId = None
        for root, dirs ,files in os.walk(dir):
            for dir in dirs:
                ids.append(int(dir.split("case")[-1]))
            break
        for idIndex in range(len(ids)):
            if int(idIndex) != ids[idIndex]:
                nowId = idIndex
        if nowId is None:
            nowId = 0
        localCaseId = "case"+str(nowId)
        return localCaseId

    def getCaseFolderByURL(self, url, fileFolder):
        splitRes = url.split("/")
        fileName = splitRes[-1]
        label = splitRes[-3]
        caseId = splitRes[-2]
        caseRepo = os.path.join(fileFolder, label)
        # localCaseId = self.createdCaseDir(caseRepo)
        caseFolder = os.path.join(caseRepo, caseId)
        return caseFolder

    def getFileNameByURL(self, url):
        splitRes = url.split("/")
        return splitRes[-1]

    def getCollection(self, dbName, collName):
        collNames, collHandle, _ = self.mongoDB.getCollByDB(dbName, collName)
        if collHandle is not None:
            return collHandle, collNames, True
        else:
            return collHandle, collNames, False

    def creatCollection(self, dbName, collName):
        collNames, collHandle, _ = self.mongoDB.creatCollByDB(dbName, collName)
        if collHandle is not None:
            return collHandle, collNames, True
        else:
            return collHandle, collNames, False

    def getManyCasesURL(self, label, number):
        thisCollCases = []
        collHandle, _,  Flag = self.getCollection(dbName, label)
        res = self.mongoDB.findMany(collHandle, number)
        for item in res:
            thisCollCases.append(item["Resource"])
        return thisCollCases

    def updateOne(self, collHandle, condition, meet):
        matchCount, modifiedCount = self.mongoDB.updateOneByTag(collHandle, condition, meet)
        return modifiedCount

    def updateMany(self, collHandle, condition, meet):
        matchCount, modifiedCount = self.mongoDB.updateManyByTag(collHandle, condition, meet)
        return modifiedCount

    def insertOneOrMany(self, collHandle, docList):
        return self.mongoDB.insertMany(collHandle, docList)

    def deleteOneOrMany(self, collHandle, docList):
        for doc in docList:
            self.mongoDB.deleteMany(collHandle, doc)
        return True

    def findOneByDoc(self, collHandle, doc):
        return self.mongoDB.findOneByDoc(collHandle, doc)

    def downLoadOneCase(self, urlList, fileFolder, label):
        countOk = 0
        leftFile = []
        caseFolder = None
        for url in urlList:
            if caseFolder is None:
                caseFolder = self.getCaseFolderByURL(url, fileFolder)
                if not os.path.exists(caseFolder):
                    os.makedirs(caseFolder)
            fileName = self.getFileNameByURL(url)
            filePath = os.path.join(caseFolder, fileName)
            status = self.fileTransfer.downLoadFile(url, filePath)
            if status:
                countOk = countOk + 1
            else:
                leftFile.append(url)
        if countOk == len(urlList):
            return True, leftFile
        else:
            return False, leftFile

    def downLoad(self, limit, folder, label, isNeedUcdf):
        if os.path.exists(folder):
            pass
        else:
            os.makedirs(folder)
        collNames, collHandle, db = self.mongoDB.getCollByDB(dbName, label)
        if len(label) == 0:
            allCollCases = []
            for collName in collNames:
                res = self.mongoDB.findMany(db[collName], limit)
                allCollCases.append(res)
                if limit is None:
                    continue
                limit = limit - len(res)
                if limit == 0:
                    break
            for collCases in allCollCases:
                for oneCase in collCases:
                    if not oneCase.has_key("Resource"):
                        continue
                    urlList = oneCase["Resource"]
                    if int(isNeedUcdf) == 0:
                        removeUcdf = None
                        for url in urlList:
                            if url.find("ucdf") >= 0:
                                removeUcdf = url
                        if removeUcdf is not None:
                            urlList.remove(removeUcdf)

                    goodBad, leftFile = self.downLoadOneCase(urlList, folder, label)
        else:
            res = self.mongoDB.findMany(collHandle, limit)
            for oneCase in res:
                if not oneCase.has_key("Resource"):
                    continue
                urlList = oneCase["Resource"]
                if int(isNeedUcdf) == 0:
                    removeUcdf = None
                    for url in urlList:
                        if url.find("ucdf") >= 0:
                            removeUcdf = url
                    if removeUcdf is not None:
                        urlList.remove(removeUcdf)
                goodBad, leftFile = self.downLoadOneCase(urlList, folder, label)

    def downLoadByCaseId(self, folder, dbName, collName, caseId, isNeedUcdf):
        if os.path.exists(folder):
            pass
        else:
            os.makedirs(folder)
        collNames, collHandle, db = self.mongoDB.getCollByDB(dbName, collName)
        if collHandle is not None:
            allCollCases = []
            res = self.mongoDB.findByTag(collHandle, {"caseId": caseId})
            allCollCases.append(res)
            for collCases in allCollCases:
                for oneCase in collCases:
                    if not oneCase.has_key("Resource"):
                        continue
                    urlList = oneCase["Resource"]
                    if int(isNeedUcdf) == 0:
                        removeUcdf = None
                        for url in urlList:
                            if url.find("ucdf") >= 0:
                                removeUcdf = url
                        if removeUcdf is not None:
                            urlList.remove(removeUcdf)

                    goodBad, leftFile = self.downLoadOneCase(urlList, folder, collName)
        else:
            print("Please check your label!")

    def uploadFile(self, urlList, fileList, fileNames, label, caseId):
        countOk = 0
        leftFile = []
        for id in range(len(fileList)):
            status = self.fileTransfer.uploadFile(urlList[id], fileList[id], fileNames[id], label, caseId)
            if status:
                countOk = countOk + 1
            else:
                leftFile.append(fileList[id])
        if countOk == len(fileList):
            return True, leftFile
        else:
            return False, leftFile

    def extractIds(self, casesWithJson):
        _dataList = []
        _labels = []
        _caseIds = []
        for data in casesWithJson:
            if data is None:
                continue
            if data.has_key("label") and data.has_key("caseId"):
                _labels.append(data["label"])
                _caseIds.append(data["caseId"])
                _dataList.append(data)
        return  _dataList, _labels, _caseIds

    def getCasesDBId(self, case):
        casesOnlyJson, _casesPath = self.getCasesContentWhenDelete(case)
        _dataList, _labels, _caseIds = self.extractIds(casesOnlyJson)
        return _dataList,  _labels, _caseIds, _casesPath

    def delete(self,  dbName, sumName, handle, dataList, collNames, caseIds, casesPath, update=False):
        passCases = []
        for nameIndex in range(len(collNames)):
            res = self.mongoDB.findByTag(handle[collNames[nameIndex]], dataList[nameIndex])
            for item in res:
                urls = item["Resource"]
                for url in urls:
                    status = self.fileTransfer.deleteFile(url)
            countDelete = self.mongoDB.deleteMany(handle[collNames[nameIndex]], dataList[nameIndex])
            self.updateCaseId(dbName, sumName, collNames[nameIndex], caseIds[nameIndex])
            passRes = {"your case":casesPath[nameIndex], "label":collNames[nameIndex], "caseId":caseIds[nameIndex]}
            passCases.append(passRes)
        if not update:
            print("to delete successfully:", passCases)
        return True

    def deleteById(self, dbName, sumName, handle, label, caseId):
        passCases = []
        res = self.mongoDB.findByTag(handle, {"caseId": caseId})
        for item in res:
            urls = item["Resource"]
            for url in urls:
                status = self.fileTransfer.deleteFile(url)
        countDelete = self.mongoDB.deleteMany(handle, {"caseId": caseId})
        self.updateCaseId(dbName, sumName, label, caseId)
        passRes = {"label":label, "caseId":caseId}
        passCases.append(passRes)
        return True

    def closeDB(self):
        self.mongoDB.client.close()

class Operation:
    def __init__(self, host, port):
        self.user = UserInterface(host, port)

    def submit(self, dbName, cases, label, sumName, update=False):
        handle, allLabel, flag = self.user.getCollection(dbName, label)
        FailCase = []
        PassCase = []
        if handle is not None:
            if len(cases) == 0:
                print("You need to type the case to submit!")
            else:
                newCases = self.user.getCasesWhenSubmit(cases)
                for oneCase in newCases:
                    caseId, _, isCurrentId, isSlotId = self.user.getNewCaseId(dbName, sumName, label)
                    docList, errorJson, localPath = self.user.formatOneDoc(oneCase, label, caseId, update)
                    try:
                        insertFlag = self.user.insertOneOrMany(handle, docList)
                        if insertFlag:
                            for doc in docList:
                                res = self.user.findOneByDoc(handle, doc)
                                if res is not None:
                                    if res.has_key("_id"):
                                        del res['_id']
                                    savePath = os.path.join(localPath, ".case.json")
                                    if os.path.exists(savePath):
                                        os.remove(savePath)
                                    json.dump(res, open(savePath, 'w'), indent=4)
                            uploadFlag, leftFile = self.user.uploadCase(oneCase, label, caseId)
                            if len(leftFile) == 0:
                                passRes = {"your case": localPath, "label": label, "caseId": caseId, "result": "successfully"}
                                PassCase.append(passRes)
                            else:
                                failRes = {"your case": localPath, "result": "Fail"}
                                FailCase.append(failRes)
                                toDeleteUrl = docList[0]["Resource"]
                                for url in toDeleteUrl:
                                    status = self.user.fileTransfer.deleteFile(url)
                                self.user.deleteOneOrMany(handle, docList)
                                self.user.updateCaseId(dbName, sumName, label,  caseId)
                        else:
                            print("Submit case failed!")
                    except Exception as badError:
                        print("bad:", badError)
                        failRes = {"your case": localPath, "result": "Fail"}
                        FailCase.append(failRes)
                        self.user.deleteOneOrMany(handle, docList)
                        self.user.updateCaseId(dbName, sumName, label, caseId)
        else:
            newCases = self.user.getCasesWhenSubmit(cases)
            newHandle = self.user.creatNewLabel(dbName, label)
            for oneCase in newCases:
                caseId, _, isCurrentId, isSlotId = self.user.getNewCaseId(dbName, sumName, label)
                docList, errorJson, localPath  = self.user.formatOneDoc(oneCase, label, caseId, update)
                try:
                    insertFlag = self.user.insertOneOrMany(newHandle, docList)
                    if insertFlag:
                        for doc in docList:
                            res = self.user.findOneByDoc(newHandle, doc)
                            if res is not None:
                                if res.has_key("_id"):
                                    del res['_id']
                                savePath = os.path.join(localPath, ".case.json")
                                if os.path.exists(savePath):
                                    os.remove(savePath)
                                json.dump(res, open(savePath, 'w'), indent=4)

                        uploadFlag, leftFile = self.user.uploadCase(oneCase, label, caseId)
                        if len(leftFile) == 0:
                            passRes = {"your case": localPath, "label": label, "caseId": caseId, "result": "successfully"}
                            PassCase.append(passRes)
                        else:
                            failRes = {"your case": localPath, "result": "Fail"}
                            FailCase.append(failRes)
                            toDeleteUrl = docList[0]["Resource"]
                            for url in toDeleteUrl:
                                status = self.user.fileTransfer.deleteFile(url)
                            self.user.deleteOneOrMany(newHandle, docList)
                            self.user.updateCaseId(dbName, sumName, label, caseId)
                    else:
                        print("Submit case failed!")
                except Exception as badError:
                    failRes = {"your case": localPath, "result": "Fail"}
                    FailCase.append(failRes)
                    print("bad:", badError)
                    self.user.deleteOneOrMany(newHandle, docList)
                    self.user.updateCaseId(dbName, sumName, label, caseId)
        self.user.closeDB()
        if update:
            for passItem in PassCase:
                print("update to submit successfully:", passItem)
            for failItem in FailCase:
                print("update to submit failed:", failItem)
            if len(PassCase) == 0:
                print("no update to submit successfully!")
            if len(FailCase) == 0:
                print("no update to submit failed!")
        else:
            for passItem in PassCase:
                print("to submit successfully:", passItem)
            for failItem in FailCase:
                print("to submit failed:", failItem)
            if len(PassCase) == 0:
                print("no one to submit successfully!")
            if len(FailCase) == 0:
                print("no one to submit failed!")

    def delete(self, dbName, sumName, cases, update=False):
        dbHandle = self.user.getDBHandle(dbName)
        dataList, labels, caseIds, casesPath = self.user.getCasesDBId(cases)
        self.user.delete(dbName, sumName, dbHandle, dataList, labels, caseIds, casesPath, update)
        self.user.closeDB()

    def deleteByCaseId(self, dbName, sumName, label, caseId):
        handle, _, _ = self.user.getCollection(dbName, label)
        if handle is None:
            print("Please check your label!")
        else:
            self.user.deleteById(dbName, sumName, handle, label, caseId)
            self.user.closeDB()
            print("Your case has been deleted!")

    def update(self, dbName, sunName,  cases, label, update):
        self.delete(dbName, sumName, cases, update)
        self.submit(dbName, cases, label, sumName, update)

    def download(self, dbName, limit, mylocal, label, isNeedUcdf):
        currentFile = os.path.abspath(__file__)
        currentFolder = os.path.join(os.path.dirname(currentFile), str(int(time.time() * 100)))
        if len(mylocal) != 0:
            currentFolder = mylocal
        self.user.downLoad(limit, currentFolder, label, isNeedUcdf)

    def downloadById(self, dbName, caseId, mylocal, label, isNeedUcdf):
        currentFile = os.path.abspath(__file__)
        currentFolder = os.path.join(os.path.dirname(currentFile), str(int(time.time() * 100)))
        if len(mylocal) != 0:
            currentFolder = mylocal
        self.user.downLoadByCaseId(currentFolder, dbName, label, caseId, isNeedUcdf)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("-submit", type=int, default=0)
    parser.add_argument("-update", type=int, default=0)
    parser.add_argument("-download", type=int, default=0)
    parser.add_argument("-delete", type=int, default=0)
    parser.add_argument("-limit", type=int, default=0)
    parser.add_argument("-ucdf", type=int, default=0)
    parser.add_argument("-caseId", type=int, default=-1)
    parser.add_argument("-label", type=str, default="")
    parser.add_argument("-case", type=str, default="")
    parser.add_argument("-mylocal", type=str, default="")
    args = parser.parse_args()

    host = "10.0.195.159"
    port = 27017
    dbName = "Prediction"
    sumName = "sum"

    myOperation = Operation(host, port)

    Tips = True
    # submit cases
    # 1, check no json
    # 2, file listing, including rmap, hmap, ucdf etc
    # 3, construct json, including url for rmap, hmap, ucdf, cases etc
    if int(args.submit) == 1:
        Tips = False
        if len(str(args.label)) == 0:
            handle, allLabel, flag = myOperation.user.getCollection(dbName, None)
            if sumName in allLabel:
                allLabel.remove(sumName)
            print("Chose your label:", allLabel, "!")
            print("Also you can type new label for submitting!")
        else:
            if str(args.label) == "sum":
                print("Label cannot be named to \"sum\"!")
            else:
                myOperation.submit(dbName, str(args.case), str(args.label), sumName)

    # update cases
    # 1, check json
    # 2, update operation
    if int(args.update) == 1:
        Tips = False
        if len(args.label) == 0:
            print("You need to type the label to update!")
        if len(args.case) == 0:
            print("You need to type the case to update!")
        if len(args.label) != 0 and len(args.case) != 0:
            update = True
            if str(args.label) == "sum":
                print("Label cannot be named to \"sum\"!")
            else:
                myOperation.update(dbName, sumName, args.case, args.label, update)

    # download cases
    # 1, check json
    # 2, downloading cases or resources
    if int(args.download) == 1:
        Tips = False
        if int(args.caseId) != -1:
            myOperation.downloadById(dbName, args.caseId, args.mylocal, args.label, args.ucdf)
        else:
            if int(args.limit) == 0:
                print("You need to type the number cases for downloading!")
            else:
                if int(args.limit) == -1:
                    args.limit = None
                myOperation.download(dbName, args.limit, args.mylocal, args.label, args.ucdf)

    # delete cases
    # 1, check json
    # 2, get url and delete cases
    if int(args.delete) == 1:
        Tips = False
        if args.caseId != -1:
            if len(args.label) == 0:
                print("You need to type the label to delete!")
            else:
                myOperation.deleteByCaseId(dbName, sumName, args.label, args.caseId)
        else:
            if len(args.case) == 0:
                print("You need to type the case for deleting!")
            if len(args.case) != 0:
                myOperation.delete(dbName, sumName,  args.case)
    if Tips:
        print("Not right operation! Please check your input!")
