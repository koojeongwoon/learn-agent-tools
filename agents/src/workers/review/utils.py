from .models import ReviewScore

def compute_total(score: ReviewScore, has_research: bool) -> float:
    """항목별 점수의 가중 평균을 계산합니다."""
    if has_research and score.faithfulness is not None:
        values = [score.relevance, score.completeness, score.accuracy, score.tone, score.faithfulness]
    else:
        values = [score.relevance, score.completeness, score.accuracy, score.tone]
    return round(sum(values) / len(values), 2)


def scores_to_dict(score: ReviewScore, total: float) -> dict:
    """ReviewScore를 로깅/상태 저장용 딕셔너리로 변환합니다."""
    result = {
        "relevance": score.relevance,
        "completeness": score.completeness,
        "accuracy": score.accuracy,
        "tone": score.tone,
        "total": total,
    }
    if score.faithfulness is not None:
        result["faithfulness"] = score.faithfulness
    return result
