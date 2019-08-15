class Presentation:
    def __init__(self, uuid, pages=[]):
        self.uuid = uuid
        self.pages = pages

    # TODO
    def addPage(self, page, index=0):
        self.pages.insert(
            index, page) if index >= 0 else self.pages.append(page)

    # TODO
    def deletePage(self, index):
        del self.pages[index]

    # TODO
    def getPage(self, index):
        return self.pages[index]

    # TODO
    def exportPresentation(self):
        return
