from game.config import BASE_SCORE, COMBO_BONUS

class GameLogic:
    def __init__(self, mode):
        self.mode = mode
        self.combo = 0
        self.max_combo = 0  # 历史最大 combo
        self.score = 0

    def check_match(self, card1_info, card2_info):
        """判断两张卡片是否匹配"""
        type1, pair_id1 = card1_info["type"], card1_info["pair_id"]
        type2, pair_id2 = card2_info["type"], card2_info["pair_id"]

        if self.mode == "A-A":
            return type1 == "A" and type2 == "A" and pair_id1 == pair_id2
        elif self.mode == "B-B":
            return type1 == "B" and type2 == "B" and pair_id1 == pair_id2
        else:  # A-B
            return pair_id1 == pair_id2 and (
                (type1 == "A" and type2 == "B") or (type1 == "B" and type2 == "A")
            )

    def on_success(self):
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        self.score += BASE_SCORE + COMBO_BONUS * (self.combo - 1)
        return self.combo, self.score

    def on_fail(self):
        self.combo = 0  # 重置当前 combo，但保留 max_combo

    def reset(self):
        self.combo = 0
        self.max_combo = 0
        self.score = 0