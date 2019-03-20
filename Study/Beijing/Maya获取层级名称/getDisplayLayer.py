def getDisplayLayers():
        import maya.cmds as cmds
        self._cmds = cmds
        """
        get sence display layers
        :return: []
        """
        all_layers = self._cmds.ls(type="displayLayer")
        layers = [i for i in all_layers if "defaultLayer" not in i and ":" not in i]
        return layers
