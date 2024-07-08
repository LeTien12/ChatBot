from chatbot.chat_function import predict  ,load_json
from chatbot.chat_class import Transformer
import torch





model_path = 'chatbot/dataset/chatbot.pt'

vocab = ['PADDING', 'START', 'END', ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'à', 'á', 'â', 'ã', 'è', 'é', 'ê', 'ì', 'í', 'î', 'ò', 'ó', 'ô', 'õ', 'ù', 'ú', 'ý', 'ă', 'đ', 'ĩ', 'ũ', 'ơ', 'ư', 'ạ', 'ả', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'ẹ', 'ẻ', 'ẽ', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'ỉ', 'ị', 'ọ', 'ỏ', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ', 'ụ', 'ủ', 'ứ', 'ừ', 'ử', 'ữ', 'ự', 'ỳ', 'ỵ', 'ỷ', 'ỹ']


index_to_vi = {k:v for k,v in enumerate(vocab)}
vi_to_index = {v:k for k,v in enumerate(vocab)}


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        
d_model = 512
ffn_hidden = 2048
num_heads = 8
drop_prob = 0.1
num_layers = 1
max_sequence_length = 300
vocab_size = len(index_to_vi)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
START_TOKEN = 'START'
PADDING_TOKEN = 'PADDING'
END_TOKEN = 'END'
model = Transformer(d_model, 
                          ffn_hidden,
                          num_heads, 
                          drop_prob, 
                          num_layers, 
                          max_sequence_length,
                          vocab_size,
                          vi_to_index,
                          START_TOKEN, 
                          END_TOKEN, 
                          PADDING_TOKEN).to(device)



model.load_state_dict(torch.load(model_path))

def chat_predict(input_user):
    bot_pred = predict(model , input_user ,max_sequence_length, index_to_vi ,device)
    return bot_pred