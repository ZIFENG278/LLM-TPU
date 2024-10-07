import argparse
import time
from transformers import AutoTokenizer
import time
import json
import torch
import numpy as np
import argparse
from PIL import Image
import torchvision 
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode

def load_image(image_file, image_size=1120):
    image = Image.open(image_file).convert('RGB')
    transform = transforms.Compose(
                [
                    transforms.Resize(
                        (image_size, image_size), interpolation=transforms.InterpolationMode.BICUBIC
                    ),
                    transforms.ToTensor(),
                    transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
                ]
            )
    
    # images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = transform(image)
    pixel_values = torch.stack(pixel_values)
    return pixel_values


class ChatGLM():
    def __init__(self, args):
        # preprocess parameters, such as prompt & tokenizer
        # parameters
        self.EOS = None
        self.SEQLEN = None
        self.input_str = ""
        self.system_prompt = ""

        # devid
        self.devices = [int(d) for d in args.devid.split(",")]

        # load tokenizer
        print("Load " + args.tokenizer_path + " ...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            args.tokenizer_path, trust_remote_code=True
        )

        # warm up
        self.tokenizer.decode([0])
        print("Done!")
        self.history = []
        self.EOS = [self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|user|>"), self.tokenizer.convert_tokens_to_ids("<|observation|>")]
        self.enable_history = args.enable_history

        # load model
        self.load_model(args)
    
    def chat(self):
        """
        Start a chat session.
        """
        # check
        if not self.EOS:
            raise NotImplementedError("Forget to set End of Sentence Token Id(EOS)")
        if not self.SEQLEN:
            raise NotImplementedError("Forget to set End of Sentence Token Id")

        # Instruct
        print(
            """\n===========================================================
1. If you want to quit, please enter one of [q, quit, exit]
2. To create a new chat session, please enter one of [clear, new]
==========================================================="""
        )
        # Stop Chatting with "exit" input
        while True:
            self.input_str = input("\nQuestion: ")
            # Quit
            if self.input_str in ["exit", "q", "quit"]:
                break
            # New Chat
            elif self.input_str in ["clear", "new"]:
                self.clear()
            # Chat
            else:
                tokens = self.encode_tokens()

                # check tokens
                if not tokens:
                    print("Sorry: your question is empty!!")
                    return
                if len(tokens) > self.SEQLEN:
                    print(
                        "The maximum question length should be shorter than {} but we get {} instead.".format(
                            self.SEQLEN, len(tokens)
                        )
                    )
                    return

                print("\nAnswer: ", end="")
                self.stream_answer(tokens)

    def stream_answer(self, tokens):
        """
        Stream the answer for the given tokens.
        """
        tok_num = 0
        self.answer_cur = ""
        self.answer_token = []

        # Image information
        
        IMAGE_SIZE = 1120
        PATCH_SIZE = 14
        pixel_values = load_image('../demo.jpg', image_size=IMAGE_SIZE)
        num_patches = int(IMAGE_SIZE // PATCH_SIZE // 2) ** 2
        # num_image_token = int((IMAGE_SIZE // PATCH_SIZE) ** 2)
        num_image_token = num_patches


        # First token
        first_start = time.time()
        token = self.model.forward_first(tokens)
        first_end = time.time()
        # Following tokens
        full_word_tokens = []
        while token not in self.EOS and self.model.token_length < self.SEQLEN:
            full_word_tokens.append(token)
            word = self.tokenizer.decode(full_word_tokens, skip_special_tokens=True)
            if "�" not in word:
            # if len(word) > 0 and "�" != word[-1]:
                print(word, flush=True, end="")
                full_word_tokens = []
            # print(token)
            self.answer_token += [token]
            tok_num += 1
            token = self.model.forward_next()
        self.answer_cur = self.tokenizer.decode(self.answer_token)
        
        # counting time
        next_end = time.time()
        first_duration = first_end - first_start
        next_duration = next_end - first_end
        tps = tok_num / next_duration

        if self.enable_history:
            self.update_history()
        else:
            self.clear()

        print()
        print(f"FTL: {first_duration:.3f} s")
        print(f"TPS: {tps:.3f} token/s")


    ## For Web Demo
    def stream_predict(self, query):
        """
        Stream the prediction for the given query.
        """
        self.answer_cur = ""
        self.input_str = query
        tokens = self.encode_tokens()

        for answer_cur, history in self._generate_predictions(tokens):
            yield answer_cur, history

    def _generate_predictions(self, tokens):
        """
        Generate predictions for the given tokens.
        """
        # First token
        next_token = self.model.forward_first(tokens)
        output_tokens = [next_token]

        # Following tokens
        while True:
            next_token = self.model.forward_next()
            if next_token in self.EOS:
                break
            output_tokens += [next_token]
            self.answer_cur = self.tokenizer.decode(output_tokens)
            if self.model.token_length >= self.SEQLEN:
                self.update_history()
                yield self.answer_cur + "\n\n\nReached the maximum length; The history context has been cleared.", self.history
                break
            else:
                yield self.answer_cur, self.history

        self.update_history()

    def load_model(self, args):
        import chat
        self.model = chat.ChatGLM()
        self.model.init(self.devices, args.model_path)
        self.model.temperature = args.temperature
        self.model.top_p = args.top_p
        self.model.repeat_penalty = args.repeat_penalty
        self.model.repeat_last_n = args.repeat_last_n
        self.model.max_new_tokens = args.max_new_tokens
        self.model.generation_mode = args.generation_mode
        self.model.prompt_mode = args.prompt_mode
        self.SEQLEN = self.model.SEQLEN

    def clear(self):
        self.history = []

    def update_history(self):
        if self.model.token_length >= self.SEQLEN:
            print("... (reach the maximal length)", flush=True, end="")
            self.history = []
        else:
            self.history.append({"role": "assistant", "content": self.answer_cur})

    def encode_tokens(self):
        self.history.append({"role": "user", "content": self.input_str})
        tokens = self.tokenizer.apply_chat_template(self.history, add_generation_prompt=True)[0]
        return tokens


def main(args):
    model = ChatGLM(args)
    model.chat()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model_path', default='../compile/glm4v-9b_int4_1dev.bmodel', type=str, help='path to the bmodel file')
    parser.add_argument('-t', '--tokenizer_path', type=str, default="../token_config", help='path to the tokenizer file')
    parser.add_argument('-d', '--devid', type=str, default='1', help='device ID to use')
    parser.add_argument('--temperature', type=float, default=1.0, help='temperature scaling factor for the likelihood distribution')
    parser.add_argument('--top_p', type=float, default=1.0, help='cumulative probability of token words to consider as a set of candidates')
    parser.add_argument('--repeat_penalty', type=float, default=1.0, help='penalty for repeated tokens')
    parser.add_argument('--repeat_last_n', type=int, default=32, help='repeat penalty for recent n tokens')
    parser.add_argument('--max_new_tokens', type=int, default=1024, help='max new token length to generate')
    parser.add_argument('--generation_mode', type=str, choices=["greedy", "penalty_sample"], default="greedy", help='mode for generating next token')
    parser.add_argument('--prompt_mode', type=str, choices=["prompted", "unprompted"], default="prompted", help='use prompt format or original input')
    parser.add_argument('--enable_history', action='store_true', help="if set, enables storing of history memory")
    args = parser.parse_args()
    main(args)
