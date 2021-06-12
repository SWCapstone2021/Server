import warnings
import sys, os

import torch
from torch.utils.data import DataLoader
from transformers import (
    BertForQuestionAnswering,
    BertTokenizer,
    squad_convert_examples_to_features
)
from transformers.data.processors.squad import SquadResult


from .my_squad_metrics import (
    compute_predictions_logits,
)

from .utils import SquadExample

warnings.filterwarnings('ignore')

args = {
    'max_seq_length': 512,
    'doc_stride': 128,
    'max_query_length': 64,
    'max_answer_length': 30,
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',
}


@torch.no_grad()
def evaluate(model, tokenizer, question, context):
    dataset, examples, features = make_example(tokenizer, question, context)

    # Note that DistributedSampler samples randomly
    eval_dataloader = DataLoader(dataset, batch_size=1)

    all_results = []

    for batch in eval_dataloader:
        model.eval()
        batch = tuple(t.to(args['device']) for t in batch)

        inputs = {
            "input_ids": batch[0],
            "attention_mask": batch[1],
            "token_type_ids": batch[2],
        }

        example_indices = batch[3]
        outputs = model(**inputs)

        for i, example_index in enumerate(example_indices):
            eval_feature = features[example_index.item()]
            unique_id = int(eval_feature.unique_id)

            output = [outputs[0][i].detach().cpu().tolist(), outputs[1][i].detach().cpu().tolist()]
            start_logits, end_logits = output[0], output[1]
            result = SquadResult(unique_id, start_logits, end_logits)

            all_results.append(result)

    predictions = compute_predictions_logits(
        all_examples=examples,
        all_features=features,
        all_results=all_results,
        n_best_size=20,
        max_answer_length=args['max_answer_length'],
        do_lower_case=False,
        null_score_diff_threshold=0.0,
        tokenizer=tokenizer,
    )

    answers = interest_of_test(predictions)

    return answers


def interest_of_test(predictions, threshold=0.7, min_threshold=0.3, top_count=5, highest_count=10):
    answers = list()
    top_answer = list()

    for i, pred in enumerate(predictions):
        text, prob, _, _ = pred.values()
        if i < top_count:
            top_answer.append((text, float(prob)))
        if float(prob) > threshold:
            answers.append(text)

    if len(answers) == 0:
        answers.clear()
        for answer in top_answer:
            if answer[1] > min_threshold:
                answers.append(answer[0])
        return answers

    if len(answers) > highest_count:
        return answers[:highest_count]

    return answers


def make_example(tokenizer, question, context):
    example = SquadExample(0, question, context)
    examples = [example]

    features, dataset = squad_convert_examples_to_features(
        examples=examples,
        tokenizer=tokenizer,
        max_seq_length=args['max_seq_length'],
        doc_stride=args['doc_stride'],
        max_query_length=args['max_query_length'],
        is_training=False,
        return_dataset="pt",
        threads=1,
        tqdm_enabled=False,
    )

    return dataset, examples, features


def main():
    model_path = 'models'
    model_class = BertForQuestionAnswering
    model = model_class.from_pretrained(model_path)
    model.to(args['device'])

    tokenizer_class = BertTokenizer
    tokenizer = tokenizer_class.from_pretrained(model_path, do_lower_case=False, cache_dir=None)

    result = evaluate(model, tokenizer)

    print(result)


if __name__ == "__main__":
    main()
