import re

def clean_text1(text, i):
            # ■ 제거
            text = text.replace("■", "")
            if i in [1,2]:
                pass
            else:
                # 페이지 제거
                text = re.sub(r"\d+\s*노무관리\s가이드\s북", "", text)
                
                text = re.sub(r"1\.\s*근로조건\s서면명시\s*\d+", "", text)
                text = re.sub(r"2\.\s*근로자\s명부\s및\s계약서류\s보존\s*\d+", "", text)
                text = re.sub(r"3\.\s*임금\s등\s각종\s금품\s지급\s*\d+", "", text)
                text = re.sub(r"4\.\s*근로시간\s및\s연장근로\s한도\s위반\s*\d+", "", text)
                text = re.sub(r"5\.\s*휴게시간\s부여\s*\d+", "", text)
                text = re.sub(r"6\.\s*유급휴일\s부여\s*\d+", "", text)
                text = re.sub(r"7\.\s*연차유급휴가\s부여\s*\d+", "", text)
                text = re.sub(r"8\.\s*연소자와\s모성\s보호\s*\d+", "", text)
                text = re.sub(r"9\.\s*취업규칙s*\d+", "", text)
                text = re.sub(r"10\.\s*퇴직급여\s지급\s*\d+", "", text)
                text = re.sub(r"11\.\s*직장\s내\s괴롭힘\s예방\s*\d+", "", text)
                text = re.sub(r"12\.\s*최저임금\s준수\s*\d+", "", text)
                text = re.sub(r"13\.\s*직장\s내\s성희롱\s예방\s*\d+", "", text)
                text = re.sub(r"14\.\s*고용상\s성차별\s금지\s*\d+", "", text)
                text = re.sub(r"15\.\s*비정규직\s차별\s금지\s*\d+", "", text)
                text = re.sub(r"16\.\s*노사협의회\s설치·운영\s*\d+", "", text)

            return text

        
def clean_text2(text, i):
    if i == 0:
        first_index = text.find("근로기준법")
        if first_index != -1:
            # 처음 '근로기준법'은 남겨두고, 나머지 부분에서 모두 제거
            before = text[:first_index + len("근로기준법")]
            after = text[first_index + len("근로기준법"):].replace("근로기준법", "")
            text = before + after
    
    else:
        text = re.sub(r'\s*근로기준법\s*', '', text)

    text = re.sub(r"법제처\s*\d+\s*국가법령정보센터", '', text)

    return text


def clean_text3(text, i):
    text =  re.sub(r'\s*-\s*\d+\s*-\s*', ' ', text)
    
    return text