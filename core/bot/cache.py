from core.bot import Logging as Logging
from config import cache_file
import arrow, json, os

class Cache():
    def __init__(self):
        self.logger = Logging.get_logger(name="cache")
        self.logger.debug("cache started!")
        self.file = cache_file
        # initiating cache and trying to create the folder
        try:
            os.mkdir(self.file)
            self.logger_info(f"Created dir \"{self.file}\"")
        except OSError:
            self.logger.debug(f"cache file not created: File already exists")
    # function to load json cache from cache file
    async def _load_from_file(self):
        self.logger.debug("attempting to load from cache file ...")
        with open(self.file,"r") as cache:
            try:
                data = json.load(cache)
                self.logger.info("Seccuessfully loaded from cache file")
                self.logger.debug(f"Cache file length: {len(data)}")
            except json.decoder.JSONDecodeError:
                self.logger.info("Cache file empty")
                data = {}
            return True
        self.logger.error(f"failed to load the cache from file {self.file}")
        return False
    # function to save to the cache file
    async def _save_to_file():
        with open(self.file,'w') as cache:
            json.dump(self.data,cache)
            self.logger.debug("Saved to cache file")
            return True
        self.logger.warning("Error in cache while saving to cache file")
    # function to save the key value pairs
    async def save(self,key,value):
        self.data[key]=value
        self.logger.debug(f"{key} with the value {value} was saved to cache")
        self._save_to_file()
    # function to get value of key
    async def get(key):
        req = None
        # if there is not variable data yet wait load of file function
        if not self.data: await self._load_from_file()
        try:
            req = self.data[key]
            self.logger.debug(f"requested: {req}")
        except KeyError:
            self.logger.info(f"requested key: \"{key}\" not found")
        return req
    # function to delete value from data
    async def delete(self,key):
        try:
            self.logger.debug(f"delted {key} with value {self.data[key]}")
            req = self.data.pop(key,None)
        except KeyError:
            self.logger.info(f"Deletion of key \"{key}\" not succesfull. key not found")
        return req