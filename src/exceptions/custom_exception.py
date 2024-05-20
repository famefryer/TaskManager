class EntityNotFoundException(Exception):
    def __init__(self, entity: str, id: str, col_name: str = 'ID'):
        self.message = f'{entity} with {col_name}({id}) does not exist'
        super().__init__(self.message)
        
class BadRequestException(Exception):
    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(msg)
        
class EntityAlreadyExistException(Exception):
    def __init__(self, entity: str, unq_col: str, id: str):
        self.message = f'{entity} with {unq_col}({id}) already exists'
        super().__init__(self.message)
