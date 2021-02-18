from db import DatabaseManager


class ServiceManager:

    def __init__(self):
        self.manager = DatabaseManager()
        self.matrix = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D',
                       'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M',
                       'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'x', 'X', 'y', 'Y',
                       'z', 'Z']

    def encode(self, url: str) -> str:
        success, code = self.manager.find_url(url)

        if success:
            return self.code_truncate(code)

        else:
            raw_code = self.manager.get_last_code()+1
            code = self.code_truncate(raw_code)
            self.manager.save_code(url, raw_code)
            return code

    def decode(self, truncated_code: str) -> (bool, str):
        success, code = self.code_restore(truncated_code)
        if success:
            success, url = self.manager.find_code(code)
            if success:
                return True, url

        return False, None

    def code_truncate(self, code: int) -> str:

        result = str()
        power = 0
        tmp = code
        length = len(self.matrix)
        while tmp > length - 1:
            tmp = tmp / (length - 1)
            power += 1

        while power > 0:
            tmp = int(code / ((length - 1) ** power))
            result += self.matrix[tmp]
            code = code - (tmp * (length - 1) ** power)
            power -= 1

        result += self.matrix[code]

        return result

    def code_restore(self, hash: str) -> (bool, int):
        hash = str(hash)
        result = 0
        length = len(self.matrix)
        try:
            for i in range(0, len(hash)):
                value = self.matrix.index(hash[i])
                result += value * (length-1) ** (len(hash)-1-i)

            return True, result

        except ValueError:
            return False, None
