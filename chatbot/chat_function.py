import re
import torch
import numpy as np
import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        return json.load(file)

    
def load_text(path):
    with open(path , 'r' , encoding='utf-8') as f:
        data = f.read().split('\n')
        return data
        

def clean_text(txt):
    txt = txt.lower()
    txt = re.sub(r"\u200b", " ", txt)
    txt = re.sub(r"'", " ", txt)
    txt = re.sub(r'"', " ", txt)
    txt = re.sub(r'v.v.', " ", txt)
    txt = re.sub(r"[^\w\s]", " ", txt)
    txt = re.sub(r"_", " ", txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

def check_len(text , max_len):
    if len(text) > max_len:
        return text[:max_len-2]
    return text
    





def create_masks(eng_batch, kn_batch , max_sequence_length):
    NEG_INFTY = -1e9
    num_sentences = len(eng_batch)
    look_ahead_mask = torch.full([max_sequence_length, max_sequence_length] , True)
    look_ahead_mask = torch.triu(look_ahead_mask, diagonal=1)
    encoder_padding_mask = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)
    decoder_padding_mask_self_attention = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)
    decoder_padding_mask_cross_attention = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)

    for idx in range(num_sentences):
        eng_sentence_length, kn_sentence_length = len(eng_batch[idx]), len(kn_batch[idx])
        eng_chars_to_padding_mask = np.arange(eng_sentence_length + 1, max_sequence_length)
        kn_chars_to_padding_mask = np.arange(kn_sentence_length + 1, max_sequence_length)
        encoder_padding_mask[idx, :, eng_chars_to_padding_mask] = True
        encoder_padding_mask[idx, eng_chars_to_padding_mask, :] = True
        decoder_padding_mask_self_attention[idx, :, kn_chars_to_padding_mask] = True
        decoder_padding_mask_self_attention[idx, kn_chars_to_padding_mask, :] = True
        decoder_padding_mask_cross_attention[idx, :, eng_chars_to_padding_mask] = True
        decoder_padding_mask_cross_attention[idx, kn_chars_to_padding_mask, :] = True

    encoder_self_attention_mask = torch.where(encoder_padding_mask, NEG_INFTY, 0)
    decoder_self_attention_mask =  torch.where(look_ahead_mask + decoder_padding_mask_self_attention, NEG_INFTY, 0)
    decoder_cross_attention_mask = torch.where(decoder_padding_mask_cross_attention, NEG_INFTY, 0)
    return encoder_self_attention_mask, decoder_self_attention_mask, decoder_cross_attention_mask
    
    
def predict(model , ques_sentence , max_sequence_length ,index_to_vi, device):
    model.eval()
    with torch.no_grad():
        ques_sentence = clean_text(ques_sentence)
        ques_sentence = check_len(ques_sentence , 300)
        ques_sentence = (ques_sentence,)
        ans_sentence = ("",)
        for word_counter in range(max_sequence_length):
            encoder_self_attention_mask, decoder_self_attention_mask, decoder_cross_attention_mask= create_masks(ques_sentence, ans_sentence , max_sequence_length)
            predictions = model(ques_sentence,
                                      ans_sentence,
                                      encoder_self_attention_mask.to(device), 
                                      decoder_self_attention_mask.to(device), 
                                      decoder_cross_attention_mask.to(device),
                                      enc_start_token=False,
                                      enc_end_token=False,
                                      dec_start_token=True,
                                      dec_end_token=False)
            next_token_prob_distribution = predictions[0][word_counter]
            next_token_index = torch.argmax(next_token_prob_distribution).item()
            next_token = index_to_vi[next_token_index]
            if next_token == index_to_vi[2]:
                break
            ans_sentence = (ans_sentence[0] + next_token, )

        return ans_sentence[0]

