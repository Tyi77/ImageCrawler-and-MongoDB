def create_document(_id: int, url: str, colorAnalysis: float, structureAnalysis: float) -> dict:
    result = {
        '_id': _id,
        'url': url,
        'colorAnalysis': colorAnalysis,
        'structureAnalysis': structureAnalysis
    }

    return result

def create_document_list(_idList: list, urlList: list, colorAnalysisList: list, structureAnalysisList: list) -> list:
    result = []
    for _id, url, colorAnalysis, structureAnalysis in zip(_idList, urlList, colorAnalysisList, structureAnalysisList):
        result.append({
             '_id': _id,
            'url': url,
            'colorAnalysis': colorAnalysis,
            'structureAnalysis': structureAnalysis
        })
    
    return result