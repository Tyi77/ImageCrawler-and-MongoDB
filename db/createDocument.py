def create_document(_id: int, name: str, hsv_aver: float, gray_code: float) -> dict:
    result = {
        '_id': _id,
        'name': name,
        'hsv_aver': hsv_aver,
        'gray_code': gray_code
    }

    return result

def create_document_list(_id_list: list, name_list: list, hsv_aver_list: list, gray_code_list: list) -> list:
    result = []
    for _id, name, hsv_aver, gray_code in zip(_id_list, name_list, hsv_aver_list, gray_code_list):
        result.append({
            '_id': _id,
            'name': name,
            'hsv_aver': hsv_aver,
            'gray_code': gray_code
        })
    
    return result