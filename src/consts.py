"""
consts used throughout the project
"""
CONTEXT_ANSWER_SEP = "|||"
CONTEXT_PREFIX = "Context: "
NUMBERED_CONTEXT_PREFIX = "Context"
FOLLOW_UP_PREFIX = "Follow up: "
KNOWLEDGE_FOLLOW_UP_PREFIX = "Knowledge Follow up: "
REASONING_FOLLOW_UP_PREFIX = "Reasoning Follow up: "
FINAL_ANSWER_PREFIX = "So the final answer is: "
INTERMEDIATE_ANS_PREFIX = "Intermediate answer: "
QUESTION_PREFIX = "Question: "
CALL_API = True
POSITIVE_PREFIX = "Positive: "
NEGATIVE_PREFIX = "Negative: "
STOP_TOKEN = "\n#"
SELF_ASK_ANSWER = "So the final answer is: "
FACTOID_ANSWER_PREFIX = "A: "
LOGGING_NAME = "logger"

# mte
FULL_MTE_FIELD = "multi_trace_entailment_full"
PRED_MTE_FIELD = "multi_trace_entailment_prediction"
ACC_MTE_FIELD = "acc@mte"
NUM_EXAMPLES_FIELD = "num_examples"
NUM_ABSTAINS_FIELD = "num_abstains"

# accuracy feilds
ACC_AT_1_FIELD = "acc@1"
ACC_AT_3_FIELD = "acc@3"
ACC_AT_MAJORITY_FIELD = "acc@majority"
