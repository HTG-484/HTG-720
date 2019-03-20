def getAllReferences(self):
        '''2018.01.18 change '''
        result = []
        allRN =  self._cmds.ls(rf=True)
        
        if 'sharedReferenceNode' in allRN:
            allRN.remove('sharedReferenceNode')
        for rn in allRN:
            #print "rn:",rn
            refPath = self._cmds.referenceQuery(rn,filename=True)
            namespace = self._cmds.referenceQuery(rn,namespace=True)
            if namespace[0]==':':
                namespace = namespace[0:]

            info = {'node':rn,
                    'ref_path': refPath,
                    'path':refPath,
                    'name':rn,
                    'namespace': namespace
                    }
            result.append(info)
            
        return result
