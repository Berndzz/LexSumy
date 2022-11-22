from rouge import Rouge


def evaluate(sum, raw):
    r = Rouge()
    r_score = r.get_scores(sum, raw)
    return r_score

# Note: "f" stands for f1_score, "p" stands for precision, "r" stands for recall.
