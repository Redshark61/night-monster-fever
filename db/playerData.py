from db.db import Database
from db.player import Player
from db.difficulty import Difficulty


class PlayerData:

    modelList = []
    playerID = None

    def __init__(self, player):
        self.player = player
        self.updateValue()
        self.playerDB = Player(self)

    def addToList(self):
        PlayerData.modelList.append(self)
        self.playerDB.addNewPlayer()
        self.addPlayer()

    def __str__(self) -> str:
        return f"{self.playerName=} - {self.health=} - {self.xp=} - {self.level=} - {self.position=} - {self.currentMap=} - {self.difficultyName=} - {self.spritePath=}"

    def addPlayer(self):
        results = Database.query(f"""
        SELECT player.id FROM player WHERE player.spritepath = '{self.spritePath}' and player.name = '{self.playerName}'
        """)
        PlayerData.playerID = results[0][0]
        # playerID = [player.id for player in Player.modelList if player.playerName == self.playerName][0]
        query = f"""INSERT INTO playerdata (playerid, health, xp, level, positionx, positiony, currentmap, difficultyid, maxhealth)
                    VALUES ('{int(PlayerData.playerID)}','{self.health}', '{self.xp}', '{self.level}', '{self.position[0]}', '{self.position[1]}', '{self.currentMap}', '{self.difficultyID}', '{self.maxHealth}')"""
        Database.query(query)

    def updateValue(self):
        self.health = int(self.player.health)
        self.maxHealth = int(self.player.maxHealth)
        self.xp = self.player.totalXP
        self.level = self.player.currentLevel
        self.position = (self.player.rect.x, self.player.rect.y)
        self.currentMap = self.player.map
        self.difficultyID = 1
        self.playerName = self.player.playerName
        self.spritePath = self.player.name
        self.difficultyName = [difficulty.name for difficulty in Difficulty.modelList if difficulty.ID == self.difficultyID][0]
        if PlayerData.playerID is not None:
            self.updateDB()

    def updateDB(self):
        query = f"""
        UPDATE playerdata 
        SET health = '{self.health}', xp = '{self.xp}', 
        level = '{self.level}', positionx = '{self.position[0]}', positiony = '{self.position[1]}', 
        currentmap = '{self.currentMap}', difficultyid = '{self.difficultyID}',
        maxhealth = '{self.maxHealth}'
        WHERE playerid = '{PlayerData.playerID}'"""
        Database.query(query)

    @staticmethod
    def upload(player, choice):
        query = """SELECT * FROM playerdata"""
        result = Database.query(query)[choice]
        PlayerData.playerID = result[0]
        player.health = result[1]
        player.totalXP = result[2]
        player.currentLevel = result[3]
        player.rect.x = result[4]
        player.rect.y = result[5]
        player.map = result[6]
        player.maxHealth = result[8]

    @staticmethod
    def getSpritePath(choice):
        query = """SELECT spritepath FROM player"""
        result = Database.query(query)[choice]
        return result[0]

    @staticmethod
    def setCurrentMap(map):
        query = f"""SELECT currentmap FROM playerdata WHERE playerid = '{PlayerData.playerID}'"""
        results = Database.query(query)[0][0]
        map.currentMap = results