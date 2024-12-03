import json, pygame

class Tile():
    def __init__(self,x,y,img):
        self.x = x*16*3
        self.y = y*16*3
        self.img = img

class TileLoader():
    def __init__(self, file, tileset):
        self.tilelist = []
        self.tileset = []

        self.tilesetImage = pygame.image.load(tileset).convert()
        x=0

                    #load tileset

        for i2 in range(4):
            for i in range(9):
                fragment_rect = pygame.Rect(i*16, i2*16, 16, 16)
                fragment = self.tilesetImage.subsurface(fragment_rect)
                scaled_fragment = pygame.transform.scale(fragment, (16*3, 16*3))
                self.tileset.append(scaled_fragment)


        with open(file, 'r') as f: #load tilemap
            self.data = json.load(f)
            f.close()
            x=0
            for rows in range(self.data['layers']['height']):
                for columns in range(self.data['layers']['width']):
                    if int(self.data['layers']['data'][x]) > 0:
                        newTile = Tile(columns,rows, self.tileset[int(self.data['layers']['data'][x])-1])
                        self.tilelist.append(newTile)
                    x += 1

    def loadMap(self):
        return self.tilelist