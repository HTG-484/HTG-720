def checkRefVersion(self):
        result = []
        allRef = self._software.getAllReferences()
        versionMatch = '(?<=/)v\d{3}(?=/)'
        
        for r in allRef:
            
            s = re.search(versionMatch,r['path'])
            if s:
                
                version = s.group()
                
                versionFolder = r['path'].split('/%s/'%version)[0]
                
                versionList = os.listdir(versionFolder)
                
                versionList = sorted(versionList)
                
                maxVersion = max(versionList)
                if version != maxVersion:
                    print r['node'],"--->",r['ref_path']
                    result.append(r['ref_path'])
        if result:
            return u'have highter version file\n,please open reference Editor!'
        return result
#------------------------------------------------------------------------
getShapeNum(num=1,compare='GreaterThan')
def getShapeNum(self,num=0,compare=''):
        #Greater than, less than ,Equal to
        Allobj = self._cmds.ls(dag = 1,type = 'transform',long=True)
        Defult = ['|persp','|top','|front','|side']
        shapes = [i for i in Allobj if i not in Defult]
        result = []
        
        for i in shapes:
            children = self._cmds.listRelatives(i , children = True,type='mesh')
            if not children:
                continue
            #print children
            if compare == 'GreaterThan':
                if len(children) > num:
                    result.append(i)
            elif compare == 'LessThan':
                if len(children) < num:
                    result.append(i)
            elif compare == 'EaualTo':
                if len(children) == num:
                    result.append(i)
        return result